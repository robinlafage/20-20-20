from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer


class PauseWindow(QWidget):
    def __init__(self, duration=20):
        super().__init__()

        self.setWindowTitle("20-20-20")
        self.showFullScreen()

        # Durée de la pause en secondes
        self.remaining_time = duration

        # Timer qui décrémente chaque seconde
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)

        # Layout vertical
        layout = QVBoxLayout()

        # Label principal
        self.label = QLabel("Regardez au loin ...")
        self.label.setFont(QFont("Segoe UI", 22))
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Label compte à rebours
        self.sub_label = QLabel(str(self.remaining_time))
        self.sub_label.setFont(QFont("Segoe UI", 22))
        layout.addWidget(self.sub_label, alignment=Qt.AlignCenter | Qt.AlignTop)

        self.setLayout(layout)

        # Thème sombre simple
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
        """)

        # Démarrer le timer
        self.timer.start(1000)

    def update_countdown(self):
        self.remaining_time -= 1
        self.sub_label.setText(str(self.remaining_time))

        if self.remaining_time <= 0:
            self.timer.stop()
            self.close()
