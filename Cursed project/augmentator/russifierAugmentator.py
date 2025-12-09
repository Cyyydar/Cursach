import cv2
import numpy as np
class RussifierAugmentor:
    @staticmethod
    def russifier(img, alpha: float = 0.5) -> np.ndarray:
        # Размеры изображения
        height, width = img.shape[:2]

        # Создаем флаг того же размера
        flag = np.zeros_like(img, dtype=np.uint8)

        # Высота каждой полосы
        stripe_height = height // 3

        # Белая полоса
        flag[0:stripe_height, :] = (255, 255, 255)
        # Синяя полоса
        flag[stripe_height:stripe_height*2, :] = (166, 57, 0)
        # Красная полоса
        flag[stripe_height*2:, :] = (30, 43, 213)

        # Накладываем флаг с прозрачностью alpha
        russified = cv2.addWeighted(img, 1 - alpha, flag, alpha, 0)

        return russified
