use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct RecommendationRequest {
    pub user_rating: u32,
    pub favorite_openings: Vec<String>,
    pub alpha: f32,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct RecommendationResponse {
    pub opening_name: String,
    pub archetype: Option<String>,
    pub moves: String,
    pub fen: String,  // FEN notation for chess board visualization
    pub hybrid_score: f64,
    pub cb_score: f64,
    pub cf_score: f64,
    pub win_rate_white: f64,
    pub win_rate_black: f64,
    pub win_rate_draw: f64,
}