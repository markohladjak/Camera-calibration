from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import cv2
import numpy as np

class ControlPanel3(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control Panel 3")
        self.setGeometry(10, 520, 300, 200)  # Збільшуємо висоту вікна

        # Створюємо полотно для гістограми
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Поле для виведення даних консолі
        self.console_output = QTextEdit(self)
        self.console_output.setReadOnly(True)  # Поле тільки для читання

        # Макет для розташування віджетів
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)  # Додаємо віджет для гістограми
        layout.addWidget(self.console_output)  # Додаємо поле виводу з консолі

        self.setLayout(layout)

    # Функція для відображення гістограми
    def update_histogram(self, frame):
        self.figure.clear()  # Очищуємо старі дані
        ax = self.figure.add_subplot(111)

        # Перевіряємо, чи кадр кольоровий або чорно-білий
        if len(frame.shape) == 2 or frame.shape[2] == 1:
            # Гістограма для чорно-білого зображення
            ax.hist(frame.ravel(), bins=256, range=(0, 256), color='gray')
        else:
            # Гістограма для кожного кольорового каналу
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                hist = cv2.calcHist([frame], [i], None, [256], [0, 256])
                ax.plot(hist, color=col)
                ax.set_xlim([0, 256])

        self.canvas.draw()  # Оновлюємо полотно

    # Функція для виведення повідомлень у консоль
    def log_to_console(self, message):
        self.console_output.append(message)  # Додаємо повідомлення у текстове поле
        self.console_output.ensureCursorVisible()  # Прокручуємо вниз для нових повідомлень
