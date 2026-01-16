import chess

def moves_to_fen(moves_str: str) -> str:
    """Debug version of moves_to_fen"""
    board = chess.Board()
    print(f"DEBUG: Processing moves: '{moves_str}'")
    try:
        moves_list = moves_str.split()
        for idx, move in enumerate(moves_list):
            if move and not any(char.isdigit() for char in move if char != '.'):
                try:
                    board.push_san(move)
                except Exception as e:
                    print(f"DEBUG: Failed to push move '{move}' at index {idx}: {e}")
                    # Print valid moves at this point
                    print(f"Legal moves: {[m.uci() for m in board.legal_moves]}")
                    break
        return board.fen()
    except Exception as e:
        print(f"DEBUG: Global error: {e}")
        return chess.Board().fen()

# Test case dari output sebelumnya
test_moves = "e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6 Be3 e5 Nb3"
fen = moves_to_fen(test_moves)
print(f"Result FEN: {fen}")
