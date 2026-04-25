import tkinter as tk
from tkinter import messagebox, simpledialog
import chess
import time

class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Šachy - Dvouhračová hra")
        self.root.resizable(False, False)

        self.board = chess.Board()
        self.selected_square = None
        self.square_size = 70
        self.highlighted_moves = []   # pro zvýraznění legálních tahů
        self.last_move = None         # poslední tah pro zvýraznění
        self.flip_board = False       # otočení desky
        self.dragging = None          # pro drag & drop
        self.drag_piece = None         # figurka při drag
        
        # Časovač (v sekundách)
        self.white_time = 600  # 10 minut
        self.black_time = 600
        self.timer_running = False
        self.last_timer_update = 0

        # Hlavní rámec
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Levý panel - zajatá černá
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="n")
        
        tk.Label(left_frame, text="Zajaté černé", font=("Arial", 10)).pack()
        self.captured_black_frame = tk.Frame(left_frame, bg="#f0d9b5", height=100)
        self.captured_black_frame.pack(fill="x", pady=(0,10))
        self.captured_black_label = tk.Label(self.captured_black_frame, text="", font=("Arial", 16), bg="#f0d9b5")
        self.captured_black_label.pack(pady=5)

        # Canvas pro šachovnici
        self.canvas = tk.Canvas(main_frame, width=560, height=560, bg="#222")
        self.canvas.grid(row=0, column=1)

        # Levý panel - zajatá bílá
        left2_frame = tk.Frame(main_frame)
        left2_frame.grid(row=0, column=2, sticky="n")
        
        tk.Label(left2_frame, text="Zajaté bílé", font=("Arial", 10)).pack()
        self.captured_white_frame = tk.Frame(left2_frame, bg="#b58863", height=100)
        self.captured_white_frame.pack(fill="x", pady=(10,0))
        self.captured_white_label = tk.Label(self.captured_white_frame, text="", font=("Arial", 16), bg="#b58863")
        self.captured_white_label.pack(pady=5)

        # Boční panel (historie + info)
        side_frame = tk.Frame(main_frame)
        side_frame.grid(row=0, column=3, padx=15, sticky="n")

        tk.Label(side_frame, text="Historie tahů", font=("Arial", 12, "bold")).pack(anchor="w")
        self.history_text = tk.Text(side_frame, width=25, height=20, font=("Consolas", 10), state="disabled")
        self.history_text.pack(pady=5)

        # Časovač
        self.timer_frame = tk.Frame(side_frame, bg="#333", bd=2, relief="raised")
        self.timer_frame.pack(pady=5, fill="x")
        self.white_timer_label = tk.Label(self.timer_frame, text="Bílý: 10:00", font=("Arial", 14, "bold"), bg="#333", fg="white")
        self.white_timer_label.pack()
        self.black_timer_label = tk.Label(self.timer_frame, text="Černý: 10:00", font=("Arial", 14, "bold"), bg="#333", fg="white")
        self.black_timer_label.pack()

        self.status_label = tk.Label(side_frame, text="Bílý na tahu", font=("Arial", 14, "bold"), fg="#00cc00")
        self.status_label.pack(pady=10)

        # Tlačítka
        btn_frame = tk.Frame(side_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Nová hra", command=self.new_game, width=12).pack(pady=2)
        tk.Button(btn_frame, text="Otočit desku", command=self.flip_board_func, width=12).pack(pady=2)
        tk.Button(btn_frame, text="Zpět tah", command=self.undo_move, width=12).pack(pady=2)
        tk.Button(btn_frame, text="Kopírovat FEN", command=self.copy_fen, width=12).pack(pady=2)
        tk.Button(btn_frame, text="Načíst FEN", command=self.load_fen, width=12).pack(pady=2)
        tk.Button(btn_frame, text="Ukončit", command=self.root.quit, width=12).pack(pady=2)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)

        self.pieces = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }

        self.draw_board()
        self.update_timer()
        self.root.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]   # klasické šachovnicové barvy

        for rank in range(8):
            for file in range(8):
                # Otočení desky podle nastavení
                display_file = 7 - file if self.flip_board else file
                display_rank = rank if self.flip_board else 7 - rank
                
                x1 = file * self.square_size
                y1 = rank * self.square_size
                color = colors[(file + rank) % 2]
                self.canvas.create_rectangle(x1, y1, x1 + 70, y1 + 70, fill=color, outline="")

                # Souřadnice
                if file == 0:
                    rank_label = str(rank + 1) if self.flip_board else str(8 - rank)
                    self.canvas.create_text(x1 + 10, y1 + 10, text=rank_label,
                                            font=("Arial", 10, "bold"), fill="#222")
                if rank == 7:
                    file_label = chr(97 + (7 - file)) if self.flip_board else chr(97 + file)
                    self.canvas.create_text(x1 + 60, y1 + 60, text=file_label,
                                            font=("Arial", 10, "bold"), fill="#222")

        # Zvýraznění posledního tahu (žluté)
        if self.last_move:
            from_sq = self.last_move.from_square
            to_sq = self.last_move.to_square
            for sq in [from_sq, to_sq]:
                file = chess.square_file(sq)
                rank = chess.square_rank(sq)
                if self.flip_board:
                    file = 7 - file
                    rank = 7 - rank
                else:
                    rank = 7 - rank
                self.canvas.create_rectangle(file*70+2, rank*70+2, file*70+68, rank*70+68,
                                             outline="#ffdd00", width=4)

        # Zvýraznění legálních tahů (zelené kruhy)
        for move in self.highlighted_moves:
            file = chess.square_file(move.to_square)
            rank = chess.square_rank(move.to_square)
            if self.flip_board:
                file = 7 - file
                rank = 7 - rank
            else:
                rank = 7 - rank
            x = file * 70 + 35
            y = rank * 70 + 35
            self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12, outline="#00ff44", width=4)

        # Figurky
        for sq in range(64):
            piece = self.board.piece_at(sq)
            if piece:
                symbol = self.pieces.get(piece.symbol(), "")
                file = chess.square_file(sq)
                rank = chess.square_rank(sq)
                if self.flip_board:
                    file = 7 - file
                    rank = 7 - rank
                else:
                    rank = 7 - rank
                x = file * 70 + 35
                y = rank * 70 + 35

                # Stín pro lepší čitelnost
                self.canvas.create_text(x + 2, y + 2, text=symbol, font=("Arial", 48), fill="#111")
                # Bílé figurky - černá barva, černé figurky - tmavší barva
                piece_color = "#000" if piece.color == chess.WHITE else "#333"
                self.canvas.create_text(x, y, text=symbol, font=("Arial", 48), fill=piece_color)

        # Zvýraznění vybraného pole
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = chess.square_rank(self.selected_square)
            if self.flip_board:
                file = 7 - file
                rank = 7 - rank
            else:
                rank = 7 - rank
            self.canvas.create_rectangle(file*70, rank*70, file*70+70, rank*70+70,
                                         outline="#00ff00", width=6)

        self.update_status()
        self.update_history()
        self.update_captured()

    def update_status(self):
        if self.board.is_checkmate():
            winner = "Černý" if self.board.turn == chess.WHITE else "Bílý"
            self.status_label.config(text=f"ŠACHMAT! Vyhrál {winner} 🎉", fg="#ff4444")
        elif self.board.is_stalemate():
            self.status_label.config(text="Pat! Remíza", fg="#ffaa00")
        elif self.board.is_insufficient_material():
            self.status_label.config(text="Nedostatek materiálu – remíza", fg="#ffaa00")
        elif self.board.is_check():
            player = "Bílý" if self.board.turn == chess.WHITE else "Černý"
            self.status_label.config(text=f"Šach! {player} na tahu", fg="#ff4444")
        else:
            player = "Bílý" if self.board.turn == chess.WHITE else "Černý"
            self.status_label.config(text=f"{player} na tahu", fg="#00cc00")

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        for i, move in enumerate(self.board.move_stack, 1):
            # SAN notace
            san = self.board.san(move)
            if i % 2 == 1:
                self.history_text.insert(tk.END, f"{(i+1)//2:2d}. ")
            self.history_text.insert(tk.END, f"{san:6s}")
            if i % 2 == 0:
                self.history_text.insert(tk.END, "\n")
        self.history_text.config(state="disabled")

    def highlight_legal_moves(self, square):
        self.highlighted_moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                self.highlighted_moves.append(move)
        self.draw_board()

    def flip_board_func(self):
        """Otočení desky"""
        self.flip_board = not self.flip_board
        self.draw_board()

    def update_timer(self):
        """Aktualizace časovače"""
        if self.board.move_stack and not self.board.is_game_over():
            current_time = time.time()
            if self.last_timer_update == 0:
                self.last_timer_update = current_time
            
            elapsed = current_time - self.last_timer_update
            self.last_timer_update = current_time
            
            if self.board.turn == chess.WHITE:
                self.white_time = max(0, self.white_time - int(elapsed))
            else:
                self.black_time = max(0, self.black_time - int(elapsed))
        else:
            self.last_timer_update = time.time()
        
        # Formátování času
        w_min, w_sec = divmod(self.white_time, 60)
        b_min, b_sec = divmod(self.black_time, 60)
        self.white_timer_label.config(text=f"Bílý: {w_min:02d}:{w_sec:02d}")
        self.black_timer_label.config(text=f"Černý: {b_min:02d}:{b_sec:02d}")
        
        # Zvýraznění aktuálního hráče
        if self.board.turn == chess.WHITE:
            self.white_timer_label.config(fg="#00ff00")
            self.black_timer_label.config(fg="white")
        else:
            self.white_timer_label.config(fg="white")
            self.black_timer_label.config(fg="#00ff00")
        
        # Kontrola vypršení času
        if self.white_time <= 0:
            self.status_label.config(text="Čas! Vyhrál Černý ⏰", fg="#ff4444")
            return
        if self.black_time <= 0:
            self.status_label.config(text="Čas! Vyhrál Bílý ⏰", fg="#ff4444")
            return
        
        self.root.after(1000, self.update_timer)

    def update_captured(self):
        """Aktualizace zobrazení zajatých figurek"""
        captured_white = []
        captured_black = []
        
        # Spočítáme zajatky z historie tahů
        for move in self.board.move_stack:
            if move.capture:
                captured = self.board.piece_at(move.to_square)
                if captured:
                    if captured.color == chess.WHITE:
                        captured_white.append(captured.symbol())
                    else:
                        captured_black.append(captured.symbol())
        
        # Seřazení podle hodnoty
        piece_order = ['Q', 'R', 'B', 'N', 'P']
        captured_white.sort(key=lambda x: piece_order.index(x.lower()) if x.lower() in piece_order else 5)
        captured_black.sort(key=lambda x: piece_order.index(x.lower()) if x.lower() in piece_order else 5)
        
        self.captured_white_label.config(text=" ".join(captured_white))
        self.captured_black_label.config(text=" ".join(captured_black))

    def handle_click(self, event):
        if self.board.is_game_over():
            return

        file = event.x // 70
        rank = event.y // 70
        if not (0 <= file < 8 and 0 <= rank < 8):
            return

        # Otočení souřadnic
        if self.flip_board:
            file = 7 - file
            rank = 7 - rank
        else:
            rank = 7 - rank

        square = chess.square(file, rank)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.highlight_legal_moves(square)
        else:
            self.try_make_move(self.selected_square, square)

    def handle_drag(self, event):
        """Drag & drop - přetahování figurek"""
        if self.selected_square is None:
            return
        
        file = event.x // 70
        rank = event.y // 70
        if not (0 <= file < 8 and 0 <= rank < 8):
            return
        
        # Překreslení s přetahovanou figurkou
        self.draw_board()
        
        # Zobrazit figurku pod myší
        piece = self.board.piece_at(self.selected_square)
        if piece:
            symbol = self.pieces.get(piece.symbol(), "")
            self.canvas.create_text(event.x, event.y, text=symbol, font=("Arial", 48), tags="drag")

    def handle_release(self, event):
        if self.selected_square is None or self.board.is_game_over():
            return

        file = event.x // 70
        rank = event.y // 70
        if not (0 <= file < 8 and 0 <= rank < 8):
            self.cancel_selection()
            return

        # Otočení souřadnic
        if self.flip_board:
            file = 7 - file
            rank = 7 - rank
        else:
            rank = 7 - rank

        target_square = chess.square(file, rank)
        self.try_make_move(self.selected_square, target_square)

    def try_make_move(self, from_sq, to_sq):
        move = chess.Move(from_sq, to_sq)

        # Automatická detekce promoce
        piece = self.board.piece_at(from_sq)
        if (piece and piece.piece_type == chess.PAWN and
            ((self.board.turn == chess.WHITE and chess.square_rank(to_sq) == 7) or
             (self.board.turn == chess.BLACK and chess.square_rank(to_sq) == 0))):

            promotion = self.ask_promotion()
            if promotion is None:   # uživatel zrušil
                self.cancel_selection()
                return
            move = chess.Move(from_sq, to_sq, promotion=promotion)

        if move in self.board.legal_moves:
            self.last_move = move  # Uložení posledního tahu
            self.board.push(move)
            self.cancel_selection()
            self.draw_board()
        else:
            # Klik na jinou vlastní figuru → přesun výběru
            new_piece = self.board.piece_at(to_sq)
            if new_piece and new_piece.color == self.board.turn:
                self.selected_square = to_sq
                self.highlight_legal_moves(to_sq)
            else:
                self.cancel_selection()

    def ask_promotion(self):
        """Dialog pro výběr figury při promoci"""
        choices = {"Dáma": chess.QUEEN, "Věž": chess.ROOK,
                   "Střelec": chess.BISHOP, "Kůň": chess.KNIGHT}
        
        choice = simpledialog.askstring("Promoce pěšce", 
                                        "Na jakou figuru chceš promoci?",
                                        initialvalue="Dáma")
        if choice and choice.lower() in ["dáma", "queen", "q"]:
            return chess.QUEEN
        elif choice and choice.lower() in ["věž", "rook", "r"]:
            return chess.ROOK
        elif choice and choice.lower() in ["střelec", "bishop", "b"]:
            return chess.BISHOP
        elif choice and choice.lower() in ["kůň", "knight", "n"]:
            return chess.KNIGHT
        return None   # zrušeno

    def cancel_selection(self):
        self.selected_square = None
        self.highlighted_moves = []
        self.draw_board()

    def new_game(self):
        if messagebox.askyesno("Nová hra", "Opravdu začít novou hru?"):
            self.board = chess.Board()
            self.selected_square = None
            self.highlighted_moves = []
            self.last_move = None
            self.white_time = 600
            self.black_time = 600
            self.last_timer_update = 0
            self.draw_board()

    def undo_move(self):
        if self.board.move_stack:
            self.board.pop()
            # Odebrat i poslední tah
            if self.board.move_stack:
                self.last_move = self.board.move_stack[-1] if self.board.move_stack else None
            else:
                self.last_move = None
            self.selected_square = None
            self.highlighted_moves = []
            self.draw_board()
        else:
            messagebox.showinfo("Undo", "Žádný tah k vrácení.")

    def copy_fen(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.board.fen())
        messagebox.showinfo("FEN", "Aktuální FEN byl zkopírován do schránky.")

    def load_fen(self):
        fen = simpledialog.askstring("Načíst FEN", "Zadej FEN pozici:")
        if fen:
            try:
                self.board = chess.Board(fen)
                self.selected_square = None
                self.highlighted_moves = []
                self.last_move = None
                self.draw_board()
            except Exception as e:
                messagebox.showerror("Chyba", f"Neplatný FEN:\n{str(e)}")

if __name__ == "__main__":
    ChessApp()