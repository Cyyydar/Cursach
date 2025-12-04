import cv2
import numpy as np
from scipy.stats import mode

class ColorRestorationAugmentor:
    def __init__(self, reference_images):
        """
        :param reference_images: список эталонных изображений (BGR, numpy array)
        """
        self.references_bgr = reference_images
        self.references_lab = [cv2.cvtColor(img, cv2.COLOR_BGR2LAB) for img in reference_images]

    def restore_pixel(self, x, y, intensity, neighborhood=1):
        """
        Восстановление цвета для одного пикселя по интенсивности.
        :param x, y: координаты пикселя в изображении
        :param intensity: L-канал исходного пикселя
        :param neighborhood: размер окрестности для статистики (по умолчанию 1)
        :return: BGR цвет
        """
        colors = []

        for ref_bgr, ref_lab in zip(self.references_bgr, self.references_lab):
            L_ref, _, _ = cv2.split(ref_lab)
            
            # Ограничиваем границы окна окрестности
            h, w = L_ref.shape
            x_min = max(x - neighborhood, 0)
            x_max = min(x + neighborhood + 1, h)
            y_min = max(y - neighborhood, 0)
            y_max = min(y + neighborhood + 1, w)

            # Берём патч яркости и маску пикселей с нужной интенсивностью
            patch_L = L_ref[x_min:x_max, y_min:y_max]
            mask = (patch_L == intensity)

            if np.any(mask):
                patch_colors = ref_bgr[x_min:x_max, y_min:y_max][mask]
                colors.extend(patch_colors)

        if colors:
            colors_array = np.array(colors)
            most_common = mode(colors_array, axis=0)[0][0]
            return most_common
        else:
            # Если не найдено совпадений — возвращаем серый
            return np.array([intensity]*3, dtype=np.uint8)

    def restore_image(self, src_image, neighborhood=1, smoothing=True):
        """
        Восстановление цвета всего изображения.
        :param src_image: BGR изображение numpy array
        :param neighborhood: размер окрестности
        :param smoothing: применять сглаживание после восстановления
        :return: восстановленное BGR изображение
        """
        lab_src = cv2.cvtColor(src_image, cv2.COLOR_BGR2LAB)
        L_channel, _, _ = cv2.split(lab_src)

        restored = np.zeros_like(src_image)

        h, w = L_channel.shape
        for i in range(h):
            for j in range(w):
                intensity = L_channel[i, j]
                restored[i, j] = self.restore_pixel(i, j, intensity, neighborhood)

        if smoothing:
            restored = cv2.GaussianBlur(restored, (3, 3), 0)

        return restored
