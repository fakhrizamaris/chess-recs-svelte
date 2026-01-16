from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationRequest(BaseModel):
    user_rating: int = Field(..., ge=500, le=3000, description="Rating ELO User")
    favorite_openings: List[str] = Field(..., min_length=1, max_length=5, description="List nama opening favorit")
    alpha: float = Field(0.7, ge=0.0, le=1.0, description="Bobot Hybrid (0.0 - 1.0)")

class RecommendationResponse(BaseModel):
    opening_name: str
    archetype: Optional[str] = "Unknown"
    moves: str
    fen: str  # FEN notation for chess board visualization
    hybrid_score: float
    cb_score: float
    cf_score: float
    # Kita tambahkan win rates agar frontend Svelte tidak perlu hitung manual
    win_rate_white: float
    win_rate_black: float
    win_rate_draw: float