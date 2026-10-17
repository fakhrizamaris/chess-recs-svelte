# Deploy ke VPS (RAM 1 GB) dengan Docker + Caddy

Panduan ini mengganti Cloud Run untuk **AI service (FastAPI)**. Hasil akhirnya: API hidup di `https://api.domainkamu.com`, sertifikat HTTPS diurus otomatis, dan tetap muat di VPS 1 GB.

## 1. Pahami dulu kenapa ini muat di 1 GB

Sebelumnya model collaborative dijalankan dengan TensorFlow. Saya ukur langsung pemakaian RAM-nya:

| Kondisi | TensorFlow (lama) | Numpy (sekarang) |
|---|---|---|
| RAM setelah model dimuat | 833 MB | 213 MB |
| RAM puncak saat prediksi | 1,33 GB | 400 MB |
| Server berjalan (uvicorn) | tidak diukur | 261 MB normal, 446 MB puncak |

Model collaborative-nya ternyata *matrix factorization* sederhana: `sigmoid(dot(emb_player, emb_opening) + bias_player + bias_opening)`. Rumus ini cukup dihitung dengan numpy, jadi TensorFlow tidak perlu dimuat. Bobotnya diekspor sekali ke `services-api/models/collaborative_weights.npz`, dan hasil prediksinya identik dengan versi Keras (selisih skor 0 pada 4 skenario uji).

Gateway Rust juga tidak dipakai di VPS. Kerjanya hanya meneruskan request ke `/predict`, jadi Caddy yang meng-rewrite `/api/recommend` menjadi `/predict`. Ini menghemat RAM dan menghindari build Rust yang bisa membuat VPS 1 GB kehabisan memori.

```
Browser ──HTTPS──> Caddy (:443) ──> ai-service (FastAPI, :8001, hanya internal)
                     │ /api/recommend  → rewrite ke /predict
                     │ /predict, /openings, /health → langsung
```

## 2. Siapkan VPS

Gunakan Ubuntu 22.04 atau 24.04. Login sebagai root atau user dengan sudo.

**Tambah swap 2 GB.** Ini jaring pengaman, bukan kebutuhan harian. Tanpa swap, satu lonjakan memori bisa mematikan proses oleh OOM killer, terutama saat `docker build`.

```bash
fallocate -l 2G /swapfile && chmod 600 /swapfile
mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
echo 'vm.swappiness=10' > /etc/sysctl.d/99-swap.conf && sysctl --system
free -h   # pastikan Swap tampil 2.0Gi
```

**Pasang Docker dan firewall:**

```bash
curl -fsSL https://get.docker.com | sh
ufw allow OpenSSH && ufw allow 80/tcp && ufw allow 443/tcp && ufw allow 443/udp
ufw --force enable
```

## 3. Arahkan domain

Buat DNS **A record** `api.domainkamu.com` yang menunjuk ke IP VPS, lalu tunggu beberapa menit sampai aktif (`dig +short api.domainkamu.com`).

Belum punya domain? Pakai sslip.io. Untuk IP `203.0.113.10`, gunakan `203-0-113-10.sslip.io` sebagai `API_DOMAIN`. Caddy tetap bisa menerbitkan HTTPS untuknya.

## 4. Jalankan

```bash
git clone https://github.com/fakhrizamaris/chess-recs-svelte.git
cd chess-recs-svelte

cp deploy/.env.example deploy/.env
nano deploy/.env        # isi API_DOMAIN dan CORS_ORIGINS

docker compose -f docker-compose.prod.yml --env-file deploy/.env up -d --build
```

Build pertama memakan beberapa menit. Pantau dengan:

```bash
docker compose -f docker-compose.prod.yml ps          # ai-service harus "healthy"
docker compose -f docker-compose.prod.yml logs -f ai-service
docker stats --no-stream                              # cek pemakaian RAM
```

## 5. Verifikasi

```bash
curl https://api.domainkamu.com/health
# {"status":"ok","model_ready":true}

curl -X POST https://api.domainkamu.com/api/recommend \
  -H 'Content-Type: application/json' \
  -d '{"user_rating":1500,"favorite_openings":["Sicilian Defense"],"alpha":0.7}'
```

Kalau `model_ready` bernilai `false`, model gagal dimuat. Lihat `logs ai-service`.

## 6. Sambungkan frontend

Variabel `PUBLIC_*` ditanam saat **build**, jadi frontend harus di-build ulang. Karena Caddy melayani semua endpoint di satu domain, kedua URL diisi sama:

```
PUBLIC_API_GATEWAY_URL=https://api.domainkamu.com
PUBLIC_AI_SERVICE_URL=https://api.domainkamu.com
```

Lalu isi `CORS_ORIGINS` di `deploy/.env` dengan domain frontend (bukan `*`), dan terapkan:

```bash
docker compose -f docker-compose.prod.yml --env-file deploy/.env up -d
```

## 7. Update dan rollback

```bash
git pull
docker compose -f docker-compose.prod.yml --env-file deploy/.env up -d --build
```

Untuk rollback, `git checkout <commit-lama>` lalu jalankan perintah yang sama.

## 8. Kalau ada masalah

| Gejala | Kemungkinan penyebab | Tindakan |
|---|---|---|
| `ai-service` restart terus | Kehabisan RAM | `docker stats`, `dmesg \| grep -i oom`, pastikan swap aktif |
| Caddy gagal terbitkan sertifikat | DNS belum mengarah ke VPS atau port 80/443 tertutup | `dig +short <domain>`, cek `ufw status` |
| Browser memblokir request | `CORS_ORIGINS` tidak memuat domain frontend | Perbaiki lalu `up -d` |
| `model_ready: false` | File model tidak ada atau rusak | Cek `docker compose logs ai-service` |
| Build gagal "Killed" | RAM habis saat `pip install` | Pastikan swap aktif, ulangi build |

## 9. Hal yang belum otomatis

- **Workflow GitHub Actions** (`.github/workflows/deploy-backend.yml`) masih mendeploy ke Cloud Run dan menunjuk ke `*.run.app`. Nonaktifkan atau ubah kalau Cloud Run sudah tidak dipakai, supaya tidak ada deploy yang gagal atau menagih biaya.
- **Rate limiting** belum ada. Untuk trafik publik yang besar, pertimbangkan plugin rate limit Caddy atau Cloudflare di depan domain.
- **Backup**: tidak ada data pengguna yang disimpan, jadi cukup repo ini. Volume `caddy_data` berisi sertifikat TLS dan akan dibuat ulang otomatis kalau hilang.
- **Fallback TensorFlow**: kalau `collaborative_weights.npz` tidak ditemukan, engine mencoba memuat `collaborative_model.keras` lewat TensorFlow. TensorFlow sudah dikeluarkan dari `requirements.txt`, jadi di VPS ini fallback itu tidak aktif. Jalankan `python scripts/export_cf_weights.py` bila model collaborative dilatih ulang.
