import cv2
import numpy as np

class GradientAugmentor:
    @staticmethod
    def sobel_unsharp(image, alpha=1.0):
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
        
        # Вычисляем градиенты по x и y
        Gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        Gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        
        gradient = np.sqrt(Gx**2 + Gy**2)
        gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX)
        
        # Применяем к каждому каналу
        result = image.astype(np.float32) + alpha * gradient[:, :, np.newaxis]
        result = np.clip(result, 0, 255).astype(np.uint8)
        return result

    @staticmethod
    def prewitt_unsharp(image, alpha=1.0):
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
        
        # Оператор Превитта
        kernelx = np.array([[1, 0, -1],[1, 0, -1],[1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1],[0, 0, 0],[-1, -1, -1]], dtype=np.float32)
        
        Gx = cv2.filter2D(gray, -1, kernelx)
        Gy = cv2.filter2D(gray, -1, kernely)
        
        gradient = np.sqrt(Gx**2 + Gy**2)
        gradient = cv2.normalize(gradient, None, 0, 255, cv2.NORM_MINMAX)
        
        result = image.astype(np.float32) + alpha * gradient[:, :, np.newaxis]
        result = np.clip(result, 0, 255).astype(np.uint8)
        return result
