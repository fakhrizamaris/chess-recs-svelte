# 🎓 CLOUD RUN DEPLOYMENT - STEP BY STEP CLI GUIDE

Panduan manual deployment dengan penjelasan setiap command.

---

## 📋 PREREQUISITES CHECKLIST

Sebelum mulai, pastikan:

- [ ] Google Cloud SDK sudah terinstall
- [ ] Punya Google account
- [ ] Sudah ada GCP project (atau akan buat baru)
- [ ] $5 credit sudah aktif (atau will activate)
- [ ] Terminal/PowerShell terbuka

---

## STEP 1: VERIFY GCLOUD INSTALLATION

**Command:**

```powershell
gcloud --version
```

**Expected Output:**

```
Google Cloud SDK 457.0.0
...
```

**Explanation:**

- Verifies gcloud CLI is installed
- Shows current version
- If error: Install from https://cloud.google.com/sdk/docs/install

**Troubleshooting:**

```powershell
# If "command not found":
# 1. Close and reopen PowerShell
# 2. Or add to PATH: C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin
```

---

## STEP 2: LOGIN TO GOOGLE CLOUD

**Command:**

```powershell
gcloud auth login
```

**What Happens:**

1. Opens browser automatically
2. Shows Google sign-in page
3. Choose your Google account
4. Click "Allow"
5. Browser shows "You are now authenticated"
6. Return to terminal

**Expected Output:**

```
You are now logged in as [YOUR-EMAIL@gmail.com]
Your current project is [PROJECT-ID]
```

**Explanation:**

- Authenticates your Google account
- Creates credentials for gcloud CLI
- Allows you to manage GCP resources

