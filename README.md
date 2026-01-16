# ♟️ ChessRecs NextGen

> Smart Chess Opening Recommendations using Hybrid Filtering

A modern web application that recommends chess openings based on your rating and playing preferences. Built with a microservices architecture using **Svelte**, **Rust**, and **Python**.

![Tech Stack](https://img.shields.io/badge/Frontend-Svelte-FF3E00?style=flat-square&logo=svelte)
![Tech Stack](https://img.shields.io/badge/Gateway-Rust-000000?style=flat-square&logo=rust)
![Tech Stack](https://img.shields.io/badge/ML-Python-3776AB?style=flat-square&logo=python)
![Tech Stack](https://img.shields.io/badge/ML-TensorFlow-FF6F00?style=flat-square&logo=tensorflow)

---

## 📋 Features

- **Smart Recommendations** - Get personalized opening suggestions based on your ELO rating
- **Hybrid Filtering** - Combines content-based and collaborative filtering approaches
- **Interactive Board** - Visual chess board showing opening positions
- **Win Rate Statistics** - View historical win/draw/loss rates for each opening
- **Adjustable Algorithm** - Fine-tune the balance between content-based and collaborative filtering

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Frontend      │────▶│   API Gateway   │────▶│   AI Service    │
│   (Svelte)      │     │   (Rust/Axum)   │     │   (FastAPI)     │
│   Port: 5173    │     │   Port: 3000    │     │   Port: 8001    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

| Service     | Technology                    | Purpose                           |
| ----------- | ----------------------------- | --------------------------------- |
| Frontend    | SvelteKit + TailwindCSS       | User Interface                    |
| API Gateway | Rust + Axum                   | Request routing, CORS, validation |
| AI Service  | Python + FastAPI + TensorFlow | ML predictions                    |

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Rust 1.70+
- Python 3.11+
- (Optional) Docker & Docker Compose

### Local Development

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/chess-recs-nextgen.git
cd chess-recs-nextgen
```

**2. Start AI Service (Python)**

```bash
cd services-api
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m app.main
```

**3. Start API Gateway (Rust)**

```bash
cd backend-rust
cargo run
```

**4. Start Frontend (Svelte)**

```bash
cd frontend-svelte
npm install
npm run dev
```

**5. Open in browser**

```
http://localhost:5173
```

### Using Docker Compose

```bash
# Build and run all services
docker-compose up --build

# Access the application
open http://localhost:5173
```

---

## 📁 Project Structure

```
chess-recs-nextgen/
├── frontend-svelte/        # SvelteKit frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api/        # API client & config
│   │   │   └── components/ # Svelte components
│   │   └── routes/         # Pages
│   └── Dockerfile
│
├── backend-rust/           # Rust API Gateway
│   ├── src/
│   │   └── main.rs
│   └── Dockerfile
│
├── services-api/           # Python AI Service
│   ├── app/
│   │   ├── main.py
│   │   └── services/
│   │       └── engine.py   # Recommendation engine
│   ├── models/             # Trained ML models
│   └── Dockerfile
│
└── docker-compose.yml      # Container orchestration
```

---

## ⚙️ Configuration

### Environment Variables

**Frontend (.env)**

```env
PUBLIC_API_GATEWAY_URL=http://localhost:3000
PUBLIC_AI_SERVICE_URL=http://localhost:8001
```

**Backend Rust (.env)**

```env
HOST=0.0.0.0
PORT=3000
AI_SERVICE_URL=http://localhost:8001
```

---

## 🧠 How It Works

### Hybrid Recommendation System

The system combines two approaches:

1. **Content-Based Filtering (CB)** - Recommends openings similar to your favorites based on move patterns and characteristics

2. **Collaborative Filtering (CF)** - Recommends openings popular among players with similar ratings

3. **Hybrid Score** - Combines both using the formula:
   ```
   hybrid_score = α × CB_score + (1-α) × CF_score
   ```
   Where α is adjustable (0 = pure CF, 1 = pure CB, 0.5 = balanced)

---

## 📦 Deployment

### Google Cloud Run

```bash
# Build and push images
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-service ./services-api
gcloud builds submit --tag gcr.io/PROJECT_ID/api-gateway ./backend-rust
gcloud builds submit --tag gcr.io/PROJECT_ID/frontend ./frontend-svelte

# Deploy services
gcloud run deploy ai-service --image gcr.io/PROJECT_ID/ai-service
gcloud run deploy api-gateway --image gcr.io/PROJECT_ID/api-gateway
gcloud run deploy frontend --image gcr.io/PROJECT_ID/frontend
```

---

## 📝 License

MIT License - feel free to use this project for learning or portfolio purposes.

---

## 🙏 Acknowledgments

- Chess opening data from Lichess
- Built as a portfolio project demonstrating microservices architecture
