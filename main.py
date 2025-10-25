import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QUrl, QThread, pyqtSignal
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtGui import QFont, QImage, QPixmap
from os.path import join
import cv2


NOTIFICATION_SOUND_EFFECT_PATH = join("assets", "notification.wav")
DONE_SOUND_EFFECT_PATH = join("assets", "done.wav")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Focus Flow")
        self.setGeometry(100, 100, 900, 500) # x, y, width, height

        self.time_between_secs = 20 * 60
        self.time_break_secs = 20 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.notification_sound_effect = QSoundEffect()
        self.notification_sound_effect.setSource(QUrl.fromLocalFile(NOTIFICATION_SOUND_EFFECT_PATH))
        self.done_sound_effect = QSoundEffect()
        self.done_sound_effect.setSource(QUrl.fromLocalFile(DONE_SOUND_EFFECT_PATH))


        self.init_ui()
    
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # region: timer
        timer_layout = QVBoxLayout()
        timer_horizontal = QHBoxLayout()

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Enter seconds")
        timer_horizontal.addWidget(self.time_input)

        self.set_time_button = QPushButton("Set time", self)
        self.set_time_button.clicked.connect(self.start_countdown)
        timer_horizontal.addWidget(self.set_time_button)
        timer_layout.addLayout(timer_horizontal)

        # self.start_button = QPushButton("Start", self)
        # self.start_button.clicked.connect(self.start_countdown)
        # timer_layout.addWidget(self.start_button)

        # self.stop_button = QPushButton("Stop", self)
        # self.stop_button.clicked.connect(self.stop_countdown)
        # self.stop_button.setEnabled(False)
        # timer_layout.addWidget(self.stop_button)

        self.timer_label = QLabel("00:00:00", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 48))
        timer_layout.addWidget(self.timer_label)

        layout.addLayout(timer_layout)
        # endregion: timer

        self.title = QLabel("What the computer sees:")
        layout.addWidget(self.title)

        self.feed_label = QLabel()
        layout.addWidget(self.feed_label)

        self.worker = Worker()
        self.worker.start()
        self.worker.image_update.connect(self.image_update_slot)
        

        self.debug_info = QLabel("Debug information:")
        layout.addWidget(self.debug_info)

        # self.button = QPushButton("Click Me!")
        # self.button.clicked.connect(self.on_button_click)
        # layout.addWidget(self.button)
    
    def start_countdown(self):
        try:
            seconds_input = int(self.time_input.text())
            if seconds_input < 0:
                self.timer_label.setText("Enter a positive number.")
                return
            self.time_left_seconds = seconds_input
            self.update_timer_display()
            self.timer.start(1000) # Update every 1000 milliseconds (1 second)
            self.set_time_button.setEnabled(False)
            # self.stop_button.setEnabled(True)
        except ValueError:
            self.timer_label.setText("Invalid input.")

    def stop_countdown(self):
        self.timer.stop()
        self.set_time_button.setEnabled(True)
        # self.stop_button.setEnabled(False)

    def update_timer(self):
        if self.time_left_seconds > 0:
            self.time_left_seconds -= 1
            self.update_timer_display()
        else:
            self.timer.stop()
            self.notification_sound_effect.play()
            self.timer_label.setText("Time's Up!")
            self.set_time_button.setEnabled(True)
            # self.stop_button.setEnabled(False)

    def update_timer_display(self):
        left = self.time_left_seconds
        hours = left // 3600
        left %= 3600
        minutes = left // 60
        seconds = left % 60
        self.timer_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def image_update_slot(self, image):
        self.feed_label.setPixmap(QPixmap.fromImage(image))


class Worker(QThread):
    image_update = pyqtSignal(QImage)

    def run(self):
        self.thread_active = True
        capture = cv2.VideoCapture(0)
        while self.thread_active:
            ret, frame = capture.read()
            if not ret:
                continue
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            flipped = cv2.flip(image, 1)
            to_qt = QImage(flipped.data, flipped.shape[1], flipped.shape[0], QImage.Format.Format_RGB888)
            pic = to_qt.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_update.emit(pic)
    
    def stop(self):
        self.thread_active = False
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("style.qss") as f:
        _style = f.read()

    app.setStyleSheet(_style)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
