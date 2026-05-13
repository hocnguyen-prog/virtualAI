import sys
from PySide6 import QtWidgets, QtCore

class btnColorSwatch(QtWidgets.QPushButton):
    def __init__(self, text, color1, color2):
        super().__init__(text)
        self.color1 = color1
        self.color2 = color2
        self.setStyleSheet(f"background-color: {self.color1};")
        self.clicked.connect(self.switch_color)

    def switch_color(self):
        current_color = self.palette().button().color().name()
        new_color = self.color2 if current_color == self.color1 else self.color1
        if self.window() and self.window().centralWidget():
            self.window().centralWidget().setStyleSheet(f"background-color: {new_color};")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Switcher")
        self.setGeometry(100, 100, 300, 200)

        # Vytvoření tlačítka s přepínáním barev
        color_button = btnColorSwatch("Switch Color", "#490068", "#8000ff")
        color_button.setFixedSize(150, 50)

        # Nastavení centrálního widgetu
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(color_button, alignment=QtCore.Qt.AlignCenter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())