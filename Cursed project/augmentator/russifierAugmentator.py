import cv2
import numpy as np
class RussifierAugmentor:
    @staticmethod
    def russifier(img, alpha: float = 0.5) -> np.ndarray:
        """
        Красит изображение в цвета российского флага.
        
        :param img: входное изображение в формате BGR (OpenCV)
        :param alpha: прозрачность наложения (0.0-1.0)
        :return: изображение с наложением флага
        """
        # Размеры изображения
        height, width = img.shape[:2]

        # Создаем флаг того же размера
        flag = np.zeros_like(img, dtype=np.uint8)

        # Высота каждой полосы
        stripe_height = height // 3

        # Белая полоса (сверху)
        flag[0:stripe_height, :] = (255, 255, 255)  # BGR
        # Синяя полоса (середина)
        flag[stripe_height:stripe_height*2, :] = (166, 57, 0)  # BGR (синий)
        # Красная полоса (снизу)
        flag[stripe_height*2:, :] = (30, 43, 213)  # BGR (красный)

        # Накладываем флаг с прозрачностью alpha
        russified = cv2.addWeighted(img, 1 - alpha, flag, alpha, 0)

        return russified
