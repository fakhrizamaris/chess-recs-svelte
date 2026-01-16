mod models;
mod handlers;

use axum::{
    routing::{get, post},
    Router,
};
use dotenv::dotenv;
use std::net::SocketAddr;
use tower_http::cors::{Any, CorsLayer};

#[tokio::main]
async fn main() {
    // 1. Load Environment Variables
    dotenv().ok();
    
    // 2. Setup Logging (Opsional tapi bagus)
    tracing_subscriber::fmt::init();

    // 3. Setup CORS (PENTING BUAT SVELTE)
    // Di production, ganti 'Any' dengan alamat domain Svelte kamu
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    // 4. Setup Routing
    let app = Router::new()
        .route("/health", get(|| async { "Rust Backend is Healthy! 🦀" }))
        .route("/api/recommend", post(handlers::get_recommendations))
        .layer(cors);

    // 5. Jalankan Server
    let port = std::env::var("PORT").unwrap_or_else(|_| "3000".to_string());
    let addr: SocketAddr = format!("0.0.0.0:{}", port).parse().unwrap();

    println!("🦀 Rust Backend berjalan di http://{}", addr);
    
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}