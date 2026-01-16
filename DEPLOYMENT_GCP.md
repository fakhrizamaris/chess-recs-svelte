# 🚀 Deployment Guide: ChessRecs NextGen to GCP Cloud Run

Panduan lengkap untuk deploy aplikasi ChessRecs NextGen ke Google Cloud Platform menggunakan Cloud Run.

**Project ID:** `chess-recs-484510`

---

## 📋 Prerequisites

1. **Google Cloud Account** dengan billing aktif
2. **gcloud CLI** terinstall ([Download](https://cloud.google.com/sdk/docs/install))

---

## 🔧 Setup Awal

### 1. Login ke GCloud

```powershell
# Login
gcloud auth login

# Set project
gcloud config set project chess-recs-484510

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 2. Buat Artifact Registry

```powershell
# Buat repository
gcloud artifacts repositories create chess-recs-repo `
  --repository-format=docker `
  --location=asia-southeast1 `
  --description="ChessRecs NextGen Docker images"

# Configure Docker authentication
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

---

## 🐍 Deploy AI Service (Python/FastAPI)

### Step 1: Build & Submit Image (Cloud Build)

Kita menggunakan `gcloud builds submit` agar tidak perlu Docker lokal.

```powershell
cd services-api

# Submit build ke Cloud
gcloud builds submit --tag asia-southeast1-docker.pkg.dev/chess-recs-484510/chess-recs-repo/ai-service:latest .
```

### Step 2: Deploy ke Cloud Run

```powershell
gcloud run deploy ai-service `
  --image asia-southeast1-docker.pkg.dev/chess-recs-484510/chess-recs-repo/ai-service:latest `
  --platform managed `
  --region asia-southeast1 `
  --memory 2Gi `
  --cpu 1 `
  --timeout 300 `
  --concurrency 10 `
  --min-instances 0 `
  --max-instances 3 `
  --allow-unauthenticated `
  --set-env-vars "PYTHONUNBUFFERED=1,TF_ENABLE_ONEDNN_OPTS=0"
```

### Step 3: Catat URL

Setelah deploy selesai, catat URLnya (contoh: `https://ai-service-xxxxx-as.a.run.app`).
https://ai-service-245846929382.asia-southeast1.run.app
---

## 🦀 Deploy API Gateway (Rust/Axum)

### Step 1: Update Environment Variable

Edit `backend-rust/.env` (lokal saja, untuk referensi):

```env
AI_SERVICE_URL=https://ai-service-xxxxx-as.a.run.app
```

### Step 2: Build & Submit Image

```powershell
cd backend-rust

gcloud builds submit --tag asia-southeast1-docker.pkg.dev/chess-recs-484510/chess-recs-repo/api-gateway:latest .
```

### Step 3: Deploy ke Cloud Run

**Ganti URL di bawah dengan URL AI Service Anda!**

```powershell
gcloud run deploy api-gateway `
  --image asia-southeast1-docker.pkg.dev/chess-recs-484510/chess-recs-repo/api-gateway:latest `
  --platform managed `
  --region asia-southeast1 `
  --memory 512Mi `
  --cpu 1 `
  --timeout 60 \
  --concurrency 100 `
  --min-instances 0 `
  --max-instances 5 `
  --allow-unauthenticated `
  --set-env-vars "RUST_LOG=info,AI_SERVICE_URL=https://ai-service-245846929382.asia-southeast1.run.app"
```

### Step 4: Catat URL Gateway

Catat URLnya (contoh: `https://api-gateway-xxxxx-as.a.run.app`).
https://api-gateway-245846929382.asia-southeast1.run.app
---

## ⚡ Deploy Frontend (SvelteKit)

### Step 1: Build & Submit Image

**PENTING:** Ganti kedua URL di bawah dengan URL aktual dari langkah sebelumnya.

```powershell
cd frontend-svelte

gcloud builds submit `
  --tag asia-southeast1-docker.pkg.dev/chess-recs-484510/chess-recs-repo/frontend:latest `
  --build-arg PUBLIC_API_GATEWAY_URL="https://api-gateway-xxxxx-as.a.run.app" `
  --build-arg PUBLIC_AI_SERVICE_URL="https://ai-service-xxxxx-as.a.run.app" `
  .
```

### Step 2: Deploy ke Cloud Run

```powershell
gcloud run deploy frontend `
  --image asia-southeast1-docker.pkg.dev/chess-recs-484510/chess-recs-repo/frontend:latest `
  --platform managed `
  --region asia-southeast1 `
  --memory 256Mi `
  --cpu 1 `
  --timeout 30 `
  --concurrency 200 `
  --min-instances 0 `
  --max-instances 10 `
  --allow-unauthenticated
```

### Step 3: Akses Aplikasi

```
https://frontend-xxxxx-as.a.run.app
```
