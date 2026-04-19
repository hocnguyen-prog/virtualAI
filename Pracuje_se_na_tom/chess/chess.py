import tkinter as tk
from tkinter import messagebox
import chess

class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Šachy - Dvouhračová aplikace")
        self.root.resizable(False, False)
        
        self.board = chess.Board()          # šachovnice s pravidly
        self.selected_square = None
        self.square_size = 70
        self.canvas_size = self.square_size * 8
        
        # Canvas pro šachovnici
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack(pady=10)
        
        # Popisky
        self.status_label = tk.Label(self.root, text="Bílý na tahu", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)
        
        # Tlačítka
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Nová hra", command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Zpět tah", command=self.undo_move).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Ukončit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Bind kliknutí myši
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Slovník unicode figur (hezké obrázky)
        self.pieces = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        self.draw_board()
        self.root.mainloop()
    
    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]   # světlá a tmavá pole
        
        for rank in range(8):
            for file in range(8):
                x1 = file * self.square_size
                y1 = rank * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                color = colors[(file + rank) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Souřadnice (a-h, 8-1)
                if file == 0:
                    self.canvas.create_text(x1+5, y1+10, text=str(8-rank), fill="black", font=("Arial", 10))
                if rank == 7:
                    self.canvas.create_text(x2-10, y2-10, text=chr(97+file), fill="black", font=("Arial", 10))
        
        # Vykreslení figur
        for square in range(64):
            piece = self.board.piece_at(square)
            if piece:
                symbol = self.pieces.get(piece.symbol(), "")
                file = chess.square_file(square)
                rank = 7 - chess.square_rank(square)   # obráceně pro canvas
                
                x = file * self.square_size + self.square_size // 2
                y = rank * self.square_size + self.square_size // 2
                
                self.canvas.create_text(x, y, text=symbol, font=("Arial", 50), fill="black")
        
        # Zvýraznění vybraného pole
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = 7 - chess.square_rank(self.selected_square)
            x1 = file * self.square_size
            y1 = rank * self.square_size
            self.canvas.create_rectangle(x1, y1, x1+self.square_size, y1+self.square_size, 
                                       outline="#00ff00", width=4)
        
        # Aktualizace stavu
        if self.board.is_checkmate():
            winner = "Černý" if self.board.turn == chess.WHITE else "Bílý"
            self.status_label.config(text=f"ŠACHMAT! Vyhrál {winner} 🎉")
        elif self.board.is_stalemate():
            self.status_label.config(text="Pat – remíza")
        elif self.board.is_check():
            self.status_label.config(text="Šach! " + ("Bílý" if self.board.turn else "Černý") + " na tahu")
        else:
            player = "Bílý" if self.board.turn else "Černý"
            self.status_label.config(text=f"{player} na tahu")
    
    def handle_click(self, event):
        if self.board.is_game_over():
            return
            
        file = event.x // self.square_size
        rank = 7 - (event.y // self.square_size)   # převod na šachovou souřadnici
        square = chess.square(file, rank)
        
        if self.selected_square is None:
            # Vybrat figuru
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
                self.selected_square = square
                self.draw_board()
        else:
            # Zkusit tah
            move = chess.Move(self.selected_square, square)
            
            # Promoce dámy (automaticky)
            if self.board.piece_at(self.selected_square).piece_type == chess.PAWN:
                if (self.board.turn == chess.WHITE and rank == 7) or (self.board.turn == chess.BLACK and rank == 0):
                    move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.draw_board()
            else:
                # Možná klikl na jinou vlastní figuru
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn:
                    self.selected_square = square
                    self.draw_board()
                else:
                    self.selected_square = None
                    self.draw_board()
    
    def new_game(self):
        self.board = chess.Board()
        self.selected_square = None
        self.draw_board()
    
    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.selected_square = None
            self.draw_board()

# Spuštění aplikace
if __name__ == "__main__":
    ChessApp()