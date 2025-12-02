import cv2
import numpy as np

class NoiseAugmentator():
    
    @staticmethod
    def gaussian(image, mean=0, std=15):
        """Шум Гаусса с использованием OpenCV снизу."""
        noise = np.random.normal(mean, std, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)

    @staticmethod
    def rayleigh(image, scale=20):
        """Шум Релея."""
        noise = np.random.rayleigh(scale, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)

    @staticmethod
    def exponential(image, lam=0.02):
        """Экспоненциальный шум."""
        noise = np.random.exponential(1.0 / lam, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)
