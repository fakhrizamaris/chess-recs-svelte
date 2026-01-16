# 🚀 CLOUD RUN DEPLOYMENT - QUICK COMMAND LIST

Quick reference untuk copy-paste setelah baca penjelasan.

---

## ⚡ FAST TRACK (All Commands)

**Replace `chessrecs-ai-prod` with YOUR project ID!**

```powershell
# 1. Verify gcloud
gcloud --version

# 2. Login
gcloud auth login
gcloud auth application-default login

# 3. Create project (or use existing)
gcloud projects create chessrecs-ai-prod --name="ChessRecs AI"

# 4. Set project
gcloud config set project chessrecs-ai-prod

# 5. Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# 6. Navigate to service
cd d:\Portofolio\portfolio\chess-recs-nextgen\services-api

# 7. Build image (takes 5-15 min)
gcloud builds submit --tag gcr.io/chessrecs-ai-prod/chessrecs-ai

# 8. Deploy to Cloud Run
gcloud run deploy chessrecs-ai `
    --image gcr.io/chessrecs-ai-prod/chessrecs-ai `
    --platform managed `
    --region asia-southeast1 `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 1 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --port 8080

# 9. Get URL
gcloud run services describe chessrecs-ai --region asia-southeast1 --format 'value(status.url)'

# 10. Test
$API_URL = gcloud run services describe chessrecs-ai --region asia-southeast1 --format 'value(status.url)'
curl "$API_URL/health"
```

---

## TROUBLESHOOTING COMMANDS

```powershell
# View logs
gcloud run services logs read chessrecs-ai --region asia-southeast1 --limit 50

# Update memory
gcloud run services update chessrecs-ai --memory 4Gi --region asia-southeast1

# Update timeout
gcloud run services update chessrecs-ai --timeout 600 --region asia-southeast1

# Redeploy after changes
gcloud builds submit --tag gcr.io/chessrecs-ai-prod/chessrecs-ai
gcloud run services update chessrecs-ai --image gcr.io/chessrecs-ai-prod/chessrecs-ai --region asia-southeast1

# Delete service
gcloud run services delete chessrecs-ai --region asia-southeast1
```

---

## 📋 VARIABLES TO CHANGE

| Variable     | Example             | Where to Change |
| ------------ | ------------------- | --------------- |
| PROJECT_ID   | `chessrecs-ai-prod` | All commands    |
| SERVICE_NAME | `chessrecs-ai`      | Deploy command  |
| REGION       | `asia-southeast1`   | Deploy command  |

---

**Full Guide:** `MANUAL_DEPLOY_GUIDE.md`
