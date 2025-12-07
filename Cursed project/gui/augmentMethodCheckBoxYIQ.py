from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QDialog, QFormLayout, QDoubleSpinBox, QLabel
from PyQt5.QtCore import Qt
from gui.augmentMethodWidget import AugmentationMethodWidget
import cv2
import numpy as np

class AugmentationMethodCheckBoxYIQ(AugmentationMethodWidget):
    def __init__(self, name: str, method_callable, parameters: dict = None, on_change_callable=None):
        super().__init__(name, method_callable, parameters, on_change_callable)

    def create_param_window(self):
        super().create_param_window()
        self.Y_chbox = QCheckBox()
        self.Y_chbox.setChecked(True)
        self.Y_chbox.stateChanged.connect(self.on_change_callable)
        self.form.addRow(QLabel("Y"), self.Y_chbox)

        self.I_chbox = QCheckBox()
        self.I_chbox.setChecked(True)
        self.I_chbox.stateChanged.connect(self.on_change_callable)
        self.form.addRow(QLabel("I"), self.I_chbox)

        self.Q_chbox = QCheckBox()
        self.Q_chbox.setChecked(True)
        self.Q_chbox.stateChanged.connect(self.on_change_callable)
        self.form.addRow(QLabel("Q"), self.Q_chbox)

    def call_method(self, image):
        if not self.is_enabled():
            return image

        params = self.get_params()

        # Конвертация в YIQ
        yiq = self.rgb_to_yiq(image)

        # Применяем фильтр к выбранным каналам
        if self.Y_chbox.isChecked():
            yiq[:, :, 0] = self.method(yiq[:, :, 0], **params)
        if self.I_chbox.isChecked():
            yiq[:, :, 1] = self.method(yiq[:, :, 1], **params)
        if self.Q_chbox.isChecked():
            yiq[:, :, 2] = self.method(yiq[:, :, 2], **params)

        # Обратно в RGB
        return self.yiq_to_rgb(yiq)
    
    def rgb_to_yiq(self, img):
        rgb = img.astype(float) / 255
        matrix = np.array([
            [0.299,     0.587,     0.114],
            [0.596,    -0.275,    -0.321],
            [0.212,    -0.523,     0.311],
        ])
        yiq = rgb @ matrix.T
        return yiq
    
    def yiq_to_rgb(self, yiq):
        matrix = np.array([
            [1.000,  0.956,  0.621],
            [1.000, -0.272, -0.647],
            [1.000, -1.106,  1.703],
        ])
        rgb = yiq @ matrix.T
        rgb = np.clip(rgb * 255, 0, 255).astype(np.uint8)
        return rgb