**Alternative (if browser doesn't open):**

```powershell
# Copy the link shown in terminal
# Paste in browser
# Complete authentication
# Copy verification code back to terminal
```

---

## STEP 3: SET APPLICATION DEFAULT CREDENTIALS

**Command:**

```powershell
gcloud auth application-default login
```

**What Happens:**

- Similar to step 2 (opens browser)
- Approve access
- These credentials are for applications (Docker builds)

**Expected Output:**

```
Credentials saved to file: [~/.config/gcloud/application_default_credentials.json]
```

**Explanation:**

- Allows Cloud Build to access your project
- Needed for `gcloud builds submit`
- Separate from user credentials

---

## STEP 4: LIST EXISTING PROJECTS (Optional)

**Command:**

```powershell
gcloud projects list
```

**Expected Output:**

```
PROJECT_ID          NAME                PROJECT_NUMBER
my-project-12345    My Project          123456789012
another-proj        Another Project     987654321098
```

**Explanation:**

- Shows all GCP projects you have access to
- Note the PROJECT_ID (you'll need this!)
- If empty: No projects yet (we'll create one)

**Use Existing or Create New?**

- Existing: Use PROJECT_ID from list
- New: Continue to Step 5

---

## STEP 5: CREATE NEW PROJECT (If Needed)

**Command:**

```powershell
gcloud projects create chessrecs-ai-prod --name="ChessRecs AI Production"
```

**Parameters Explained:**

- `chessrecs-ai-prod` = PROJECT_ID (must be unique globally!)
- `--name="..."` = Human-readable name

**Expected Output:**

```
Create in progress for [https://cloudresourcemanager.googleapis.com/v1/projects/chessrecs-ai-prod].
Waiting for [operations/cp.1234567890123456789] to finish...done.
```

**Explanation:**

- Creates new GCP project
- PROJECT_ID must be globally unique (3-30 chars, lowercase, numbers, hyphens)
- Name can be anything

**If PROJECT_ID already exists:**

```powershell
# Try: chessrecs-ai-prod-2
# Or: chessrecs-ai-yourname
# Or: chess-recs-12345
```

---

## STEP 6: SET DEFAULT PROJECT

**Command:**

```powershell
gcloud config set project chessrecs-ai-prod
```

**Expected Output:**

```
Updated property [core/project].
```

**Explanation:**

- Sets this project as default for all commands
- Won't need to specify `--project` flag every time
- Can check current project: `gcloud config get-value project`

**Verify:**

```powershell
gcloud config get-value project
# Should output: chessrecs-ai-prod
```

---

## STEP 7: ENABLE REQUIRED APIs

**Command:**

```powershell
gcloud services enable cloudbuild.googleapis.com
```

**Expected Output:**

```
Operation "operations/acf.p2-123456789" finished successfully.
```

**What This Does:**

- Enables Cloud Build API
- Needed to build Docker images
- First-time: Takes 30-60 seconds

**Then enable Cloud Run:**

```powershell
gcloud services enable run.googleapis.com
```

**Then enable Container Registry:**

```powershell
gcloud services enable containerregistry.googleapis.com
```

**All-in-one (Optional):**

```powershell
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
```

**Explanation:**

- `cloudbuild` = Builds Docker images in cloud
- `run` = Cloud Run service
- `containerregistry` = Stores Docker images

**Troubleshooting:**

```
Error: "billing account must be attached"
Solution: Go to console.cloud.google.com → Billing → Link account
```

---

## STEP 8: BUILD DOCKER IMAGE

**Navigate to service directory:**

```powershell
cd d:\Portofolio\portfolio\chess-recs-nextgen\services-api
```

**Command:**

```powershell
gcloud builds submit --tag gcr.io/chessrecs-ai-prod/chessrecs-ai
```

**Parameters Explained:**

- `--tag` = Image name
- `gcr.io` = Google Container Registry
- `chessrecs-ai-prod` = Your PROJECT_ID
- `chessrecs-ai` = Image name (any name you want)

**What Happens:**

1. Uploads current directory to Cloud Build (excludes .dockerignore files)
2. Finds Dockerfile
3. Builds image in cloud (not local!)
4. Pushes to Google Container Registry
5. Takes 5-15 minutes (first time)

**Expected Output (Progress):**

```
Creating temporary tarball archive of XX files in d:\...
Uploading tarball of [.] to [gs://...]
...
BUILD
Starting Step #0 - "pulling image"
Step #0: Pulling image: gcr.io/cloud-builders/docker
...
Step #1: Successfully built abc123def456
...
PUSH
Pushing gcr.io/chessrecs-ai-prod/chessrecs-ai
...
DONE
```

**Final Output:**

```
ID                                    CREATE_TIME                DURATION  SOURCE  IMAGES  STATUS
12345678-1234-1234-1234-123456789012  2026-01-16T11:30:00+00:00  10M15S    gs://   gcr...  SUCCESS
```

**Explanation:**

- Builds Docker image using your Dockerfile
- Runs in Google's servers (not local)
- Image stored in Container Registry
- Can be reused for multiple deployments

**Troubleshooting:**

```powershell
# If "Dockerfile not found":
ls Dockerfile  # Verify file exists
pwd  # Verify you're in services-api directory

# If build fails:
# Check logs in output
# Common: Requirements installation error
# Solution: Check requirements.txt syntax
```

---

## STEP 9: DEPLOY TO CLOUD RUN

**Command:**

```powershell
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
```

**Parameters Explained:**

| Parameter                 | Value           | Why?                     |
| ------------------------- | --------------- | ------------------------ |
| `chessrecs-ai`            | Service name    | Identifies your service  |
| `--image`                 | gcr.io/...      | Docker image from Step 8 |
| `--platform managed`      | Serverless      | Auto-scaling, no servers |
| `--region`                | asia-southeast1 | Singapore (closest!)     |
| `--allow-unauthenticated` | Public          | Anyone can call API      |
| `--memory`                | 2Gi             | TensorFlow needs RAM     |
| `--cpu`                   | 1               | 1 virtual CPU            |
| `--timeout`               | 300s            | Max 5min per request     |
| `--max-instances`         | 10              | Cost protection          |
| `--min-instances`         | 0               | Free when idle           |
| `--port`                  | 8080            | Container port           |

**What Happens:**

1. Creates Cloud Run service
2. Deploys your container
3. Configures networking
4. Assigns public URL
5. Takes 1-3 minutes

**Expected Output:**

```
Deploying container to Cloud Run service [chessrecs-ai] in project [chessrecs-ai-prod] region [asia-southeast1]
✓ Deploying... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
Done.
Service [chessrecs-ai] revision [chessrecs-ai-00001-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://chessrecs-ai-xxxxxxxxxxxx-as.a.run.app
```

**Explanation:**

- Creates new service on Cloud Run
- Allocates resources (2GB RAM, 1 CPU)
- Generates public HTTPS URL
- Auto-scales 0-10 instances
- Charges only when requests come in

**Troubleshooting:**

```powershell
# If "service deployment failed":
# Check logs:
gcloud run services logs read chessrecs-ai --region asia-southeast1 --limit 50

# Common issues:
# 1. Port mismatch: Container must listen on $PORT (we set ENV PORT=8080 in Dockerfile)
# 2. Startup timeout: Service takes too long (increase --timeout)
# 3. Memory: TensorFlow crashes (increase --memory to 4Gi)
```

---

## STEP 10: GET SERVICE URL

**Command:**

```powershell
gcloud run services describe chessrecs-ai `
    --region asia-southeast1 `
    --format 'value(status.url)'
```

**Expected Output:**

```
https://chessrecs-ai-xxxxxxxxxxxx-as.a.run.app
```

**Explanation:**

- Retrieves the public URL of your service
- This is your API endpoint
- Already has HTTPS enabled
- Copy this URL for testing

**Save it:**

```powershell
# Save to variable (PowerShell)
$API_URL = gcloud run services describe chessrecs-ai --region asia-southeast1 --format 'value(status.url)'
echo $API_URL
```

---

## STEP 11: TEST DEPLOYMENT

**Test 1: Health Check**

```powershell
curl "$API_URL/health"
```

**Expected:**

```json
{ "status": "healthy", "model_ready": true }
```

**Test 2: Openings Endpoint**

```powershell
curl "$API_URL/openings"
```

**Expected:**

```json
{"openings":["Sicilian Defense","French Defense",...], "count":XX}
```

**Test 3: Recommendations**

```powershell
curl -X POST "$API_URL/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "user_rating": 1500,
    "favorite_openings": ["Sicilian Defense"],
    "alpha": 0.5
  }'
```

**Expected:**

```json
[
  {
    "opening_name": "French Defense",
    "fen": "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR",
    "hybrid_score": 0.87,
    ...
  },
  ...
]
```

**If using Windows PowerShell and curl doesn't work:**

```powershell
# Use Invoke-WebRequest instead:
Invoke-WebRequest -Uri "$API_URL/health"
```

---

## STEP 12: UPDATE FRONTEND

**File:** `frontend-svelte/src/lib/api/client.ts`

**Change:**

```typescript
// Before:
const API_BASE = 'http://localhost:3000';

// After:
const API_BASE = 'https://chessrecs-ai-xxxxxxxxxxxx-as.a.run.app';
// ← Use your actual URL from Step 10
```

**Test frontend:**

1. Save file
2. Vite auto-reloads
3. Try get recommendations
4. Should call Cloud Run API now!

---

## 📊 MONITORING & LOGS

### View Logs:

```powershell
# Real-time logs
gcloud run services logs read chessrecs-ai --region asia-southeast1 --follow

# Last 50 lines
gcloud run services logs read chessrecs-ai --region asia-southeast1 --limit 50
```

### View Service Details:

```powershell
gcloud run services describe chessrecs-ai --region asia-southeast1
```

### Check Metrics (Web):

```
https://console.cloud.google.com/run/detail/asia-southeast1/chessrecs-ai/metrics
```

---

## 💰 COST MONITORING

### Set Budget Alert:

```powershell
# Via web console (easier):
# 1. Go to: https://console.cloud.google.com/billing/budgets
# 2. Click "Create Budget"
# 3. Set amount: $5
# 4. Alert at: 50%, 90%, 100%
# 5. Add your email
```

### Check Current Spending:

```powershell
# Via web:
https://console.cloud.google.com/billing/
```

---

## 🔄 UPDATE/REDEPLOY

**When you make changes:**

**1. Rebuild image:**

```powershell
cd services-api
gcloud builds submit --tag gcr.io/chessrecs-ai-prod/chessrecs-ai
```

**2. Redeploy (uses same config):**

```powershell
gcloud run services update chessrecs-ai `
    --image gcr.io/chessrecs-ai-prod/chessrecs-ai `
    --region asia-southeast1
```

**Or deploy with new config:**

```powershell
# Just run Step 9 command again
# It will update existing service
```

---

## 🐛 TROUBLESHOOTING CHEATSHEET

### Service won't start:

```powershell
# Check logs
gcloud run services logs read chessrecs-ai --region asia-southeast1 --limit 100

# Common causes:
# - Port mismatch (set ENV PORT=8080 in Dockerfile)
# - Missing dependencies (check requirements.txt)
# - Model files too large (use GCS instead)
```

### Out of memory:

```powershell
# Increase memory
gcloud run services update chessrecs-ai `
    --memory 4Gi `
    --region asia-southeast1
```

### Too slow:

```powershell
# Increase timeout
gcloud run services update chessrecs-ai `
    --timeout 600 `
    --region asia-southeast1
```

### Delete service (if needed):

```powershell
gcloud run services delete chessrecs-ai --region asia-southeast1
```

---

## ✅ SUCCESS CHECKLIST

- [ ] Step 1: gcloud --version works
- [ ] Step 2: Logged in to Google
- [ ] Step 3: Application credentials set
- [ ] Step 4: Listed projects
- [ ] Step 5: Created/selected project
- [ ] Step 6: Set default project
- [ ] Step 7: Enabled APIs
- [ ] Step 8: Built Docker image (SUCCESS)
- [ ] Step 9: Deployed to Cloud Run
- [ ] Step 10: Got service URL
- [ ] Step 11: All 3 tests passed
- [ ] Step 12: Updated frontend

---

## 📚 USEFUL COMMANDS REFERENCE

```powershell
# List all Cloud Run services
gcloud run services list

# Get service URL
gcloud run services describe SERVICE_NAME --region REGION --format 'value(status.url)'

# View logs (follow)
gcloud run services logs read SERVICE_NAME --region REGION --follow

# Update service config
gcloud run services update SERVICE_NAME --OPTION=VALUE --region REGION

# Delete service
gcloud run services delete SERVICE_NAME --region REGION

# List regions
gcloud run regions list

# Check quotas
gcloud projects describe PROJECT_ID

# Set region default
gcloud config set run/region asia-southeast1
```

---

**Next:** Follow each step carefully, understand each command!  
**Time:** ~30-45 minutes first time  
**Result:** API live on Cloud Run! 🚀

Ready untuk mulai Step 1? 🎓
