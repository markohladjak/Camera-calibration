from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ControlPanel2(QWidget):
    def __init__(self, update_video_settings_callback):
        super().__init__()

        self.update_video_settings_callback = update_video_settings_callback  # Передаємо налаштування у відеопотік

        self.setWindowTitle("Control Panel 2")
        self.setGeometry(10, 240, 300, 200)  # Збільшуємо розмір вікна для кращого відображення

        # Чекбокси для відеопараметрів
        self.grayscale_checkbox = QCheckBox('Перетворити в відтінки сірого', self)
        self.grayscale_checkbox.setChecked(False)  # Дефолтне значення: False
        self.grayscale_checkbox.stateChanged.connect(self.update_settings)

        self.chessboard_checkbox = QCheckBox('Покращення розпізнавання шахової дошки', self)
        self.chessboard_checkbox.setChecked(False)  # Дефолтне значення: False
        self.chessboard_checkbox.stateChanged.connect(self.update_settings)

        self.contrast_checkbox = QCheckBox('Підвищити контрасність', self)
        self.contrast_checkbox.setChecked(False)  # Дефолтне значення: False
        self.contrast_checkbox.stateChanged.connect(self.update_settings)

        # Інпут для кадрів за секунду (FPS)
        self.fps_label = QLabel('Кадри за секунду:')
        self.fps_input = QLineEdit(self)
        self.fps_input.setText('30')  # Дефолтне значення FPS 30
        self.fps_input.textChanged.connect(self.update_settings)

        # Кнопки
        self.calibration_button = QPushButton('Calibration', self)
        self.calibration_button.clicked.connect(self.calibration_clicked)  # Додаємо обробку кнопки Calibration

        self.photo_button = QPushButton('Photo', self)
        self.photo_button.clicked.connect(self.photo_clicked)  # Додаємо обробку кнопки Photo

        self.auto_photo_button = QPushButton('Auto Photo', self)
        self.auto_photo_button.clicked.connect(self.auto_photo_clicked)  # Додаємо обробку кнопки Auto Photo

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_values)

        # Макет для віджетів
        layout = QVBoxLayout()
        layout.addWidget(self.grayscale_checkbox)
        layout.addWidget(self.chessboard_checkbox)
        layout.addWidget(self.contrast_checkbox)
        layout.addWidget(self.fps_label)
        layout.addWidget(self.fps_input)
        layout.addWidget(self.calibration_button)  # Додаємо кнопку Calibration
        layout.addWidget(self.photo_button)  # Додаємо кнопку Photo
        layout.addWidget(self.auto_photo_button)  # Додаємо кнопку Auto Photo
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    # Функція для скидання значень до дефолтних
    def reset_values(self):
        self.fps_input.setText('30')  # Дефолтне значення для FPS
        self.grayscale_checkbox.setChecked(False)  # Дефолтне значення для grayscale
        self.chessboard_checkbox.setChecked(False)  # Дефолтне значення для chessboard
        self.contrast_checkbox.setChecked(False)  # Дефолтне значення для contrast
        self.update_settings()

    # Функція для обробки налаштувань відеопотоку
    def update_settings(self):
        settings = {
            'grayscale': self.grayscale_checkbox.isChecked(),
            'chessboard': self.chessboard_checkbox.isChecked(),
            'contrast': self.contrast_checkbox.isChecked(),
            'fps': int(self.fps_input.text()) if self.fps_input.text().isdigit() else 30,
        }
        self.update_video_settings_callback(settings)  # Передаємо налаштування назад у відеопотік

    # Обробка події для кнопки Calibration
    def calibration_clicked(self):
        print("Calibration process started")
        # Додаємо логіку для процесу калібрування

    # Обробка події для кнопки Photo
    def photo_clicked(self):
        print("Photo taken")
        # Додаємо логіку для процесу збереження фото

    # Обробка події для кнопки Auto Photo
    def auto_photo_clicked(self):
        print("Auto photo process started")
        # Додаємо логіку для автоматичного захоплення фото
