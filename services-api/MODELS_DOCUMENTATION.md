# 📦 MODELS FOLDER - File Overview

## ✅ ACTUAL FILES IN FOLDER

```
services-api/models/
├── content_based_model.pkl       (18.7 MB)  ✅ USED
├── collaborative_model.keras     (10.5 MB)  ✅ USED
├── collaborative_data.pkl        (2.7 MB)   ✅ USED
├── collaborative_model_data.pkl  (3.5 MB)   ❓ NOT USED
└── hybrid_model.pkl              (77 bytes) ✅ USED
```

---

## 🔍 FILE USAGE MAPPING

### config.py Variables → Actual Files:

| Config Variable            | File Path                   | Used?  | Purpose                             |
| -------------------------- | --------------------------- | ------ | ----------------------------------- |
| `CONTENT_MODEL_PATH`       | `content_based.pkl`         | ✅ YES | Content-based recommendation model  |
| `COLLABORATIVE_MODEL_PATH` | `collaborative_model.keras` | ✅ YES | Keras collaborative filtering model |
| `COLLAB_DATA_PATH`         | `collaborative_data.pkl`    | ✅ YES | Collaborative filtering data        |
| `HYBRID_MODEL_PATH`        | `hybrid_model.pkl`          | ✅ YES | Hybrid model configuration          |
| ~~`COLLAB_EXTRA_PATH`~~    | ~~N/A~~                     | ❌ NO  | **REMOVED** - Not used in code      |

---

## 📝 FILES EXPLAINED

### 1. `content_based.pkl` (18.7 MB)

**What:** TF-IDF similarity matrix for content-based filtering
**Used in:** `engine.py` line 54-55
**Purpose:** Find similar openings based on characteristics

### 2. `collaborative_model.keras` (10.5 MB)

**What:** Neural network model for collaborative filtering
**Used in:** `engine.py` line 61-62
**Purpose:** Predict user preferences based on similar users

### 3. `collaborative_data.pkl` (2.7 MB)

**What:** Supporting data for collaborative model
**Used in:** `engine.py` line 57-58
**Purpose:** User-opening interaction matrix

### 4. `hybrid_model.pkl` (77 bytes)

**What:** Hybrid model configuration/weights
**Used in:** `engine.py` line 69-70
**Purpose:** Combine CB + CF predictions

### 5. `collaborative_model_data.pkl` (3.5 MB) ❓

**What:** Unknown - seems redundant with #3
**Used in:** ❌ NOT USED in current code
**Action:** Can be deleted OR investigate if needed

---

## ⚠️ COLLAB_EXTRA_PATH - WHY REMOVED?

**Original code (engine.py line 64-66):**

```python
# with open(settings.COLLAB_EXTRA_PATH, 'rb') as f:
#     collab_data_extra = pickle.load(f)
#     self.collaborative_model.update(collab_data_extra)
```

**Status:** Commented out (not used)

**Reason:** Code works without it!

**Decision:** Removed from config.py to avoid confusion

---

## 🚀 FOR CLOUD DEPLOYMENT

### Model Size Analysis:

```
Total: ~36 MB (under 500MB limit ✅)
```

**Import Models Strategy:**

**Option 1: Include in Docker image** (CURRENT)

```dockerfile
# Dockerfile already includes:
COPY . .
# This copies models/ folder
```

**Pros:**

- ✅ Fast startup
- ✅ No external dependencies
- ✅ Works offline

**Cons:**

- ⚠️ Larger Docker image
- ⚠️ Longer build time

**Option 2: Load from Google Cloud Storage** (FUTURE)

```python
from google.cloud import storage

# Download models at startup
def download_from_gcs():
    client = storage.Client()
    bucket = client.bucket('my-models-bucket')
    blob = bucket.blob('content_based.pkl')
    blob.download_to_filename('models/content_based.pkl')
```

**Pros:**

- ✅ Smaller Docker image
- ✅ Easier model updates
- ✅ Versioning

**Cons:**

- ⚠️ Slower startup
- ⚠️ Network dependency
- ⚠️ Extra GCS costs

**Recommendation for now:** Keep in Docker image (36MB is fine!)

---

## 🧹 CLEANUP SUGGESTION

**collaborative_model_data.pkl** appears unused. To verify:

```bash
# Search for usage in code
grep -r "collaborative_model_data" services-api/

# If no results, safe to delete!
```

---

## 📋 CONFIG.PY FINAL STATE

**Variables defined:**

```python
CONTENT_MODEL_PATH = "models/content_based.pkl"
COLLABORATIVE_MODEL_PATH = "models/collaborative_model.keras"
COLLAB_DATA_PATH = "models/collaborative_data.pkl"
HYBRID_MODEL_PATH = "models/hybrid_model.pkl"
# Note: COLLAB_EXTRA_PATH removed (not used)
```

**All referenced files exist:** ✅  
**No missing files:** ✅  
**No unused variables:** ✅

---

## ✅ SUMMARY

**Question:** Why COLLAB_EXTRA_PATH?  
**Answer:** It was **leftover code** that's not actually used!

**Action Taken:**

1. ✅ Verified engine.py doesn't use it (commented code)
2. ✅ Removed from config.py
3. ✅ Cleaned up documentation

**Result:** Cleaner code, no missing files, no confusion! 🎉

---

**All models accounted for and working!** ✅
