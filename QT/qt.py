import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget,
    QListWidgetItem, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

# --- 1. POZNÁMKY ---
class NotesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.notes_file = "notes.json"
        self.init_ui()
        self.load_notes()

    def init_ui(self):
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        title = QLabel("📝 Poznámky")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Hledat...")
        self.search_bar.textChanged.connect(self.load_notes)
        top_layout.addWidget(title)
        top_layout.addWidget(self.search_bar)
        layout.addLayout(top_layout)
        
        self.note_input = QTextEdit()
        layout.addWidget(self.note_input)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Uložit")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        save_btn.clicked.connect(self.save_note)
        clear_btn = QPushButton("🧹 Vyčistit")
        clear_btn.clicked.connect(self.note_input.clear)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)
        
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_selected_note)
        layout.addWidget(self.notes_list)
        
        delete_btn = QPushButton("❌ Smazat")
        delete_btn.clicked.connect(self.delete_note)
        layout.addWidget(delete_btn)
        self.setLayout(layout)

    def load_notes_data(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_note(self):
        text = self.note_input.toPlainText().strip()
        if not text: return
        notes = self.load_notes_data()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notes[ts] = {"title": text.split('\n')[0][:30], "content": text}
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        self.note_input.clear()
        self.load_notes()

    def load_notes(self):
        self.notes_list.clear()
        search = self.search_bar.text().lower()
        notes = self.load_notes_data()
        for ts, data in sorted(notes.items(), reverse=True):
            if search in data['content'].lower():
                item = QListWidgetItem(f"{ts} - {data['title']}")
                item.setData(Qt.UserRole, ts)
                self.notes_list.addItem(item)

    def load_selected_note(self, item):
        ts = item.data(Qt.UserRole)
        notes = self.load_notes_data()
        self.note_input.setPlainText(notes[ts]['content'])

    def delete_note(self):
        item = self.notes_list.currentItem()
        if not item: return
        notes = self.load_notes_data()
        del notes[item.data(Qt.UserRole)]
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2)
        self.load_notes()

# --- 2. KALKULAČKA ---
class CalculatorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 25px; padding: 10px;")
        layout.addWidget(self.display)

        grid = [['7','8','9','/'],['4','5','6','*'],['1','2','3','-'],['C','0','=','+']]
        for row in grid:
            h = QHBoxLayout()
            for char in row:
                btn = QPushButton(char)
                btn.setFixedSize(50, 50)
                if char == '=': btn.clicked.connect(self.solve)
                elif char == 'C': btn.clicked.connect(lambda: self.display.setText("0"))
                else: btn.clicked.connect(lambda _, c=char: self.press(c))
                h.addWidget(btn)
            layout.addLayout(h)
        self.setLayout(layout)

    def press(self, char):
        if self.display.text() == "0": self.display.setText(char)
        else: self.display.setText(self.display.text() + char)

    def solve(self):
        try: self.display.setText(str(eval(self.display.text())))
        except: self.display.setText("Error")

# --- 3. TIMER ---
class TimerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.seconds = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.lbl = QLabel("00:00:00")
        self.lbl.setFont(QFont("Arial", 30, QFont.Bold))
        self.lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl)

        self.spin = QSpinBox()
        self.spin.setMaximum(3600)
        layout.addWidget(self.spin)

        btn = QPushButton("Start / Stop")
        btn.clicked.connect(self.toggle)
        layout.addWidget(btn)
        self.setLayout(layout)

    def toggle(self):
        if self.timer.isActive(): self.timer.stop()
        else:
            if self.seconds == 0: self.seconds = self.spin.value()
            self.timer.start(1000)

    def update_timer(self):
        if self.seconds > 0:
            self.seconds -= 1
            m, s = divmod(self.seconds, 60)
            h, m = divmod(m, 60)
            self.lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")
        else:
            self.timer.stop()
            QMessageBox.information(self, "Čas vypršel", "Timer dojel do konce!")

# --- 4. TODO ---
class TodoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.file = "todos.json"
        self.init_ui()
        self.load_todos()

    def init_ui(self):
        layout = QVBoxLayout()
        h = QHBoxLayout()
        self.input = QLineEdit()
        btn = QPushButton("Přidat")
        btn.clicked.connect(self.add)
        h.addWidget(self.input)
        h.addWidget(btn)
        layout.addLayout(h)
        self.list = QListWidget()
        layout.addWidget(self.list)
        self.setLayout(layout)

    def add(self):
        txt = self.input.text()
        if not txt: return
        todos = self.get_data()
        todos[datetime.now().isoformat()] = {"task": txt, "done": False}
        with open(self.file, 'w') as f: json.dump(todos, f)
        self.input.clear()
        self.load_todos()

    def get_data(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f: return json.load(f)
        return {}

    def load_todos(self):
        self.list.clear()
        for k, v in self.get_data().items():
            self.list.addItem(v['task'])

# --- HLAVNÍ OKNO ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Dashboard")
        self.resize(400, 600)
        
        tabs = QTabWidget()
        tabs.addTab(NotesTab(), "Notes")
        tabs.addTab(CalculatorTab(), "Calc")
        tabs.addTab(TimerTab(), "Timer")
        tabs.addTab(TodoTab(), "Todo")
        
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
