import cv2
import os
import random
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QPushButton, 
    QDialog, QFormLayout, QDoubleSpinBox, QLabel, QButtonGroup
)
from gui.augmentMethodRadioButton import AugmentationMethodRadio
from PyQt5.QtCore import Qt

class AugmentationMethodBlendRadioButton(AugmentationMethodRadio):
    def __init__(self, name, method_callable, parameters = None, on_change_callable=None):
        super().__init__(name, method_callable, parameters, on_change_callable)
    
    def change_folder(self, path):
        self.img_path = path
        self.files = [f for f in os.listdir(self.img_path) 
                      if f.lower().endswith(('.jpg', '.png'))]



    def call_method(self, image):
        path = os.path.join(self.img_path, random.choice(self.files))
        img = cv2.imread(path)
        if self.is_enabled():
            params = self.get_params()
            return self.method(image, img, **params)
        return image
        #return super().call_method(image)
