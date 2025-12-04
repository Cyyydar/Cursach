import cv2
import numpy as np

class HistogramAugmentator:

    @staticmethod
    def equalize(img):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        L, A, B = cv2.split(lab)
        L_eq = cv2.equalizeHist(L)
        lab_eq = cv2.merge([L_eq, A, B])
        return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    @staticmethod
    def statistical(img: np.ndarray):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = img.astype(np.float32)
        means = img.mean(axis=(0, 1), keepdims=True)
        stds = img.std(axis=(0, 1), keepdims=True) + 1e-5

        target_mean = 128.0
        target_std = 50.0

        corrected = (img - means) / stds * target_std + target_mean
        corrected = np.clip(corrected, 0, 255).astype(np.uint8)

        return corrected
