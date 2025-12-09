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

        pad = ksize // 2

        # паддинг по краям
        padded = np.pad(img, pad, mode='edge')

        H, W = img.shape
        window_size = ksize * ksize

        # массив всех окон (H, W, ksize*ksize)
        windows = np.empty((H, W, window_size), dtype=img.dtype)

        idx = 0
        for dy in range(ksize):
            for dx in range(ksize):
                windows[:, :, idx] = padded[dy:dy+H, dx:dx+W]
                idx += 1

        # медиана по последнему измерению
        return np.median(windows, axis=2).astype(img.dtype)
