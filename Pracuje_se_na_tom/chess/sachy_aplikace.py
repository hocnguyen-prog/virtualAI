import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import chess
import chess.pgn
import chess.engine
import pygame
import time
import threading
import os
from datetime import datetime

class ChessApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Šachy Pro - Profesionální Šachová Aplikace")
        self.root.geometry("1150x780")
        self.root.resizable(True, True)

        # Inicializace pygame pro zvuky
        try:
            pygame.mixer.init()
        except:
            pass

        self.board = chess.Board()
        self.square_size = 80
        self.selected_square = None
        self.highlighted_moves = []
        self.last_move = None
        self.flip_board = False
        self.game_mode = "vs_ai"        # AUTOMATICKY NASTAVENO: Hráč vs Bot
        self.ai_difficulty = 5          # Hloubka výpočtu (1-20)
        self.ai_is_thinking = False     # Zámek desky během tahu AI

        # Nastavení cesty na lokální složku (hledá stockfish.exe vedle skriptu)
        self.engine_path = os.path.join(os.path.dirname(__file__), "stockfish.exe") if __file__ else "stockfish.exe"

        self.white_remaining = 600
        self.black_remaining = 600
        self.increment = 5
        self.last_update = None
        self.game_over = False
        self.current_theme = "Klasický"

        self.themes = {
            "Klasický": (("#f0d9b5", "#b58863"), "#1e1e1e"),
            "Tmavý": (("#a8a8a8", "#5e5e5e"), "#0f0f0f"),
            "Modrý": (("#b8d8ff", "#4a8cff"), "#0a1f3d"),
            "Zelený": (("#a8d8a8", "#3a8a3a"), "#0f2a0f"),
        }

        self.pieces_dict = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }

        self._create_full_ui()
        self.reset_game_state()
        self.draw_board()
        self.update_timer()
        
        self.root.mainloop()

    def _create_full_ui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Soubor", menu=filemenu)
        filemenu.add_command(label="Nová hra", command=self.new_game)
        filemenu.add_command(label="Uložit jako PGN", command=self.save_pgn)
        filemenu.add_command(label="Načíst PGN", command=self.load_pgn)
        filemenu.add_separator()
        filemenu.add_command(label="Konec", command=self.root.quit)

        gamemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hra", menu=gamemenu)
        gamemenu.add_command(label="Hráč vs Hráč", command=lambda: self.set_mode("pvp"))
        gamemenu.add_command(label="Hráč vs Počítač", command=lambda: self.set_mode("vs_ai"))
        gamemenu.add_separator()
        gamemenu.add_command(label="Vzdát se", command=self.resign)

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(main)
        left.grid(row=0, column=0, sticky="ns")
        tk.Label(left, text="Sebrané černé", font=("Arial", 11, "bold")).pack()
        self.black_captured_lbl = tk.Label(left, font=("Arial", 20), width=10, height=4, bg="#333", fg="white", wraplength=120)
        self.black_captured_lbl.pack(pady=8)

        self.canvas = tk.Canvas(main, width=640, height=640, bg="#111", highlightthickness=3)
        self.canvas.grid(row=0, column=1, padx=15)

        right = tk.Frame(main)
        right.grid(row=0, column=2, sticky="ns")
        tk.Label(right, text="Sebrané bílé", font=("Arial", 11, "bold")).pack()
        self.white_captured_lbl = tk.Label(right, font=("Arial", 20), width=10, height=4, bg="#ddd", fg="#111", wraplength=120)
        self.white_captured_lbl.pack(pady=8)

        side = tk.Frame(main)
        side.grid(row=0, column=3, sticky="n", padx=10)

        tf = tk.LabelFrame(side, text="Časovač", padx=10, pady=8)
        tf.pack(fill="x")
        self.white_time_lbl = tk.Label(tf, text="Bílý: 10:00", font=("Consolas", 18, "bold"), fg="#22aa22")
        self.white_time_lbl.pack()
        self.black_time_lbl = tk.Label(tf, text="Černý: 10:00", font=("Consolas", 18, "bold"), fg="#aa2222")
        self.black_time_lbl.pack()

        self.status_lbl = tk.Label(side, text="Bílý na tahu", font=("Arial", 14, "bold"), fg="#00aa55", pady=15)
        self.status_lbl.pack()

        tk.Label(side, text="Historie tahů", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,0))
        self.history_text = tk.Text(side, width=29, height=14, font=("Consolas", 10), state="disabled", bg="#1c1c1c", fg="#eee")
        self.history_text.pack()

        bf = tk.Frame(side)
        bf.pack(pady=15)
        for text, cmd in [
            ("Nová hra", self.new_game),
            ("Zpět tah", self.undo_move),
            ("Otočit desku", self.flip_board_func),
            ("Nastavení AI", self.ai_settings),
            ("Uložit PGN", self.save_pgn)
        ]:
            tk.Button(bf, text=text, command=cmd, width=20).pack(pady=3)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)

    def draw_board(self):
        self.canvas.delete("all")
        light, dark = self.themes[self.current_theme][0]

        for rank in range(8):
            for file in range(8):
                display_file = 7 - file if self.flip_board else file
                display_rank = rank if self.flip_board else 7 - rank
                
                x1 = display_file * self.square_size
                y1 = (7 - display_rank) * self.square_size
                
                color = light if (rank + file) % 2 == 0 else dark
                self.canvas.create_rectangle(x1, y1, x1+self.square_size, y1+self.square_size, fill=color, outline="")

                if display_file == 0:
                    num = str(display_rank + 1)
                    lbl_col = dark if color == light else light
                    self.canvas.create_text(x1+10, y1+12, text=num, font=("Arial", 10, "bold"), fill=lbl_col)
                
                if display_rank == 0:
                    let = chr(97 + display_file)
                    lbl_col = dark if color == light else light
                    self.canvas.create_text(x1+self.square_size-10, y1+self.square_size-12, text=let, font=("Arial", 10, "bold"), fill=lbl_col)

        if self.last_move:
            for sq in (self.last_move.from_square, self.last_move.to_square):
                self._highlight_square(sq, "#ffee00", 4)

        if self.selected_square is not None:
            self._highlight_square(self.selected_square, "#00ff00", 4)

        for move in self.highlighted_moves:
            self._highlight_square(move.to_square, "#22ff55", circle=True)

        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                self._draw_piece(sq, piece)

        self.update_captured()
        self.update_history()
        self.update_status()

    def _highlight_square(self, square, color, width=4, circle=False):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if self.flip_board:
            file = 7 - file
            rank = 7 - rank
        x = file * self.square_size
        y = (7 - rank) * self.square_size

        if circle:
            cx = x + self.square_size // 2
            cy = y + self.square_size // 2
            self.canvas.create_oval(cx-12, cy-12, cx+12, cy+12, fill=color, outline="")
        else:
            self.canvas.create_rectangle(x+2, y+2, x+self.square_size-2, y+self.square_size-2, outline=color, width=width)

    def _draw_piece(self, sq, piece):
        symbol = self.pieces_dict.get(piece.symbol(), "")
        file = chess.square_file(sq)
        rank = chess.square_rank(sq)
        if self.flip_board:
            file = 7 - file
            rank = 7 - rank
        x = file * self.square_size + self.square_size // 2
        y = (7 - rank) * self.square_size + self.square_size // 2

        self.canvas.create_text(x+2, y+2, text=symbol, font=("Arial", 48), fill="#111111")
        col = "#ffffff" if piece.color == chess.WHITE else "#222222"
        self.canvas.create_text(x, y, text=symbol, font=("Arial", 48), fill=col)

    def handle_click(self, event):
        if self.game_over or self.ai_is_thinking: return
        square = self._coord_to_square(event.x, event.y)
        if square is None: return

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.highlighted_moves = [m for m in self.board.legal_moves if m.from_square == square]
                self.draw_board()
        else:
            self.try_make_move(self.selected_square, square)

    def handle_drag(self, event):
        if self.selected_square is None or self.ai_is_thinking: return
        piece = self.board.piece_at(self.selected_square)
        if piece:
            self.canvas.delete("drag")
            self.canvas.create_text(event.x, event.y, text=self.pieces_dict[piece.symbol()], font=("Arial", 46), fill="#555555", tags="drag")

    def handle_release(self, event):
        if self.selected_square is None or self.ai_is_thinking: return
        self.canvas.delete("drag")
        square = self._coord_to_square(event.x, event.y)
        if square is not None and square != self.selected_square:
            self.try_make_move(self.selected_square, square)
        else:
            self.cancel_selection()

    def _coord_to_square(self, x, y):
        file = x // self.square_size
        rank = 7 - (y // self.square_size)
        if not (0 <= file < 8 and 0 <= rank < 8): return None
        if self.flip_board:
            file = 7 - file
            rank = 7 - rank
        return chess.square(file, rank)

    def try_make_move(self, from_sq, to_sq):
        move = chess.Move(from_sq, to_sq)
        piece = self.board.piece_at(from_sq)

        if piece and piece.piece_type == chess.PAWN and \
           ((self.board.turn == chess.WHITE and chess.square_rank(to_sq) == 7) or
            (self.board.turn == chess.BLACK and chess.square_rank(to_sq) == 0)):
            prom = self.ask_promotion()
            if prom is None:
                self.cancel_selection()
                return
            move = chess.Move(from_sq, to_sq, promotion=prom)

        if move in self.board.legal_moves:
            if self.board.move_stack:  
                if self.board.turn == chess.WHITE: self.white_remaining += self.increment
                else: self.black_remaining += self.increment

            self.last_move = move
            self.board.push(move)
            self.cancel_selection()

            if self.game_mode == "vs_ai" and self.board.turn == chess.BLACK and not self.board.is_game_over():
                self.ai_is_thinking = True
                self.root.after(300, self.make_ai_move)
        else:
            self.cancel_selection()

    def ask_promotion(self):
        choice = simpledialog.askstring("Promoce", "Vyber figuru (Dáma, Věž, Střelec, Jezdec):", initialvalue="Dáma")
        d = {"dáma": chess.QUEEN, "věž": chess.ROOK, "střelec": chess.BISHOP, "jezdec": chess.KNIGHT, "kůň": chess.KNIGHT,
             "queen": chess.QUEEN, "rook": chess.ROOK, "bishop": chess.BISHOP, "knight": chess.KNIGHT}
        return d.get(choice.lower() if choice else "", chess.QUEEN)

    def cancel_selection(self):
        self.selected_square = None
        self.highlighted_moves = []
        self.draw_board()

    def make_ai_move(self):
        def ai_thread():
            try:
                with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:
                    result = engine.play(self.board, chess.engine.Limit(depth=self.ai_difficulty))
                    def submit_move():
                        self.ai_is_thinking = False
                        if result.move: self.try_make_move(result.move.from_square, result.move.to_square)
                    self.root.after(0, submit_move)
            except Exception as e:
                def report_error():
                    self.ai_is_thinking = False
                    messagebox.showerror("AI Chyba", f"Došlo k chybě při komunikaci s botem.\nUjistěte se, že soubor 'stockfish.exe' je ve stejné složce jako tento skript.\n\nDetaily: {e}")
                self.root.after(0, report_error)

        threading.Thread(target=ai_thread, daemon=True).start()

    def update_timer(self):
        if self.game_over:
            self.root.after(200, self.update_timer)
            return

        now = time.time()
        if self.last_update is None: self.last_update = now

        if self.board.move_stack:
            elapsed = now - self.last_update
            if self.board.turn == chess.WHITE: self.white_remaining = max(0, self.white_remaining - elapsed)
            else: self.black_remaining = max(0, self.black_remaining - elapsed)

        self.last_update = now

        w_min, w_sec = divmod(int(self.white_remaining), 60)
        b_min, b_sec = divmod(int(self.black_remaining), 60)
        self.white_time_lbl.config(text=f"Bílý: {w_min:02d}:{w_sec:02d}")
        self.black_time_lbl.config(text=f"Černý: {b_min:02d}:{b_sec:02d}")

        if self.white_remaining <= 0 or self.black_remaining <= 0:
            self.game_over = True
            winner = "Černý" if self.white_remaining <= 0 else "Bílý"
            self.status_lbl.config(text=f"Čas vypršel! Vyhrál {winner}", fg="red")
            messagebox.showinfo("Konec hry", f"Vypršel čas! Vítězí {winner}.")

        self.root.after(200, self.update_timer)

    def update_captured(self):
        starting_counts = {'P': 8, 'N': 2, 'B': 2, 'R': 2, 'Q': 1, 'p': 8, 'n': 2, 'b': 2, 'r': 2, 'q': 1}
        current_counts = {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0, 'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}

        for sq in chess.SQUARES:
            p = self.board.piece_at(sq)
            if p and p.piece_type != chess.KING: current_counts[p.symbol()] += 1

        white_cap, black_cap = [], []
        for piece_sym in starting_counts:
            missing = starting_counts[piece_sym] - current_counts[piece_sym]
            if missing > 0:
                visual_char = self.pieces_dict[piece_sym]
                if piece_sym.isupper(): white_cap.extend([visual_char] * missing)
                else: black_cap.extend([visual_char] * missing)

        self.white_captured_lbl.config(text=" ".join(white_cap))
        self.black_captured_lbl.config(text=" ".join(black_cap))

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        temp_board = chess.Board()
        for i, move in enumerate(self.board.move_stack):
            try:
                san_move = temp_board.san(move)
                temp_board.push(move)
                if i % 2 == 0: self.history_text.insert(tk.END, f"{(i // 2) + 1:2d}. {san_move:<8}")
                else: self.history_text.insert(tk.END, f"{san_move}\n")
            except: break
        self.history_text.config(state="disabled")
        self.history_text.see(tk.END)

    def update_status(self):
        if self.board.is_checkmate():
            self.game_over = True
            winner = "Černý" if self.board.turn == chess.WHITE else "Bílý"
            self.status_lbl.config(text=f"ŠACHMAT! {winner} vyhrál", fg="#ff4444")
        elif self.board.is_stalemate():
            self.game_over = True
            self.status_lbl.config(text="PAT - Remíza", fg="#ffaa00")
        elif self.board.is_insufficient_material():
            self.game_over = True
            self.status_lbl.config(text="Remíza - materiál", fg="#ffaa00")
        else:
            player = "Bílý" if self.board.turn == chess.WHITE else "Černý"
            check = " (Šach)" if self.board.is_check() else ""
            color = "#00aa55" if self.board.turn == chess.WHITE else "#ff5555"
            self.status_lbl.config(text=f"{player} na tahu{check}", fg=color)

    def reset_game_state(self):
        self.white_remaining = 600
        self.black_remaining = 600
        self.increment = 5
        self.last_move = None
        self.game_over = False
        self.ai_is_thinking = False
        self.last_update = time.time()
        self.cancel_selection()

    def new_game(self):
        if messagebox.askyesno("Nová hra", "Opravdu chcete začít novou hru?"):
            self.board = chess.Board()
            self.reset_game_state()
            self.draw_board()

    def undo_move(self):
        if self.ai_is_thinking: return
        undo_count = 2 if self.game_mode == "vs_ai" else 1
        for _ in range(undo_count):
            if self.board.move_stack: self.board.pop()
        self.last_move = self.board.move_stack[-1] if self.board.move_stack else None
        self.game_over = False
        self.last_update = time.time()
        self.cancel_selection()

    def flip_board_func(self):
        self.flip_board = not self.flip_board
        self.draw_board()

    def set_mode(self, mode):
        self.game_mode = mode
        self.board = chess.Board()
        self.reset_game_state()
        self.draw_board()

    def ai_settings(self):
        level = simpledialog.askinteger("Obtížnost AI", "Zadejte hloubku výpočtu bota (1-20):", minvalue=1, maxvalue=20, initialvalue=self.ai_difficulty)
        if level: self.ai_difficulty = level

    def save_pgn(self):
        game = chess.pgn.Game.from_board(self.board)
        game.headers["Event"] = "Šachy Pro Zápas"
        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        filename = filedialog.asksaveasfilename(defaultextension=".pgn", filetypes=[("PGN soubory", "*.pgn")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f: f.write(str(game))

    def load_pgn(self):
        filename = filedialog.askopenfilename(filetypes=[("PGN soubory", "*.pgn")])
        if filename:
            with open(filename, encoding="utf-8") as f:
                game = chess.pgn.read_game(f)
                if game:
                    self.board = game.board()
                    for move in game.mainline_moves(): self.board.push(move)
                    self.reset_game_state()
                    if self.board.move_stack: self.last_move = self.board.move_stack[-1]
                    self.draw_board()

    def resign(self):
        if not self.game_over and messagebox.askyesno("Vzdát se", "Opravdu se chcete vzdát?"):
            self.game_over = True
            winner = "Černý" if self.board.turn == chess.WHITE else "Bílý"
            self.status_lbl.config(text=f"{winner} vyhrál (vzdání)", fg="red")

if __name__ == "__main__":
    ChessApp()