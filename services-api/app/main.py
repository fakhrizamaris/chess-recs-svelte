from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.schemas import RecommendationRequest, RecommendationResponse
from app.services.engine import recommender
from typing import List
import pandas as pd
from app.config import settings

# --- Lifespan Event (Pengganti @on_event("startup")) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model saat aplikasi start
    recommender.load_resources()
    if not recommender.is_ready:
        print("⚠️ Warning: Models failed to load. API will return errors.")
    yield
    # Clean up resources jika perlu (saat shutdown)
    print("🛑 Shutting down AI Service...")

app = FastAPI(title="ChessRecs AI Service", version="1.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (atau specify ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router for API endpoints
router = APIRouter()

@app.get("/")
def health_check():
    return {"status": "active", "model_ready": recommender.is_ready}

@app.get("/openings")
def get_all_openings():
    """Get list of unique opening names from games.csv"""
    try:
        df = pd.read_csv(settings.DATA_PATH)
        
        # Get unique opening names and sort
        if 'opening_name' in df.columns:
            openings = df['opening_name'].dropna().unique().tolist()
            openings.sort()
            return {"openings": openings, "count": len(openings)}
        else:
            # Fallback to hardcoded list if column not found
            return {"openings": [
                "Sicilian Defense",
                "French Defense", 
                "Caro-Kann Defense",
                "Italian Game",
                "Spanish Opening",
                "Queen's Gambit",
                "King's Indian Defense",
                "English Opening",
                "Ruy Lopez",
                "Scandinavian Defense",
                "Nimzo-Indian Defense",
                "Pirc Defense"
            ], "count": 12}
    except Exception as e:
        print(f"Error loading openings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load openings: {str(e)}")

@app.post("/predict", response_model=List[RecommendationResponse])
def get_recommendations(payload: RecommendationRequest):
    if not recommender.is_ready:
        raise HTTPException(status_code=503, detail="AI Models are not loaded yet.")
    
    try:
        results = recommender.predict(
            user_rating=payload.user_rating,
            favorite_openings=payload.favorite_openings,
            alpha=payload.alpha
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Reload=True hanya untuk development
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)