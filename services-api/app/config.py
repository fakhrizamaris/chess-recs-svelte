import os
from pathlib import Path

# Base directory - works both locally and in containers
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths - use environment variables in production, local paths in development
DATA_PATH = Path(os.getenv("DATA_PATH", str(BASE_DIR / "games.csv")))

# Model paths - only files actually loaded!
CONTENT_MODEL_PATH = Path(os.getenv("CONTENT_MODEL_PATH", str(BASE_DIR / "models" / "content_based_model.pkl")))
COLLAB_MODEL_PATH = Path(os.getenv("COLLAB_MODEL_PATH", str(BASE_DIR / "models" / "collaborative_model.keras")))
COLLAB_DATA_PATH = Path(os.getenv("COLLAB_DATA_PATH", str(BASE_DIR / "models" / "collaborative_data.pkl")))

# Note: hybrid_model.pkl not needed - hybrid logic is in predict() method, not a pickled function

# Server configuration (for Cloud Run compatibility)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8001))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# CORS origins (for production)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]

# Application metadata
APP_NAME = "ChessRecs AI Service"
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Settings class for backward compatibility
class Settings:
    """Settings class for more structured configuration"""
    BASE_DIR = BASE_DIR
    DATA_PATH = DATA_PATH
    CONTENT_MODEL_PATH = CONTENT_MODEL_PATH
    COLLAB_MODEL_PATH = COLLAB_MODEL_PATH
    COLLAB_DATA_PATH = COLLAB_DATA_PATH
    HOST = HOST
    PORT = PORT
    LOG_LEVEL = LOG_LEVEL
    CORS_ORIGINS = CORS_ORIGINS
    APP_NAME = APP_NAME
    APP_VERSION = APP_VERSION
    ENVIRONMENT = ENVIRONMENT

# Singleton instance
settings = Settings()