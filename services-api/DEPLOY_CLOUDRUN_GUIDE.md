# 🚀 GOOGLE CLOUD RUN DEPLOYMENT GUIDE

## 💰 COST OPTIMIZATION dengan $5 Credit

**Your Situation:**

- $5 GCP credit (180 days)
- Need free/cheap hosting
- ML microservice (TensorFlow)

**Perfect Match:** Google Cloud Run! ✅

---

## 💵 FREE TIER BREAKDOWN

### Cloud Run Free Tier (PERMANENT):

```
✅ 2 million requests/month FREE
✅ 360,000 vCPU-seconds/month FREE
✅ 180,000 vCPU-seconds/month FREE (memory)
✅ 1GB egress/month FREE
```

### With Your $5 Credit:

```
Estimated usage cost (low-medium traffic): $3-5/month
$5 credit = 1-2 months coverage
After credit: Still mostly in free tier!

Result: 180 days coverage EASY! 🎉
```

---

## 📦 FILES CREATED FOR YOU

✅ **Dockerfile** - Optimized for Cloud Run  
✅ **.dockerignore** - Reduced image size  
✅ **config.py** - Updated with env vars  
✅ **deploy-cloudrun.sh** - Bash deployment script  
✅ **deploy-cloudrun.ps1** - PowerShell deployment script

---

## 🚀 DEPLOYMENT STEPS

### Prerequisites:

**1. Install Google Cloud SDK:**

```powershell
# Download from:
https://cloud.google.com/sdk/docs/install

# Or with Chocolatey:
choco install gcloudsdk
```

**2. Login to GCP:**

```bash
gcloud auth login
gcloud auth application-default login
```

**3. Create GCP Project:**

```bash
# Go to: https://console.cloud.google.com/
# Create new project or use existing
# Note your PROJECT_ID
```

---

### Quick Deploy (Automated):

**1. Edit deploy script:**

```powershell
# Open: services-api/deploy-cloudrun.ps1
# Change line 4:
$ProjectId = "YOUR-GCP-PROJECT-ID"  # ← Your actual project ID
```

**2. Run deployment:**

```powershell
cd services-api
.\deploy-cloudrun.ps1
```

**3. Wait 10-15 minutes** ☕

**4. Done!** Your API is live! 🎉

---

### Manual Deploy (Step-by-Step):

**1. Set GCP Project:**

```bash
gcloud config set project YOUR-PROJECT-ID
```

**2. Enable APIs:**

```bash
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com
```

**3. Build Image:**

```bash
cd services-api
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/chessrecs-ai
```

**4. Deploy to Cloud Run:**

```bash
gcloud run deploy chessrecs-ai \
    --image gcr.io/YOUR-PROJECT-ID/chessrecs-ai \
    --platform managed \
    --region asia-southeast1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10 \
    --min-instances 0 \
    --port 8080
```

**5. Get Service URL:**

```bash
gcloud run services describe chessrecs-ai \
    --region asia-southeast1 \
    --format 'value(status.url)'
```

---

## 🔧 COST OPTIMIZATION TIPS

### 1. **Min Instances = 0** ✅ (Already set)

- No charge when idle
- Cold start ~4-8 seconds (acceptable)

### 2. **Max Instances = 10** ✅

- Prevents runaway costs
- Adjust based on traffic

### 3. **Memory = 2GB** ✅

- Enough for TensorFlow
- Lower = cheaper but might crash

### 4. **Region: asia-southeast1** ✅

- Singapore (closest to you)
- Lower latency
- Same price as other regions

### 5. **Request Timeout = 300s**

- Max for Cloud Run
- ML inference can be slow

---

## 💰 EXPECTED COSTS

### Scenario 1: Low Traffic (100 req/day)

```
Monthly: 3,000 requests
vCPU: ~6,000 seconds
Memory: ~12,000 seconds

Cost: $0 (well within free tier!) ✅
```

### Scenario 2: Medium Traffic (1000 req/day)

```
Monthly: 30,000 requests
vCPU: ~60,000 seconds
Memory: ~120,000 seconds

Cost: ~$3/month
Your $5 credit: Covers 1.5 months
After credit: ~$3/month
```

### Scenario 3: High Traffic (10k req/day)

```
Monthly: 300,000 requests
vCPU: ~600,000 seconds (exceeds free tier)
Memory: ~1.2M seconds

Cost: ~$15/month
Your $5 credit: Covers ~10 days
Need to upgrade OR optimize
```

---

## 📊 MONITORING COSTS

### Check spending:

```bash
# Via command line
gcloud billing accounts list
gcloud billing projects describe YOUR-PROJECT-ID

# Or visit:
https://console.cloud.google.com/billing/
```

### Set Budget Alerts:

```bash
# Go to: https://console.cloud.google.com/billing/budgets
# Create budget: $5
# Alert at: 50%, 90%, 100%
```

