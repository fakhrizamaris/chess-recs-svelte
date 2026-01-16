import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
import chess
from app.config import settings

def moves_to_fen(moves_str: str) -> str:
    """Convert opening moves to FEN notation for board visualization"""
    board = chess.Board()
    try:
        # Split moves and filter out move numbers
        moves_list = moves_str.split()
        for move in moves_list:
            # Skip move numbers (like "1.", "20.")
            if move.endswith('.'):
                continue
            # Skip empty strings
            if not move or move.isspace():
                continue
                
            try:
                board.push_san(move)
            except Exception as e:
                # Log error for debugging but continue
                print(f"⚠️ Failed to parse move '{move}': {e}")
                # Return current board state (partial opening)
                break
        
        fen = board.fen()
        print(f"✅ Generated FEN: {fen}")  # Debug log
        return fen
    except Exception as e:
        # If any error, return starting position
        print(f"❌ FEN error: {e}")
        return chess.Board().fen()


class ChessRecommender:
    def __init__(self):
        self.chess_data = None
        self.content_based_model = None
        self.collaborative_data = None
        self.collaborative_model = None
        self.hybrid_model = None
        self.is_ready = False
        # Cached data for performance
        self._opening_complexity_cache = None
        self._encoded_openings_cache = None
        # Lazy cache for CF predictions by rating bucket (key: rating_bucket, value: DataFrame)
        self._cf_prediction_cache = {}

    def load_resources(self):
        """Memuat semua model dan dataset ke memori sekali saja saat startup."""
        print("⏳ Loading AI Models & Data...")
        try:
            # 1. Load CSV Data
            self.chess_data = pd.read_csv(settings.DATA_PATH)
            # Preprocessing ringan (DRY: dipindahkan ke sini dari load_data app.py)
            self.chess_data = self.chess_data.drop_duplicates(subset=['id'])
            self.chess_data = self.chess_data.assign(
                opening_archetype=self.chess_data.opening_name.map(
                    lambda n: n.split(":")[0].split("|")[0].split("#")[0].strip()
                ),
                opening_moves=self.chess_data.apply(
                    lambda srs: ' '.join(srs['moves'].split(" ")[:srs['opening_ply']]), axis=1
                )
            )

            # 2. Load Models
            with open(settings.CONTENT_MODEL_PATH, 'rb') as f:
                self.content_based_model = pickle.load(f)
            
            with open(settings.COLLAB_DATA_PATH, 'rb') as f:
                self.collaborative_data = pickle.load(f)
            
            # Load Keras Model
            keras_model = tf.keras.models.load_model(settings.COLLAB_MODEL_PATH)
            self.collaborative_model = {'model': keras_model}
            
            # with open(settings.COLLAB_EXTRA_PATH, 'rb') as f:
            #     collab_data_extra = pickle.load(f)
            #     self.collaborative_model.update(collab_data_extra)
            
            # Hybrid model not needed - logic is in predict() method
            # with open(settings.HYBRID_MODEL_PATH, 'rb') as f:
            #    self.hybrid_model = pickle.load(f)
            self.hybrid_model = None  # Not used in current implementation

            # === PERFORMANCE OPTIMIZATION ===
            # 1. Pre-compute opening complexity (cache)
            print("⏳ Pre-computing opening complexity...")
            self._opening_complexity_cache = self._compute_opening_complexity()
            
            # 2. Pre-cache encoded openings
            opening_encoder = self.collaborative_data['opening_encoder']
            self._encoded_openings_cache = np.arange(len(opening_encoder.classes_))
            
            # 3. Pre-warm TensorFlow model (trigger XLA compilation)
            print("⏳ Warming up TensorFlow model...")
            self._prewarm_model()
            
            self.is_ready = True
            print("✅ AI Models Loaded & Optimized Successfully!")
        except Exception as e:
            print(f"❌ Failed to load models: {e}")
            self.is_ready = False

    def _compute_opening_complexity(self):
        """Pre-compute opening complexity scores (called once at startup)"""
        player_opening = self.collaborative_data['player_opening_matrix'].copy()
        player_data = self.collaborative_data['player_data']
        player_opening = player_opening.merge(player_data[['player_id', 'rating']], on='player_id', how='left')
        opening_avg_rating = player_opening.groupby('opening_name')['rating'].mean()
        
        if opening_avg_rating.max() - opening_avg_rating.min() > 0:
            normalized_complexity = (opening_avg_rating - opening_avg_rating.min()) / (opening_avg_rating.max() - opening_avg_rating.min())
        else:
            normalized_complexity = pd.Series(0.5, index=opening_avg_rating.index)
        return normalized_complexity

    def _prewarm_model(self):
        """Run dummy prediction to trigger XLA compilation at startup"""
        try:
            model = self.collaborative_model['model']
            player_encoder = self.collaborative_data['player_encoder']
            
            # Small dummy batch
            dummy_players = np.array([0, 0, 0])
            dummy_openings = np.array([0, 1, 2])
            
            # This triggers XLA compilation
            _ = model.predict([dummy_players, dummy_openings], batch_size=3, verbose=0)
            print("✅ Model warmed up!")
        except Exception as e:
            print(f"⚠️ Model warmup failed (non-critical): {e}")

    # --- Helper Methods (Private) ---
    def _calibrate_score(self, score, target_min=0.5, target_max=0.99):
        score_norm = (score - np.min(score)) / (np.max(score) - np.min(score))
        return score_norm * (target_max - target_min) + target_min

    def _get_win_rates(self, opening_name):
        games = self.chess_data[self.chess_data.opening_name == opening_name]
        if len(games) == 0:
            return 0.0, 0.0, 0.0
        total = len(games)
        w = len(games[games.winner == 'white']) / total
        b = len(games[games.winner == 'black']) / total
        d = len(games[games.winner == 'draw']) / total
        return w, b, d

    # --- Core Logic Methods (Refactored from app.py) ---
    
    def _get_content_based(self, favorite_openings, top_n=50):
        # ... (Logika dari get_content_based_recommendations di app.py) ...
        # Saya ringkas untuk mempersingkat jawaban, tapi Anda paste logika intinya di sini
        # Pastikan menggunakan self.content_based_model
        
        # Contoh implementasi minimal:
        sim_df = self.content_based_model['similarity_matrix']
        valid_favs = [o for o in favorite_openings if o in self.content_based_model['opening_names']]
        if not valid_favs: return pd.DataFrame()
        
        scores = sim_df[valid_favs].mean(axis=1)
        recs = pd.DataFrame({'opening_name': scores.index, 'similarity_score': scores.values})
        # ... normalisasi & sorting ...
        recs = recs.sort_values('similarity_score', ascending=False)
        return recs.head(top_n)

    def _get_collaborative(self, user_rating, top_n=50, debug=False):
        """
        Logic Collaborative Filtering - OPTIMIZED VERSION
        """
        if self.collaborative_data is None or self.collaborative_model is None:
            return pd.DataFrame(columns=['opening_name', 'score'])

        # --- Helper Inner Functions (Optimized) ---
        def softmax(x):
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum()

        def adjust_by_rating_vectorized(predictions, complexity_scores, user_rating, rating_max=3000, influence=0.3):
            """Vectorized version - much faster than loop"""
            normalized_rating = user_rating / rating_max
            
            # Align indices
            common_idx = predictions.index.intersection(complexity_scores.index)
            pred_aligned = predictions.loc[common_idx]
            comp_aligned = complexity_scores.loc[common_idx]
            
            # Vectorized calculation
            rating_factor = normalized_rating - 0.5
            complexity_factor = comp_aligned - 0.5
            adjustment = influence * rating_factor * complexity_factor * 2
            adjusted = pred_aligned * (1 + adjustment)
            
            # Normalize
            if adjusted.max() > 0:
                adjusted = adjusted / adjusted.max()
            return adjusted

        # --- Main Logic ---
        player_data = self.collaborative_data['player_data']
        player_encoder = self.collaborative_data['player_encoder']
        opening_encoder = self.collaborative_data['opening_encoder']
        model = self.collaborative_model['model']

        # === LAZY CACHING ===
        # Round rating to nearest 250 for cache bucket (reduces buckets while maintaining accuracy)
        rating_bucket = round(user_rating / 250) * 250
        rating_bucket = max(500, min(3000, rating_bucket))
        
        # Check if we have cached predictions for this rating bucket
        if rating_bucket in self._cf_prediction_cache:
            print(f"⚡ Cache HIT for rating bucket {rating_bucket}")
            cached_result = self._cf_prediction_cache[rating_bucket].copy()
            # Apply rating-specific adjustments
            final_result = adjust_by_rating_vectorized(
                pd.Series(cached_result['score'].values, index=cached_result['opening_name']),
                self._opening_complexity_cache,
                user_rating
            )
            return pd.DataFrame({
                'opening_name': final_result.index,
                'score': final_result.values
            }).sort_values('score', ascending=False).head(top_n)
        
        print(f"🔄 Cache MISS for rating bucket {rating_bucket}, computing...")

        # Cari pemain mirip (REDUCED from 10 to 5 for performance)
        rating_diff = abs(player_data['rating'] - user_rating)
        min_similar_players = 5
        rating_ranges = [50, 100, 200, 300, 400, 500, 750, 1000]
        
        similar_players_idx = None
        for r_range in rating_ranges:
            similar_players_idx = rating_diff[rating_diff <= r_range].index
            if len(similar_players_idx) >= min_similar_players:
                break
        
        if len(similar_players_idx) < min_similar_players:
            similar_players_idx = rating_diff.nsmallest(min_similar_players).index

        rating_weights = 1 / (rating_diff.loc[similar_players_idx] + 10)
        rating_weights = rating_weights / rating_weights.sum()
        
        similar_players = player_data.loc[similar_players_idx, 'player_id'].unique()
        
        # Filter valid players
        valid_similar_players = [p for p in similar_players if p in player_encoder.classes_]
        valid_player_indices = [similar_players_idx[i] for i, p in enumerate(similar_players) if p in player_encoder.classes_]
        
        if valid_player_indices:
            valid_weights = rating_weights.loc[valid_player_indices]
            valid_weights = valid_weights / valid_weights.sum()
        else:
            valid_weights = None

        if len(valid_similar_players) == 0:
            # Fallback popularity - USE CACHED COMPLEXITY
            opening_counts = self.collaborative_data['player_opening_matrix'].groupby('opening_name').size()
            adjusted_counts = adjust_by_rating_vectorized(opening_counts, self._opening_complexity_cache, user_rating)
            normalized_counts = adjusted_counts / adjusted_counts.max() if adjusted_counts.max() > 0 else adjusted_counts
            
            return pd.DataFrame({
                'opening_name': adjusted_counts.index,
                'score': normalized_counts.values
            }).sort_values('score', ascending=False).head(top_n)

        else:
            # Predict with Model - USE CACHED encoded_openings
            encoded_players = player_encoder.transform(valid_similar_players)
            encoded_openings = self._encoded_openings_cache  # CACHED!
            
            players_batch = np.repeat(encoded_players, len(encoded_openings))
            openings_batch = np.tile(encoded_openings, len(encoded_players))
            
            predictions = model.predict(
                [players_batch, openings_batch],
                batch_size=1024,
                verbose=0
            ).flatten()
            
            predictions_matrix = predictions.reshape(len(encoded_players), -1)
            
            if valid_weights is not None:
                weighted_predictions = np.zeros(predictions_matrix.shape[1])
                for i in range(len(valid_similar_players)):
                    if i < len(valid_weights): # Safety check
                        weighted_predictions += predictions_matrix[i] * valid_weights.iloc[i]
                    else:
                        weighted_predictions += predictions_matrix[i] * (1/len(valid_similar_players))
                avg_predictions = weighted_predictions
            else:
                avg_predictions = np.mean(predictions_matrix, axis=0)

            temperature = 2.0
            softmax_predictions = softmax(avg_predictions / temperature)
            
            # Store raw predictions in cache (before rating adjustment)
            # This allows reuse for nearby ratings
            raw_predictions_df = pd.DataFrame({
                'opening_name': opening_encoder.classes_,
                'score': softmax_predictions
            })
            self._cf_prediction_cache[rating_bucket] = raw_predictions_df
            print(f"✅ Cached predictions for rating bucket {rating_bucket}")
            
            # USE CACHED COMPLEXITY & VECTORIZED FUNCTION
            final_predictions = adjust_by_rating_vectorized(
                pd.Series(softmax_predictions, index=opening_encoder.classes_),
                self._opening_complexity_cache,
                user_rating
            )
            
            return pd.DataFrame({
                'opening_name': final_predictions.index,
                'score': final_predictions.values
            }).sort_values('score', ascending=False).head(top_n)

    def predict(self, user_rating: int, favorite_openings: list, alpha: float, top_n: int = 5):
        if not self.is_ready:
            raise RuntimeError("Model is not loaded")

        # 1. Get CB & CF Recs
        cb_recs = self._get_content_based(favorite_openings)
        cf_recs = self._get_collaborative(user_rating)

        # 2. Merge & Hybrid Logic (Sesuai app.py)
        # Rename columns
        if not cb_recs.empty:
            cb_recs = cb_recs.rename(columns={'similarity_score': 'cb_score'})
        if not cf_recs.empty:
            cf_recs = cf_recs.rename(columns={'score': 'cf_score'})

        # Merge
        if cb_recs.empty and cf_recs.empty:
            return []
        elif cb_recs.empty:
            hybrid = cf_recs
            hybrid['cb_score'] = 0
            hybrid['hybrid_score'] = (1 - alpha) * hybrid['cf_score']
        elif cf_recs.empty:
            hybrid = cb_recs
            hybrid['cf_score'] = 0
            hybrid['hybrid_score'] = alpha * hybrid['cb_score']
        else:
            hybrid = pd.merge(cb_recs, cf_recs, on='opening_name', how='outer').fillna(0)
            
            # === FIX: Percentile-based normalization for fair comparison ===
            # This ensures both CB and CF have the same distribution shape
            # so that alpha=0.5 is truly balanced
            
            for col in ['cb_score', 'cf_score']:
                if hybrid[col].max() > 0:
                    # Convert to percentile ranks (0-1)
                    # This makes distributions comparable regardless of original scale
                    ranked = hybrid[col].rank(method='average', pct=True)
                    # Scale to [0.1, 1.0] to ensure no zeros
                    hybrid[col] = ranked * 0.9 + 0.1
                else:
                    hybrid[col] = 0.1
            
            # Hitung hybrid score dengan bobot alpha
            # alpha=1.0 → 100% CB, alpha=0.0 → 100% CF, alpha=0.5 → 50/50
            hybrid['hybrid_score'] = (alpha * hybrid['cb_score']) + ((1 - alpha) * hybrid['cf_score'])
            
            # Normalisasi ulang hybrid_score ke [0, 1] agar maksimum 100%
            hs_max = hybrid['hybrid_score'].max()
            hs_min = hybrid['hybrid_score'].min()
            if hs_max > hs_min:
                hybrid['hybrid_score'] = (hybrid['hybrid_score'] - hs_min) / (hs_max - hs_min)

        # 3. Filter & Sort
        hybrid = hybrid[~hybrid.opening_name.isin(favorite_openings)]
        hybrid = hybrid.sort_values('hybrid_score', ascending=False).head(top_n)

        # 4. Format Output sesuai Schema
        results = []
        for _, row in hybrid.iterrows():
            name = row['opening_name']
            # Ambil data tambahan dari self.chess_data
            meta = self.chess_data[self.chess_data.opening_name == name].iloc[0]
            w, b, d = self._get_win_rates(name)
            
            results.append({
                "opening_name": name,
                "archetype": meta['opening_archetype'],
                "moves": meta['opening_moves'],
                "fen": moves_to_fen(meta['opening_moves']),  # ← ADD FEN
                "hybrid_score": float(row['hybrid_score']),
                "cb_score": float(row['cb_score']),
                "cf_score": float(row['cf_score']),
                "win_rate_white": w,
                "win_rate_black": b,
                "win_rate_draw": d
            })
            
        return results

# Singleton Instance
recommender = ChessRecommender()