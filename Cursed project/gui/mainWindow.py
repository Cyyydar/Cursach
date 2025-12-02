import os
import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QComboBox, QFileDialog, QHBoxLayout, QVBoxLayout, QCheckBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
#from augmentMethodWidget import AugmentationMethodWidget #augmentMethodWidget import AugmentationMethodWidget
from gui.augmentMethodWidget import AugmentationMethodWidget
from augmentator.noiseAugmentator import NoiseAugmentator

# Путь до папки platforms, так как qt на питоне проклят и не работает нифига
plugin_path = r"Lib\site-packages\PyQt5\Qt5\plugins\platforms"

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
class MainWindow(QMainWindow):
    path_to_data = "Cursed project\data"
    pic_index = 1
    current_dataset = ""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Аугментатор")
        self.resize(1000, 600)

        central = QWidget(self)
        self.setCentralWidget(central)

        # -------- Основная вертикальная компоновка ----------
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # --------------- Блок изображений --------------------
        images_layout = QHBoxLayout()
        images_layout.setAlignment(Qt.AlignCenter)

        # Левое изображение (оригинал)
        self.image_left = QLabel("Вход")
        self.image_left.setAlignment(Qt.AlignCenter)
        self.image_left.setFixedSize(300, 300)
        self.image_left.setStyleSheet("border: 1px solid gray;")

        # Правое изображение (результат)
        self.image_right = QLabel("Выход")
        self.image_right.setAlignment(Qt.AlignCenter)
        self.image_right.setFixedSize(300, 300)
        self.image_right.setStyleSheet("border: 1px solid gray;")

        images_layout.addWidget(self.image_left)
        images_layout.addWidget(self.image_right)

        main_layout.addLayout(images_layout)

        # --------------- Блок выбора параметров ----------------
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignCenter)

        # ComboBox выбора набора данных
        self.dataset_combo = QComboBox()
        self.dataset_combo.addItems(self.get_data_names())
        self.dataset_combo.currentTextChanged.connect(self.change_dataset)
        self.dataset_combo.setFixedWidth(200)

        controls_layout.addWidget(self.dataset_combo)

        # Методы аугментации
        self.methods = []

        # Шум
        noise_box = QVBoxLayout()
        noise_box.setSpacing(10)
        
        self.noise_label = QLabel("Зашумление")
        noise_box.addWidget(self.noise_label)
        noise_methods = [AugmentationMethodWidget("Гаусс", NoiseAugmentator.gaussian, {"mean": (0, -50, 50, 1), "sigma": (10, 0, 100, 1)}),
                         AugmentationMethodWidget("Релей", NoiseAugmentator.rayleigh, {"scale": (20, -50, 50, 1)}),
                         AugmentationMethodWidget("Экспоненциальный шум", NoiseAugmentator.exponential, {"lam": (0.02, -50, 50, 0.01)})
                         ]
        for method in noise_methods:
            self.methods.append(method)
            noise_box.addWidget(method)

        controls_layout.addLayout(noise_box)

        # Дальше всякие методы

        main_layout.addLayout(controls_layout)

        # ----------------- Кнопки --------------------
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)


        self.back_button = QPushButton("<- Назад")
        self.back_button.setFixedSize(250, 40)
        self.back_button.clicked.connect(self.button_left)
        buttons_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.process_button = QPushButton("Выполнить обработку")
        self.process_button.setFixedSize(250, 40)
        self.process_button.clicked.connect(self.process)
        buttons_layout.addWidget(self.process_button, alignment=Qt.AlignCenter)

        self.forward_button = QPushButton("Вперед ->")
        self.forward_button.setFixedSize(250, 40)
        self.forward_button.clicked.connect(self.button_right)
        buttons_layout.addWidget(self.forward_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(buttons_layout)

    # =============== Методы логики ===========================

    def get_data_names(self):
        folders = [entry.name for entry in os.scandir(self.path_to_data) if entry.is_dir()]
        return folders
    
    def change_dataset(self, text):
        self.pic_index = 1
        self.current_dataset = text
        self.set_left_image(f"{self.path_to_data}\{text}\{text}_1.jpg")

    def button_right(self):
        if self.current_dataset == "":
            return

        if self.pic_index + 1 >= 3000:
            self.pic_index = 1
        else:
            self.pic_index += 1
        
        text = self.current_dataset
        self.set_left_image(f"{self.path_to_data}\{text}\{text}_{self.pic_index}.jpg")

    def button_left(self):
        if self.current_dataset == "":
                    return

        if self.pic_index - 1 <= 0:
            self.pic_index = 3000
        else:
            self.pic_index -= 1
        
        text = self.current_dataset
        self.set_left_image(f"{self.path_to_data}\{text}\{text}_{self.pic_index}.jpg")

        
    def load_image_cv(self, path: str) -> QPixmap:
        # cv2 читает изображение в BGR
        img = cv2.imread(path)
        if img is None:
            print("OpenCV не смог открыть файл:", path)
            return QPixmap()  # null pixmap
        self.current_image = img
        return img

    def convert_cv_in_qt(self, img):
        # Конвертация BGR → RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w, ch = img.shape
        bytes_per_line = ch * w

        # Создаём QImage из numpy массива
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Конвертация QImage → QPixmap
        return QPixmap.fromImage(qimg)
        

    def set_left_image(self, path: str):
        """Устанавливает изображение слева."""        
        img = self.load_image_cv(path)
        pixmap = self.convert_cv_in_qt(img)
        self.image_left.setPixmap(
            pixmap.scaled(
                self.image_left.width(), self.image_left.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def set_right_image(self, img):
        """Устанавливает изображение справа."""
        self.image_right.setPixmap(
            img.scaled(
                self.image_right.width(), self.image_right.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def process(self):
        """Обработка данных."""
        #dataset = self.dataset_combo.currentText()
        #method = self.processing_combo.currentText()
        
        #print("Выбран набор данных:", dataset)
        #print("Выбран метод обработки:", method)
        processed_image = self.current_image
        for method in self.methods:
            processed_image = method.call_method(processed_image)
        #NoiseAugmentator.gaussian() 
        self.set_right_image(self.convert_cv_in_qt(processed_image))


        # Здесь будет твоя логика обработки
        # result = process_data(dataset, method)
        # self.set_right_image(result_path)
    