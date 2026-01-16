use axum::{
    extract::Json,
    http::StatusCode,
    response::IntoResponse,
};
use std::env;
use crate::models::{RecommendationRequest, RecommendationResponse};

pub async fn get_recommendations(
    Json(payload): Json<RecommendationRequest>,
) -> impl IntoResponse {
    // 1. Validasi Input (Layer keamanan Rust)
    if payload.favorite_openings.is_empty() {
        return (StatusCode::BAD_REQUEST, "Wajib pilih minimal 1 opening!").into_response();
    }
    if payload.user_rating < 500 || payload.user_rating > 3000 {
        return (StatusCode::BAD_REQUEST, "Rating tidak valid (500-3000)").into_response();
    }


    let ai_service_base = env::var("AI_SERVICE_URL")
        .unwrap_or_else(|_| "http://localhost:8001".to_string());

    // Pastikan URL mengarah ke endpoint /predict
    let ai_service_url = if ai_service_base.ends_with("/predict") {
        ai_service_base
    } else {
        format!("{}/predict", ai_service_base.trim_end_matches('/'))
    };

    println!("🔗 Forwarding request to: {}", ai_service_url); // Log untuk debugging

    // 3. Tembak ke Python (Proxy)
    let client = reqwest::Client::new();
    let response = client.post(&ai_service_url)
        .json(&payload)
        .send()
        .await;

    // 4. Handle Respon dari Python
    match response {
        Ok(resp) => {
            if resp.status().is_success() {
                // Jika Python sukses, teruskan JSON ke Frontend
                match resp.json::<Vec<RecommendationResponse>>().await {
                    Ok(data) => (StatusCode::OK, Json(data)).into_response(),
                    Err(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Gagal parsing data dari AI").into_response(),
                }
            } else {
                (StatusCode::BAD_GATEWAY, "AI Service error").into_response()
            }
        }
        Err(e) => {
            println!("❌ Gagal konek ke Python: {}", e);
            (StatusCode::SERVICE_UNAVAILABLE, "AI Service sedang mati").into_response()
        }
    }
}