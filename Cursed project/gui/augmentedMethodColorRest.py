import cv2
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QPushButton, QFileDialog,
    QDialog, QFormLayout, QDoubleSpinBox, QLabel, QButtonGroup
)
from gui.augmentMethodWidget import AugmentationMethodWidget

class AugmentationMethodColorRestoration(AugmentationMethodWidget):
    def __init__(self, name, method_callable, parameters = None, on_change_callable=None):
        super().__init__(name, method_callable, parameters, on_change_callable)
        self.button.stateChanged.disconnect()
        self.button.stateChanged.connect(self.choose_img)

    def choose_img(self, state):
        if state:
            self.path_to_img = QFileDialog.getOpenFileNames(self, "Выберите изображение", "", "Images(*.png, *jpg)")
            print(self.path_to_img)
            self.imgs = []
            for path in self.path_to_img[0]:
                self.imgs.append(cv2.imread(path))
        self._trigger()

    def call_method(self, image):
        if self.is_enabled():
            params = self.get_params()
            return self.method(image, self.imgs, **params)
        return image
