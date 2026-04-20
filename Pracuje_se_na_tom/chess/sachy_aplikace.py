import tkinter as tk
from tkinter import messagebox
import chess   # ← musí být python-chess knihovna, ne tvůj soubor

class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Šachy - Dvouhračová aplikace")
        self.root.resizable(False, False)
        
        self.board = chess.Board()          # teď by mělo fungovat
        self.selected_square = None
        self.square_size = 70
        
        self.canvas = tk.Canvas(self.root, width=560, height=560)
        self.canvas.pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="Bílý na tahu", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Nová hra", command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Zpět tah", command=self.undo_move).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Ukončit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.pieces = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        self.draw_board()
        self.root.mainloop()
    
    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]
        
        for rank in range(8):
            for file in range(8):
                x1 = file * 70
                y1 = rank * 70
                color = colors[(file + rank) % 2]
                self.canvas.create_rectangle(x1, y1, x1+70, y1+70, fill=color, outline="")
                
                # Popisky
                if file == 0:
                    self.canvas.create_text(x1+8, y1+8, text=str(8-rank), font=("Arial", 10))
                if rank == 7:
                    self.canvas.create_text(x1+62, y1+62, text=chr(97+file), font=("Arial", 10))
        
        # Figurky
        for sq in range(64):
            piece = self.board.piece_at(sq)
            if piece:
                symbol = self.pieces.get(piece.symbol(), "")
                file = chess.square_file(sq)
                rank = 7 - chess.square_rank(sq)
                x = file * 70 + 35
                y = rank * 70 + 35
                self.canvas.create_text(x, y, text=symbol, font=("Arial", 48))
        
        # Zvýraznění vybraného pole
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = 7 - chess.square_rank(self.selected_square)
            self.canvas.create_rectangle(file*70, rank*70, file*70+70, rank*70+70, 
                                       outline="#00ff00", width=5)
        
        # Stav hry
        if self.board.is_checkmate():
            winner = "Černý" if self.board.turn == chess.WHITE else "Bílý"
            self.status_label.config(text=f"ŠACHMAT! Vyhrál {winner} 🎉")
        elif self.board.is_check():
            self.status_label.config(text="Šach! " + ("Bílý" if self.board.turn else "Černý") + " na tahu")
        else:
            self.status_label.config(text=("Bílý" if self.board.turn else "Černý") + " na tahu")
    
    def handle_click(self, event):
        if self.board.is_game_over():
            return
        file = event.x // 70
        rank = 7 - (event.y // 70)
        square = chess.square(file, rank)
        
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.draw_board()
        else:
            move = chess.Move(self.selected_square, square)
            # Automatická promoce na dámu
            if (self.board.piece_at(self.selected_square).piece_type == chess.PAWN and
                ((self.board.turn == chess.WHITE and rank == 7) or 
                 (self.board.turn == chess.BLACK and rank == 0))):
                move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.draw_board()
            else:
                # Klik na jinou figuru stejné barvy
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn:
                    self.selected_square = square
                else:
                    self.selected_square = None
                self.draw_board()
    
    def new_game(self):
        self.board = chess.Board()
        self.selected_square = None
        self.draw_board()
    
    def undo_move(self):
        if self.board.move_stack:
            self.board.pop()
            self.selected_square = None
            self.draw_board()

if __name__ == "__main__":
    ChessApp()