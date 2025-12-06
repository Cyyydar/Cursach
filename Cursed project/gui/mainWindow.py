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
from gui.augmentMethodRadioButton import AugmentationMethodRadio, AugmentationMethodGroup

from augmentator.noiseAugmentator import NoiseAugmentator
from augmentator.denoiseAugmentator import DenoiseAugmentor
from augmentator.historgamAugmentator import HistogramAugmentator
from augmentator.colorTransformAugmetnator import ColorTransformAugmentor
from augmentator.colorRestorationAugmentator import ColorRestorationAugmentor
from augmentator.gradientAugmentator import GradientAugmentor
from augmentator.geometricAugmentator import GeometricAugmentor
from augmentator.blendAugmentator import ImageBlender
from augmentator.russifierAugmentator import RussifierAugmentor

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

        images_layout.addWidget(self.dataset_combo)

        # Методы аугментации
        self.methods = []

        # Шум
        noise_box = QVBoxLayout()
        noise_box.setAlignment(Qt.AlignTop)
        
        noise_label = QLabel("Зашумление")
        noise_box.addWidget(noise_label)
        methods = [AugmentationMethodWidget("Гаусс", NoiseAugmentator.gaussian, {"mean": (0, -50, 50, 1), "std": (10, 0, 100, 1)}),
                         AugmentationMethodWidget("Релей", NoiseAugmentator.rayleigh, {"scale": (20, -50, 50, 1)}),
                         AugmentationMethodWidget("Экспоненциальный шум", NoiseAugmentator.exponential, {"lam": (0.02, -50, 50, 0.01)})
                         ]
        for method in methods:
            self.methods.append(method)
            noise_box.addWidget(method)
        methods.clear()
        controls_layout.addLayout(noise_box)

        # Удаление шума

        denoise_box = QVBoxLayout()
        denoise_box.setAlignment(Qt.AlignTop)
        
        denoise_label = QLabel("Удаление шума")
        denoise_box.addWidget(denoise_label)
        methods = [AugmentationMethodWidget("Усреднение", DenoiseAugmentor.average, {"ksize": (3, -11, 11, 2)}),
                         AugmentationMethodWidget("Фильтр Гаусса", DenoiseAugmentor.gaussian, {"ksize": (3, -11, 11, 2), "sigma": (0, -10, 10, 1)}),
                         AugmentationMethodWidget("Медианный фильтр", DenoiseAugmentor.median, {"ksize": (3, -11, 11, 2)})
                         ]
        for method in methods:
            self.methods.append(method)
            denoise_box.addWidget(method)
        methods.clear()
        controls_layout.addLayout(denoise_box)

        # Преобразование на основе гистограммы RGB

        rgb_box = QVBoxLayout()
        rgb_box.setAlignment(Qt.AlignTop)
        
        rgb_box.addWidget(QLabel("Преобразование на основе гистограммы RGB"))
        methods = [AugmentationMethodWidget("Эквализация", HistogramAugmentator.equalize),
                         AugmentationMethodWidget("Статическая цветокоррекция", HistogramAugmentator.statistical),
                         ]
        for method in methods:
            self.methods.append(method)
            rgb_box.addWidget(method)
        methods.clear()
        controls_layout.addLayout(rgb_box)

        # Преобразование цветности

        color_box = QVBoxLayout()
        color_box.setAlignment(Qt.AlignTop)
        
        color_box.addWidget(QLabel("Преобразование цветности"))
        group = AugmentationMethodGroup("stas", [AugmentationMethodRadio("В серый", ColorTransformAugmentor.to_gray),
                    AugmentationMethodRadio("В бинарный", ColorTransformAugmentor.to_binary, {"threshold": (127, 0, 255, 1)}),
                         ])
        color_box.addWidget(group)
        self.methods.append(group)
        controls_layout.addLayout(color_box)

        # Восстановление цветности
        controls_layout2 = QHBoxLayout()
        controls_layout2.setAlignment(Qt.AlignCenter)
        
        rcolor_box = QVBoxLayout()
        rcolor_box.setAlignment(Qt.AlignTop)
        
        rcolor_box.addWidget(QLabel("Восстановление цветности"))
        methods = [AugmentationMethodWidget("Восстановление цветности", ColorRestorationAugmentor.restore_image)
                         ]
        for method in methods:
            self.methods.append(method)
            rcolor_box.addWidget(method)
        methods.clear()
        controls_layout2.addLayout(rcolor_box)

        # Градиенты изображения

        grad_box = QVBoxLayout()
        grad_box.setAlignment(Qt.AlignTop)
        
        grad_box.addWidget(QLabel("Градиенты изображения"))
        methods = [AugmentationMethodWidget("Оператор Собеля", GradientAugmentor.sobel_unsharp, {"alpha": (1, -10, 10, 1)}),
                         AugmentationMethodWidget("Оператор Превитта", GradientAugmentor.prewitt_unsharp, {"alpha": (1, -10, 10, 1)}),
                         ]
        for method in methods:
            self.methods.append(method)
            grad_box.addWidget(method)
        methods.clear()
        controls_layout2.addLayout(grad_box)

        # Смешение изображений

        blend_box = QVBoxLayout()
        blend_box.setAlignment(Qt.AlignTop)
    
        blend_box.addWidget(QLabel("Смешение изображений"))
        methods = [AugmentationMethodWidget("Эквализация", DenoiseAugmentor.average, {"ksize": (3, -10, 10, 2)}),
                         AugmentationMethodWidget("Статическая цветокоррекция", DenoiseAugmentor.gaussian, {"ksize": (3, -10, 10, 2), "sigma": (0, -10, 10, 1)}),
                         ]
        for method in methods:
            self.methods.append(method)
            blend_box.addWidget(method)
        methods.clear()
        controls_layout2.addLayout(blend_box)

        # Геометрические преобразования

        geom_box = QVBoxLayout()
        geom_box.setAlignment(Qt.AlignTop)
        
        geom_box.addWidget(QLabel("Геометрические преобразования"))
        methods = [AugmentationMethodWidget("Масштабирование", GeometricAugmentor.scale, {"fx": (2, 0, 10, 1), "fy": (2, 0, 10, 1)}),
                         AugmentationMethodWidget("Перенос/Поворот", GeometricAugmentor.translate_rotate, {"tx": (1, -10, 10, 1), "ty": (1, -10, 10, 1), "angle": (90, -360, 360, 15)}),
                         AugmentationMethodWidget("Эффект \"Стекла\"", GeometricAugmentor.glass_effect),
                         AugmentationMethodWidget("Motion blur", GeometricAugmentor.motion_blur),
                         AugmentationMethodWidget("Волна 1", GeometricAugmentor.wave1),
                         AugmentationMethodWidget("Волна 2", GeometricAugmentor.wave2),
                         ]
        for method in methods:
            self.methods.append(method)
            geom_box.addWidget(method)
        methods.clear()
        controls_layout2.addLayout(geom_box)


        # Одно наше преорабзование пока хз какое

        our_box = QVBoxLayout()
        our_box.setAlignment(Qt.AlignTop)
        
        our_box.addWidget(QLabel("Русификатор изображения"))
        methods = [AugmentationMethodWidget("Русификация", RussifierAugmentor.russifier, {"alpha": (0.5, 0, 1, 0.1)})
                         ]
        for method in methods:
            self.methods.append(method)
            our_box.addWidget(method)
        methods.clear()
        controls_layout2.addLayout(our_box)




        main_layout.addLayout(controls_layout)
        main_layout.addLayout(controls_layout2)

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
    