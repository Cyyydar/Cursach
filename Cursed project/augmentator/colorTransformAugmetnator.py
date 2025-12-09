import cv2
import numpy as np

class ColorTransformAugmentor:
    @staticmethod
    def to_gray(image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) # Переводим обратно, чтобы не конфликтовать с другими методами

    @staticmethod
    def to_binary(image, threshold=127):
        gray = ColorTransformAugmentor.to_gray(image)

        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return binary