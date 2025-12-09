import cv2
import numpy as np
from collections import Counter

class ColorRestorationAugmentor:
    @staticmethod
    def restore_color(gray_image, reference_images: list, neighborhood_size: int = 3, smoothing = True):
        h, w = gray_image.shape[:2]
        restored_image = np.zeros((h, w, 3), dtype=np.uint8)

        neighborhood_size = int(neighborhood_size)
        
        pad = neighborhood_size // 2
        
        # Подготовка паддинга для окрестности
        padded_refs = [cv2.copyMakeBorder(ref, pad, pad, pad, pad, cv2.BORDER_REFLECT) for ref in reference_images]
        
        for y in range(h):
            for x in range(w):
                intensity = gray_image[y, x].astype(np.int16)
                
                colors = []
                # Для каждого референсного изображения берем окрестность
                for ref in padded_refs:
                    neighborhood = ref[y:y+neighborhood_size, x:x+neighborhood_size, :]
                    # Выбираем пиксели, у которых средняя интенсивность близка к интенсивности текущего серого пикселя
                    gray_neigh = cv2.cvtColor(neighborhood, cv2.COLOR_BGR2GRAY)
                    mask = np.abs(gray_neigh.astype(np.int16) - intensity) <= 10  # допускаем небольшое расхождение
                    valid_colors = neighborhood[mask]
                    if valid_colors.size > 0:
                        colors.extend(valid_colors.tolist())
                
                if colors:
                    # Выбираем наиболее частый цвет
                    most_common_color = np.array(Counter([tuple(c) for c in colors]).most_common(1)[0][0], dtype=np.uint8)
                    restored_image[y, x] = most_common_color
                else:
                    # Если подходящего цвета нет - оставляем серое
                    restored_image[y, x] = np.full(3,intensity, dtype=np.uint8)
        
        if smoothing:
            restored_image = cv2.blur(restored_image, (3, 3))
        
        return restored_image
