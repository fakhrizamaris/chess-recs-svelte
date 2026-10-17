# ChessRecs AI Service (FastAPI + TensorFlow CPU)
# Berjalan di Cloud Run (PORT diisi otomatis) maupun VPS (default 8001).
FROM python:3.11-slim

WORKDIR /app

# Tidak perlu build-essential: semua dependensi punya wheel siap pakai
# (python-chess murni Python). Image lebih kecil dan build lebih cepat.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# PORT default 8001 agar sama dengan config.py dan docker-compose.
# Cloud Run menimpa nilai ini dengan PORT miliknya (8080).
ENV PORT=8001 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Hemat RAM dan kurangi log berisik dari TensorFlow
    TF_ENABLE_ONEDNN_OPTS=0 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    OMP_NUM_THREADS=1 \
    TF_NUM_INTRAOP_THREADS=1 \
    TF_NUM_INTEROP_THREADS=1 \
    MALLOC_ARENA_MAX=2

EXPOSE 8001

# Healthcheck memakai stdlib (urllib), tanpa curl/requests.
# start-period panjang karena TensorFlow butuh waktu memuat model di VPS kecil.
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\", \"8001\")}/health', timeout=5)" || exit 1

# Satu worker saja: model dimuat sekali ke memori, worker kedua = RAM dobel.
CMD exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${PORT} \
    --workers 1 \
    --timeout-keep-alive 75 \
    --log-level info
