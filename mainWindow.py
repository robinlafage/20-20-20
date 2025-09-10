from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from pauseWindow import PauseWindow
from PySide6.QtCore import Qt, QTimer

TIMER = 20 * 60

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("20-20-20")
        self.setMinimumSize(500, 400)
        self.setFont(QFont("Segoe UI", 10))

        layout = QVBoxLayout()

        # Label explicatif
        self.label = QLabel(
            "Rappel toutes les 20 minutes pour regarder à 20 pieds (6 mètres) pendant 20 secondes."
        )
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Segoe UI", 13))
        layout.addWidget(self.label, alignment=Qt.AlignCenter | Qt.AlignTop)

        # Bouton start
        self.start_button = QPushButton("Démarrer")
        self.start_button.clicked.connect(self.start)
        self.start_button.setFixedWidth(150)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        # Bouton pause
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause)
        self.pause_button.setFixedWidth(150)
        layout.addWidget(self.pause_button, alignment=Qt.AlignCenter)

        # Label résultat (compte à rebours)
        self.result = QLabel("Prochaine pause dans : 20 min 0 s")
        self.result.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.result, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Thème sombre
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #3c3f41;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #505354;
            }
        """)

        # Gestion timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)

        self.remaining_time = None
        self.pauseWindow = None

    def start(self):
        print("Timer démarré")
        if self.remaining_time is None:
            self.remaining_time = TIMER
        
        if not self.timer.isActive():
            self.timer.start(1000)  # appel toutes les 1 seconde

    def pause(self):
        print("Timer en pause")
        self.timer.stop()

    def update_countdown(self):
        self.remaining_time -= 1
        minutes, seconds = divmod(self.remaining_time, 60)
        self.result.setText(f"Prochaine pause dans : {minutes} min {seconds} s")

        if self.remaining_time <= 0:
            self.timer.stop()
            self.show_pause_window()

    def show_pause_window(self):
        print("Affichage de la pause")
        self.pauseWindow = PauseWindow(duration=20)
        self.pauseWindow.show()

        QTimer.singleShot(20000, self.close_pause_window)

    def close_pause_window(self):
        print("Fin de la pause")
        if self.pauseWindow:
            self.pauseWindow.close()
            self.pauseWindow = None

        # Relancer le timer
        self.restart_timer()

    def restart_timer(self):
        print("Reprise du cycle après pause")
        self.remaining_time = TIMER
        self.timer.start(1000)  
