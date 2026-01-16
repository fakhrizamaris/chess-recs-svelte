# 🔍 502 BAD GATEWAY - COMPLETE DEBUG GUIDE

## ❌ ERROR FLOW:

```
Frontend → Rust API (port 3000) → Python AI (port 8001)
          ↓
       502 Bad Gateway ← Python returns 503 Service Unavailable
```

---

## 🔍 WHY 502 BAD GATEWAY?

**502 = Upstream service (Python) returned error**

Python AI Service returning **503 Service Unavailable** because:

```python
# main.py line 72-73
if not recommender.is_ready:
    raise HTTPException(status_code=503, detail="AI Models are not loaded yet.")
```

**Root cause:** `recommender.is_ready = False`  
**Meaning:** Models failed to load!

---

## 🐛 DEBUGGING STEPS

### Step 1: Check Python Terminal Output

**Look for:**

```
⏳ Loading AI Models & Data...
✅ AI Models Loaded Successfully!  ← Should see this!
INFO: Application startup complete.
```

**If you see:**

```
❌ Failed to load models: ...
⚠️ Warning: Models failed to load
```

**Then models didn't load!**

### Step 2: Common Causes

**A. Wrong File Paths**

```python
# Check config.py variables:
CONTENT_MODEL_PATH = BASE_DIR / "models" / "content_based.pkl"
```

**File must exist:**

```
services-api/models/content_based.pkl  ✅
```

**B. Variable Name Mismatch**

```python
# config.py must have:
COLLAB_MODEL_PATH  # ← Not COLLABORATIVE_MODEL_PATH!
```

**C. Port Conflict**

```
Multiple Python processes on port 8001
```

**D. Import Error**

```python
ModuleNotFoundError: No module named 'chess'
```

---

## ✅ CLEAN RESTART PROCEDURE

### 1. Kill ALL Python Processes

```powershell
# Stop all Python services
taskkill /F /IM python.exe

# Or kill specific PIDs:
netstat -ano | findstr :8001
taskkill /F /PID <PID>
```

### 2. Verify Port Is Free

```powershell
netstat -ano | findstr :8001
# Should return NOTHING
```

### 3. Check Files Exist

```powershell
cd services-api
ls models/

# Should see:
# content_based.pkl  ✅
# collaborative_model.keras  ✅
# collaborative_data.pkl  ✅
# hybrid.pkl  ✅
```

### 4. Verify Config Variables

```powershell
# Check config.py has:
cat app/config.py | Select-String "COLLAB_MODEL_PATH"

# Should output:
# COLLAB_MODEL_PATH = Path(...)  ✅ (not COLLABORATIVE_!)
```

### 5. Clean Start

```powershell
cd services-api
.\.venv\Scripts\Activate.ps1
python -m app.main
```

### 6. Watch Startup

```
Expected output:
⏳ Loading AI Models & Data...
Loading 'content_based.pkl'
Loading 'collaborative_model.keras'
Loading 'collaborative_data.pkl'
Loading 'hybrid.pkl'
✅ AI Models Loaded Successfully!  ← MUST SEE THIS!
INFO: Uvicorn running on http://0.0.0.0:8001
INFO: Application startup complete.
```

### 7. Test Python Service Directly

```powershell
# Test root endpoint
curl.exe http://localhost:8001/

# Expected:
# {"status":"active","model_ready":true}  ✅

# Test openings
curl.exe http://localhost:8001/openings

# Expected:
# {"openings":[...],"count":XX}  ✅
```

### 8. Test Recommendations

```powershell
curl.exe -X POST http://localhost:8001/predict `
  -H "Content-Type: application/json" `
  -d '{\"user_rating\":1500,\"favorite_openings\":[\"Sicilian Defense\"],\"alpha\":0.5}'

# Expected:
# [{"opening_name":"...","fen":"...","hybrid_score":0.87,...}]  ✅

# NOT:
# {"detail":"AI Models are not loaded yet."}  ❌
```

---

## 🔧 TROUBLESHOOTING ERRORS

### Error: "COLLAB_MODEL_PATH not found"

```bash
Solution: Check config.py line 12
Should be: COLLAB_MODEL_PATH (not COLLABORATIVE_MODEL_PATH)
```

### Error: "FileNotFoundError: content_based.pkl"

```bash
Solution:
cd services-api
ls models/  # Verify file exists
# Check path in config.py matches actual file name
```

### Error: "ModuleNotFoundError: chess"

```bash
Solution:
cd services-api
.\.venv\Scripts\Activate.ps1
pip install python-chess
```

### Error: "Port 8001 already in use"

```bash
Solution:
netstat -ano | findstr :8001
taskkill /F /PID <PID>
```

### Error: Still 503 after restart

```bash
Check Python terminal for "✅ AI Models Loaded Successfully!"
If not shown, models failed to load
Read error message in "❌ Failed to load models: ..."
```

---

## 📋 VERIFICATION CHECKLIST

Before testing from browser:

- [ ] No other Python process on port 8001
- [ ] All 4 model files exist in `models/` folder
- [ ] config.py has `COLLAB_MODEL_PATH` (short form)
- [ ] Python service started successfully
- [ ] Saw "✅ AI Models Loaded Successfully!" in terminal
- [ ] `curl http://localhost:8001/` returns model_ready=true
- [ ] `curl http://localhost:8001/openings` works
- [ ] `curl POST /predict` returns recommendations (not 503)

---

## 🎯 EXPECTED FLOW

**After clean restart:**

1. **Python starts:** ✅

```
⏳ Loading AI Models & Data...
✅ AI Models Loaded Successfully!
```

2. **Direct Python test works:** ✅

```
curl localhost:8001/predict → 200 OK
```

3. **Rust can reach Python:** ✅

```
Rust calls localhost:8001/predict → 200 OK
```

4. **Frontend works:** ✅

```
Browser → Rust (port 3000) → Python (port 8001) → 200 OK
```

---

## 🚨 CURRENT STATE DIAGNOSIS

**Symptoms:**

- 502 Bad Gateway from browser
- Frontend → Rust → Python chain broken

**Most Likely Cause:**

```
Models failed to load
↓
recommender.is_ready = False
↓
Python returns 503
↓
Rust sees error, returns 502
↓
Frontend shows "AI Service error"
```

**Fix:** Clean restart with verified config.py

---

## ✅ QUICK FIX NOW:

```powershell
# 1. Kill all Python
taskkill /F /IM python.exe

# 2. Verify config
cd d:\Portofolio\portfolio\chess-recs-nextgen\services-api
cat app\config.py | Select-String "COLLAB_MODEL"
# Should see: COLLAB_MODEL_PATH (not COLLABORATIVE_!)

# 3. Clean start
.\.venv\Scripts\Activate.ps1
python -m app.main

# 4. Watch for success
# MUST see: ✅ AI Models Loaded Successfully!

# 5. Test
curl.exe http://localhost:8001/

# 6. Then test from browser
```

---

**Status:** 🔴 Models not loaded  
**Action:** Clean restart required  
**Expected:** "✅ AI Models Loaded Successfully!" 🎉