---

## 🧪 TESTING DEPLOYMENT

### After deployment, test:

**1. Health Check:**

```bash
curl https://YOUR-SERVICE-URL/health
# Should return: {"status":"healthy","model_ready":true}
```

**2. Openings Endpoint:**

```bash
curl https://YOUR-SERVICE-URL/openings
# Should return: {"openings":[...], "count":XX}
```

**3. Recommendations:**

```bash
curl -X POST https://YOUR-SERVICE-URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "user_rating": 1500,
    "favorite_openings": ["Sicilian Defense"],
    "alpha": 0.5
  }'
# Should return: Array of 5 recommendations
```

---

## 🔄 UPDATE FRONTEND

**After deployment, update frontend API URL:**

**File:** `frontend-svelte/src/lib/api/client.ts`

```typescript
// Change from:
const API_BASE = 'http://localhost:3000';

// To:
const API_BASE = 'https://YOUR-CLOUD-RUN-URL';
// Example: 'https://chessrecs-ai-xxxxx-as.a.run.app'
```

---

## 🐛 TROUBLESHOOTING

### Issue: Build fails

```
Error: models/*.pkl files too large
```

**Solution:**

```bash
# Check model sizes
ls -lh models/

# If > 500MB, use Google Cloud Storage instead
# Update config.py to load from GCS
```

### Issue: Deployment timeout

```
Error: Service failed to become ready
```

**Solution:**

```bash
# Check logs
gcloud run services logs read chessrecs-ai --region asia-southeast1

# Increase startup timeout
--timeout 600  # 10 minutes
```

### Issue: Memory exceeded

```
Error: Container killed due to memory
```

**Solution:**

```bash
# Increase memory
--memory 4Gi  # Cost: ~2x more
```

---

## 📈 SCALING STRATEGY

### Phase 1: MVP (Current)

```
Config: 2GB RAM, 1 CPU, min=0, max=10
Traffic: < 10k req/day
Cost: FREE (within free tier)
```

### Phase 2: Growing (10k-100k req/day)

```
Config: 2GB RAM, 1 CPU, min=1, max=50
Cost: $10-30/month
Optimization: Add caching, optimize models
```

### Phase 3: Scale (100k+ req/day)

```
Config: 4GB RAM, 2 CPU, min=5, max=100
Cost: $50-150/month
Consider: Model compression, load balancing
```

---

## ✅ DEPLOYMENT CHECKLIST

**Before Deploy:**

- [ ] GCP account created
- [ ] $5 credit activated
- [ ] Google Cloud SDK installed
- [ ] Project ID noted
- [ ] deploy-cloudrun.ps1 edited (PROJECT_ID)
- [ ] Models < 500MB OR using GCS

**During Deploy:**

- [ ] APIs enabled (automatic in script)
- [ ] Image built successfully
- [ ] Service deployed
- [ ] URL obtained

**After Deploy:**

- [ ] All endpoints tested
- [ ] Frontend API URL updated
- [ ] Budget alerts configured
- [ ] Monitoring dashboard checked

---

## 🎯 SUCCESS METRICS

**Deployment successful if:**

- ✅ Health endpoint returns 200
- ✅ Openings endpoint works
- ✅ Recommendations endpoint works
- ✅ Response time < 5 seconds
- ✅ No errors in logs
- ✅ Frontend can fetch data

---

## 💡 PRO TIPS

**1. Use Cloud Build Caching:**

```bash
# Speeds up builds 5x
gcloud builds submit --tag=... --cache-from=gcr.io/PROJECT/IMAGE
```

**2. Monitor Free Tier Usage:**

```
Visit monthly: https://console.cloud.google.com/run/
Check: Requests, vCPU-seconds, Memory usage
```

**3. Cold Start Optimization:**

```python
# Add to main.py
@app.on_event("startup")
async def warmup():
    # Warm up TensorFlow
    recommender.predict(...)
```

**4. Use Separate Services:**

```
- API Gateway (Rust) → Cloud Run (small, cheap)
- AI Service (Python) → Cloud Run (larger)
Frontend → Vercel/Netlify (free!)
```

---

## 📞 SUPPORT & RESOURCES

**Documentation:**

- Cloud Run: https://cloud.google.com/run/docs
- Pricing: https://cloud.google.com/run/pricing
- Quotas: https://cloud.google.com/run/quotas

**Community:**

- Stack Overflow: `google-cloud-run`
- Reddit: r/googlecloud
- Discord: GCP Community

---

**Status:** 🟢 **READY TO DEPLOY!**  
**Estimated Setup Time:** 15 minutes  
**Estimated Cost:** FREE ($5 credit covers 180 days!)

Run `.\deploy-cloudrun.ps1` and you're live! 🚀
