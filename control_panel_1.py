import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout
import sys
from control_panel_2 import ControlPanel2  # Імпортуємо control_panel_2
from control_panel_3 import ControlPanel3  # Імпортуємо control_panel_3

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control Panel 1")
        self.setGeometry(10, 40, 300, 150)

        # Випадаючий список для вибору індексу камери
        self.label_index = QLabel("Виберіть індекс камери:", self)
        self.camera_index_combo = QComboBox(self)
        self.camera_index_combo.addItems(["0", "1", "2"])  # Індекси камер

        # Випадаючий список для вибору роздільної здатності
        self.label_resolution = QLabel("Виберіть розмір камери:", self)
        self.camera_resolution_combo = QComboBox(self)
        self.camera_resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])  # Розміри камер

        # Кнопка для запуску відеопотоку
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_camera)

        # Кнопка для зупинки відеопотоку
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)  # Робимо кнопку неактивною до запуску відеопотоку
        self.stop_button.clicked.connect(self.stop_camera)

        # Макет для розташування віджетів
        layout = QVBoxLayout()
        layout.addWidget(self.label_index)
        layout.addWidget(self.camera_index_combo)
        layout.addWidget(self.label_resolution)
        layout.addWidget(self.camera_resolution_combo)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.cap = None  # Перемінна для відеопотоку
        self.current_settings = None  # Зберігаємо налаштування з другого файлу

        # Створюємо екземпляр ControlPanel2 і підключаємо функцію для оновлення налаштувань
        self.control_panel_2 = ControlPanel2(self.update_video_settings)
        self.control_panel_2.show()  # Автоматично відкриваємо друге вікно

        # Додаємо виклик для ControlPanel3
        self.control_panel_3 = ControlPanel3()
        self.control_panel_3.show()  # Автоматично відкриваємо третє вікно

    def update_video_settings(self, settings):
        """
        Функція для обробки змінених налаштувань з control_panel_2.py
        """
        self.current_settings = settings
        print(f"Оновлені налаштування: {settings}")  # Виводимо для перевірки
        # Можемо використати ці налаштування під час відеопотоку

    def start_camera(self):
        camera_index = int(self.camera_index_combo.currentText())
        resolution = self.camera_resolution_combo.currentText().split('x')
        width, height = int(resolution[0]), int(resolution[1])

        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.camera_index_combo.setEnabled(False)
        self.camera_resolution_combo.setEnabled(False)

        frame_count = 0  # Лічильник кадрів

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_count += 1  # Збільшуємо лічильник кадрів

            # Перевіряємо і застосовуємо налаштування з control_panel_2
            if self.current_settings:
                if self.current_settings['grayscale']:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if self.current_settings['contrast']:
                    frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

            # Оновлюємо гістограму кожного кадру
            self.control_panel_3.update_histogram(frame)

            # Логуємо повідомлення в консоль кожні 30 кадрів
            if frame_count % 30 == 0:
                self.control_panel_3.log_to_console(f"Оброблено {frame_count} кадрів")

            cv2.imshow('Camera Stream', frame)

            # Вихід з потоку при натисканні 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop_camera(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.camera_index_combo.setEnabled(True)
        self.camera_resolution_combo.setEnabled(True)

# Запуск програми
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
