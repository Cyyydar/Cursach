import cv2
import numpy as np


class DenoiseAugmentor:

    @staticmethod
    def average(img: np.ndarray, ksize: int = 3) -> np.ndarray:
        ksize = int(ksize)
        if ksize % 2 == 0:
            raise ValueError("ksize должен быть нечетным")

        return cv2.blur(img, (ksize, ksize))

    @staticmethod
    def gaussian(img: np.ndarray, ksize: int = 3, sigma: float = 0) -> np.ndarray:
        ksize = int(ksize)
        if ksize % 2 == 0:
            raise ValueError("ksize должен быть нечетным")

        return cv2.GaussianBlur(img, (ksize, ksize), sigma)

    @staticmethod
    def median(img: np.ndarray, ksize: int = 3) -> np.ndarray:
        ksize = int(ksize)
        if ksize % 2 == 0:
            raise ValueError("ksize должен быть нечетным")

        return cv2.medianBlur(img, ksize)
