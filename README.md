# ♟️ ChessRecs NextGen

> Modern Chess Opening Recommendation System using Hybrid Filtering & Microservices Architecture

A complete rewrite of the original Streamlit-based chess opening recommendation system, now built with a scalable microservices architecture featuring Rust, Python, and Svelte.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Documentation](#-documentation)

---

## 🎯 Overview

ChessRecs NextGen recommends chess openings based on:

- **User ELO Rating** (500-3000)
- **Favorite Openings** (3 selections)
- **Alpha Weight** (0.0-1.0) for balancing content-based vs collaborative filtering

The system uses **Hybrid Filtering** combining:

- Content-based filtering (opening characteristics)
- Collaborative filtering (neural network)
- Weighted combination controlled by alpha parameter

**Key Features:**

- 🚀 High-performance Rust backend with input validation
- 🧠 Python AI service with TensorFlow & scikit-learn
- 🎨 Modern Svelte frontend with TailwindCSS
- 🔒 Type-safe API with Pydantic & Serde
- 📊 5 personalized opening recommendations
- ⚡ Fast model loading at startup (no request delays)

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Svelte         │  Frontend (Port 5173)
│  + TailwindCSS  │  - User Interface
└────────┬────────┘  - Input Forms
         │           - Results Display
         │ HTTP POST
         ▼
┌─────────────────┐
│  Rust (Axum)    │  API Gateway (Port 3000)
│  Backend        │  - Input Validation
└────────┬────────┘  - Rate Limiting
         │           - CORS Handling
         │ HTTP Proxy
         ▼
┌─────────────────┐
│  Python         │  AI Service (Port 8001)
│  (FastAPI)      │  - Model Loading
└─────────────────┘  - Hybrid Filtering
                     - Predictions
```

**Why Microservices?**

- **Separation of Concerns:** UI, security, and AI logic in separate services
- **Scalability:** Each service can be scaled independently
- **Performance:** Rust handles I/O efficiently, Python handles ML
- **Flexibility:** Replace any service without affecting others

---

## 🛠️ Tech Stack

### Frontend

- **SvelteKit** - Modern reactive framework
- **TailwindCSS v4** - Utility-first CSS
- **Vite** - Fast build tool
- **TypeScript** - Type safety

### Backend (API Gateway)

- **Rust 2021** - Systems programming language
- **Axum** - Web framework
- **Tokio** - Async runtime
- **Serde** - Serialization
- **Reqwest** - HTTP client

### AI Service

- **Python 3.9+** - ML ecosystem
- **FastAPI** - Modern API framework
- **TensorFlow** - Neural networks
- **scikit-learn** - ML algorithms
- **Pandas** - Data processing

### Data

- **games.csv** - 7.6 MB chess games dataset
- **Pickle models** - Pre-trained ML models
- **Keras models** - Collaborative filtering NN

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.9 or higher
- **Rust** 1.70 or higher
- **Node.js** 18 or higher
- **npm** or **yarn**

### 1. Setup Python AI Service

```powershell
cd services-api

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Verify:** http://localhost:8001 should return `{"status":"active","model_ready":true}`

### 2. Setup Rust Backend

```powershell
cd backend-rust

# Build and run
cargo run
```

**Verify:** http://localhost:3000/health should return `Rust Backend is Healthy! 🦀`

### 3. Setup Svelte Frontend

```powershell
cd frontend-svelte

# Install dependencies
npm install

# Run dev server
npm run dev
```

**Verify:** http://localhost:5173 should show the Svelte app

### 4. Test the System

```bash
# Test direct Python AI service
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "user_rating": 1500,
    "favorite_openings": ["Sicilian Defense", "French Defense", "Caro-Kann Defense"],
    "alpha": 0.5
  }'

# Test through Rust gateway
curl -X POST http://localhost:3000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_rating": 1500,
    "favorite_openings": ["Sicilian Defense", "French Defense", "Caro-Kann Defense"],
    "alpha": 0.5
  }'
```

**Expected Response:**

```json
[
  {
    "name": "King's Indian Defense",
    "score": 0.87,
    "reason": "Matches your aggressive playing style"
  }
  // ... 4 more recommendations
]
```

---

## 📁 Project Structure

```
chess-recs-nextgen/
├── backend-rust/           # Rust API Gateway
│   ├── src/
│   │   ├── main.rs        # Server setup, CORS, routing
│   │   ├── handlers.rs    # Route handlers, validation
│   │   └── models.rs      # Data structures (Serde)
│   ├── Cargo.toml         # Rust dependencies
│   └── .env               # Environment variables
│
├── services-api/          # Python AI Service
│   ├── app/
│   │   ├── main.py        # FastAPI app, endpoints
│   │   ├── config.py      # Configuration, paths
│   │   ├── schemas.py     # Pydantic models
│   │   └── services/
│   │       └── engine.py  # Hybrid filtering logic
│   ├── models/            # Pre-trained models (.pkl, .keras)
│   ├── games.csv          # Chess games dataset
│   └── requirements.txt   # Python dependencies
│
└── frontend-svelte/       # Svelte Frontend
    ├── src/
    │   ├── routes/
    │   │   └── +page.svelte  # Main page
    │   └── lib/
    │       ├── components/   # Reusable UI components
    │       └── api/          # API client functions
    ├── package.json       # Node dependencies
    └── vite.config.ts     # Vite configuration
```

---

## 📡 API Documentation

### Rust Backend Endpoints

#### `GET /health`

Health check endpoint.

**Response:**

```
Rust Backend is Healthy! 🦀
```

#### `POST /api/recommend`

Get chess opening recommendations.

**Request Body:**

```json
{
  "user_rating": 1500,
  "favorite_openings": ["Sicilian Defense", "French Defense", "Caro-Kann Defense"],
  "alpha": 0.5
}
```

**Validation:**

- `user_rating`: Integer between 500-3000
- `favorite_openings`: Array of strings, 1-3 items
- `alpha`: Float between 0.0-1.0

**Response:** (200 OK)

```json
[
  {
    "name": "King's Indian Defense",
    "score": 0.87,
    "archetype": "Aggressive",
    "moves": "1. d4 Nf6 2. c4 g6"
  }
  // ... 4 more items
]
```

**Error Responses:**

- `400`: Invalid input (rating out of range, empty openings, etc.)
- `502`: AI Service returned error
- `503`: AI Service unavailable

### Python AI Service Endpoints

#### `GET /`

Health check and model status.

**Response:**

```json
{
  "status": "active",
  "model_ready": true
}
```

#### `POST /predict`

Internal endpoint (called by Rust backend).

**Request/Response:** Same as Rust `/api/recommend`

---

## 💻 Development

### Running All Services (Development Mode)

Open 3 terminals:

**Terminal 1 - Python AI:**

```powershell
cd services-api
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Rust Backend:**

```powershell
cd backend-rust
cargo run
```

**Terminal 3 - Svelte Frontend:**

```powershell
cd frontend-svelte
npm run dev
```

### Environment Variables

#### `backend-rust/.env`

```env
AI_SERVICE_URL=http://localhost:8001/predict
PORT=3000
```

#### `services-api/.env` (optional)

```env
# Currently using hardcoded values in config.py
# Can add custom model paths here
```

### Code Style & Linting

**Rust:**

```bash
cargo fmt       # Format code
cargo clippy    # Lint code
```

**Python:**

```bash
pip install black flake8
black app/      # Format
flake8 app/     # Lint
```

**Svelte:**

```bash
npm run format  # Prettier
npm run lint    # ESLint
```

---

## 🚢 Deployment

### Docker (Optional)

Create `docker-compose.yml` at project root:

```yaml
version: '3.8'

services:
  ai-service:
    build: ./services-api
    ports:
      - '8001:8001'
    environment:
      - PYTHONUNBUFFERED=1

  rust-backend:
    build: ./backend-rust
    ports:
      - '3000:3000'
    environment:
      - AI_SERVICE_URL=http://ai-service:8001/predict
    depends_on:
      - ai-service

  frontend:
    build: ./frontend-svelte
    ports:
      - '5173:5173'
    depends_on:
      - rust-backend
```

Run:

```bash
docker-compose up --build
```

### Production Deployment

**Options:**

- **Frontend:** Vercel, Netlify, CloudFlare Pages
- **Rust Backend:** fly.io, Railway, AWS Lambda (with adapter)
- **Python AI:** Railway, Render, AWS EC2

**Environment Variables for Production:**

- Update `AI_SERVICE_URL` in Rust to production Python URL
- Update CORS origin in Rust `main.rs` to production frontend URL
- Set `reload=False` in Python `uvicorn.run()`

---

## 📚 Documentation

- **[EVALUATION_REPORT.md](../Opening_Chess_Recommendations/EVALUATION_REPORT.md)** - Full PRD evaluation
- **[CONFIGURATION_POST_MOVE.md](./CONFIGURATION_POST_MOVE.md)** - Setup after folder migration
- **[QUICK_START.md](./QUICK_START.md)** - Immediate actions guide

---

## 🐛 Troubleshooting

### Python: "ModuleNotFoundError"

```powershell
# Make sure venv is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Rust: "AI Service sedang mati"

```bash
# 1. Check Python service is running
curl http://localhost:8001/

# 2. Check .env file
cat backend-rust/.env
```

### Frontend: npm install errors

```powershell
# Clear cache and reinstall
npm cache clean --force
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install
```

See [CONFIGURATION_POST_MOVE.md](./CONFIGURATION_POST_MOVE.md) for detailed troubleshooting.

---

## 📈 Project Status

- ✅ **Backend Rust:** 100% Complete
- ✅ **AI Service Python:** 90% Complete (needs algorithm verification)
- ❌ **Frontend Svelte:** 5% Complete (only setup, UI not implemented)

**Overall Completion:** 63.3%

**Next Priorities:**

1. Implement frontend UI components
2. Verify hybrid filtering algorithm
3. End-to-end testing
4. Documentation completion

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👨‍💻 Author

**Fakhri** - Portfolio Project  
Demonstrating Fullstack Engineering & System Design capabilities

---

## 🙏 Acknowledgments

- Original Streamlit app for providing the hybrid filtering algorithm
- Lichess for chess games dataset
- Rust, Python, and Svelte communities

---

**Built with ❤️ using Rust, Python, and Svelte**
