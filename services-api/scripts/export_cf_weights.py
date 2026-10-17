"""Ekspor bobot model collaborative (Keras) ke .npz agar inferensi bisa jalan tanpa TensorFlow.

Model-nya matrix factorization sederhana:
    sigmoid(dot(player_emb, opening_emb) + player_bias + opening_bias)

Jalankan sekali di mesin yang punya TensorFlow (bukan di VPS):
    pip install tensorflow-cpu
    python scripts/export_cf_weights.py
"""
from pathlib import Path

import numpy as np
import tensorflow as tf

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
SRC = MODELS_DIR / "collaborative_model.keras"
DST = MODELS_DIR / "collaborative_weights.npz"

model = tf.keras.models.load_model(SRC)

np.savez_compressed(
    DST,
    player_emb=model.get_layer("player_embedding").get_weights()[0].astype(np.float32),
    opening_emb=model.get_layer("opening_embedding").get_weights()[0].astype(np.float32),
    player_bias=model.get_layer("player_bias").get_weights()[0].reshape(-1).astype(np.float32),
    opening_bias=model.get_layer("opening_bias").get_weights()[0].reshape(-1).astype(np.float32),
)
print(f"Tersimpan: {DST} ({DST.stat().st_size / 1024:.0f} KB)")
