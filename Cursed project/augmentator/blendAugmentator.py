import cv2
import numpy as np

class ImageBlender:
    @staticmethod
    def blend_patch(patch1, patch2, alpha=0.5, blend_width=0):
        """
        Линейное смешение двух патчей с возможной границей сглаживания
        :param patch1, patch2: патчи BGR numpy array одинакового размера
        :param alpha: коэффициент смешивания
        :param blend_width: ширина границы плавного смешения
        :return: смешанный патч
        """
        if blend_width == 0:
            return cv2.addWeighted(patch1, alpha, patch2, 1 - alpha, 0)
        else:
            # создаём маску для границы
            h, w, _ = patch1.shape
            mask = np.ones((h, w), dtype=np.float32) * alpha
            # линейное уменьшение alpha в границе
            for i in range(blend_width):
                factor = (i + 1) / blend_width
                mask[i, :] = alpha * factor + (1 - factor) * alpha
                mask[-i-1, :] = alpha * factor + (1 - factor) * alpha
                mask[:, i] = alpha * factor + (1 - factor) * alpha
                mask[:, -i-1] = alpha * factor + (1 - factor) * alpha
            mask = mask[:, :, np.newaxis]
            return np.clip(patch1 * mask + patch2 * (1 - mask), 0, 255).astype(np.uint8)

    @staticmethod
    def blend_images(img1, img2, patch_size=(50, 50), alpha=0.5, blend_width=0, mode="random"):
        """
        Смешение двух изображений
        :param img1, img2: изображения BGR numpy array одинакового размера
        :param patch_size: размер патча (h, w)
        :param alpha: коэффициент смешивания
        :param blend_width: толщина границы смешения
        :param mode: "random" или "chessboard"
        :return: смешанное изображение
        """
        out = img1.copy()
        h_img, w_img, _ = img1.shape
        h_patch, w_patch = patch_size

        for i in range(0, h_img, h_patch):
            for j in range(0, w_img, w_patch):
                i_end = min(i + h_patch, h_img)
                j_end = min(j + w_patch, w_img)

                patch1 = img1[i:i_end, j:j_end]
                patch2 = img2[i:i_end, j:j_end]

                use_patch2 = False
                if mode == "random":
                    use_patch2 = np.random.rand() > 0.5
                elif mode == "chessboard":
                    row_flag = (i // h_patch) % 2
                    col_flag = (j // w_patch) % 2
                    use_patch2 = (row_flag + col_flag) % 2 == 1

                if use_patch2:
                    blended_patch = ImageBlender.blend_patch(patch1, patch2, alpha, blend_width)
                    out[i:i_end, j:j_end] = blended_patch

        return out
