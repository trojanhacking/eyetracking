import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QUrl, QThread, pyqtSignal
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtGui import QFont, QImage, QPixmap
from os.path import join
import cv2
import mediapipe as mp #for intelligence
from testIsFocus import isFocused


mp_face_mesh = mp.solutions.face_mesh # type: ignore
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)


NOTIFICATION_SOUND_EFFECT_PATH = join("assets", "notification.wav")
DONE_SOUND_EFFECT_PATH = join("assets", "done.wav")

FOCUS_TIME_TEXT = "Current settings: Focus for %d minutes then let your eyes take a %d second break"


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

        self.minutes = 20
        self.seconds = 20


        self.init_ui()
    
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # region: time
        timer_layout = QVBoxLayout()

        self.time_header = QLabel("Set timings:")
        self.time_header.setFont(QFont("Arial", 48))
        timer_layout.addWidget(self.time_header)

        self.time_explainer = QLabel(FOCUS_TIME_TEXT % (20, 20))
        self.time_explainer.setFont(QFont("Arial", 24))
        timer_layout.addWidget(self.time_explainer)

        timer_horizontal = QHBoxLayout()
        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Enter period of focus (minutes)")
        timer_horizontal.addWidget(self.time_input)

        self.set_time_button = QPushButton("Set time", self)
        self.set_time_button.clicked.connect(self.set_time)
        timer_horizontal.addWidget(self.set_time_button)

        self.timer_label = QLabel("20 minutes", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.timer_label.setFont(QFont("Arial", 48))
        timer_horizontal.addWidget(self.timer_label)

        timer_layout.addLayout(timer_horizontal)

        timer_horizontal2 = QHBoxLayout()
        self.time_input2 = QLineEdit(self)
        self.time_input2.setPlaceholderText("Enter period of eye rest (seconds)")
        timer_horizontal2.addWidget(self.time_input2)

        self.set_time_button2 = QPushButton("Set time", self)
        self.set_time_button2.clicked.connect(self.set_time2)
        timer_horizontal2.addWidget(self.set_time_button2)

        self.timer_label2 = QLabel("20 seconds", self)
        self.timer_label2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.timer_label2.setFont(QFont("Arial", 48))
        timer_horizontal2.addWidget(self.timer_label2)
        
        timer_layout.addLayout(timer_horizontal2)
        layout.addLayout(timer_layout)
        # endregion: timer

        self.title = QLabel("What the computer sees:")
        layout.addWidget(self.title)

        self.feed_label = QLabel()
        layout.addWidget(self.feed_label)

        self.worker = Worker()
        self.worker.start()
        self.worker.image_update.connect(self.image_update_slot)
        self.worker.focus_update.connect(self.focus_update_slot)
        

        self.debug_info = QLabel("Debug information:")
        layout.addWidget(self.debug_info)

        # self.button = QPushButton("Click Me!")
        # self.button.clicked.connect(self.on_button_click)
        # layout.addWidget(self.button)
    
    def set_time(self):
        try:
            minutes = int(self.time_input.text())
            self.timer_label.setText(f"{minutes} minutes")
            self.time_explainer.setText(FOCUS_TIME_TEXT % (minutes, self.seconds))
            self.minutes = minutes
        except ValueError:
            print("Enter a positive integer for minutes!")
    
    def set_time2(self):
        try:
            seconds = int(self.time_input2.text())
            self.timer_label.setText(f"{seconds} minutes")
            self.time_explainer.setText(FOCUS_TIME_TEXT % (seconds, self.seconds))
            self.minutes = seconds
        except ValueError:
            print("Enter a positive integer for seconds!")

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
        self.timer_label.setText(f"Time left: {hours:02}:{minutes:02}:{seconds:02}")

    def image_update_slot(self, image):
        self.feed_label.setPixmap(QPixmap.fromImage(image))

    def focus_update_slot(self, is_focused):
        print(is_focused)
        if is_focused:
            self.start_countdown()
        else:
            self.start_countdown()


class Worker(QThread):
    image_update = pyqtSignal(QImage)
    focus_update = pyqtSignal(QImage)

    def run(self):
        self.thread_active = True
        self.was_focused = None

        capture = cv2.VideoCapture(0)
        while self.thread_active:
            ret, frame = capture.read()
            if not ret:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)
            h, w, _ = rgb.shape

            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks: #primary face
                    h, w, _ = rgb.shape
                    for id, lm in enumerate(landmarks.landmark):
                        
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(rgb, (x, y), 1, (0,255,0), -1)
                        cv2.circle(rgb, (x, y), 1, (0,255,0), -1)

                    # cv2.circle(frame, (int(landmarks.landmark[468].x * w), int(landmarks.landmark[468].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
                    # cv2.circle(frame, (int(landmarks.landmark[473].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

                    #head
                    cv2.circle(rgb, (int(landmarks.landmark[127].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
                    cv2.circle(rgb, (int(landmarks.landmark[6].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)
                    cv2.circle(rgb, (int(landmarks.landmark[356].x * w), int(landmarks.landmark[473].y * h)), radius=3, color=(0, 0, 255), thickness=-1)

                    # if (is_looking_at_screen(landmarks.landmark, w, h)):
                    #     print("Looking")
                    # else:
                    #     print("Not looking")
                    # print(calculate_eye_focus_rotation(landmarks.landmark, w, h))

                    # is_focused = isFocused(landmarks)
                    # if is_focused is not self.was_focused:
                    #     self.focus_update.emit(is_focused)
                    #     self.was_focused = is_focused

                    # print(normalizedLandmark_to_numpyVector( landmarks.landmark[6] ))
                    # print(calculate_eye_rotation())
                    # depthTracking(landmarks)
            # flipped = cv2.flip(rgb, 1)
            frame = cv2.flip(rgb, 1)
            to_qt = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
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
