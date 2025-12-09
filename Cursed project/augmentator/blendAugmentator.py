import cv2
import numpy as np

class ImageBlender:
    @staticmethod
    def blend_patch(patch1, patch2, alpha=0.5, blend_width=0):
        if blend_width == 0:
            return cv2.addWeighted(patch1, alpha, patch2, 1 - alpha, 0)
        else:
            h, w, _ = patch1.shape
            yy, xx = np.ogrid[:h, :w]
            dist = np.minimum(np.minimum(yy, h-1-yy), np.minimum(xx, w-1-xx)).astype(np.float32)
            mask = np.clip(dist / float(blend_width), 0.0, 1.0)
            return np.clip(patch1 * mask[...,None] + patch2 * (1 - mask[...,None]), 0, 255).astype(np.uint8)
    
    @staticmethod
    def blend_randomly(img1, img2, size=16, alpha=0.5, blend_width=0):
        out = img1.copy()
        h_img, w_img, _ = img1.shape
        h_patch = w_patch = int(size)
        blend_width = int(np.clip(blend_width, 0, min(h_patch,w_patch)-1))

        for i in range(0, h_img, h_patch):
            for j in range(0, w_img, w_patch):
                i_end = min(i + h_patch, h_img)
                j_end = min(j + w_patch, w_img)

                patch1 = img1[i:i_end, j:j_end]
                patch2 = img2[i:i_end, j:j_end]

                use_patch2 = False
                use_patch2 = np.random.rand() > 0.5

                if use_patch2:
                    blended_patch = ImageBlender.blend_patch(patch1, patch2, alpha, blend_width)
                    out[i:i_end, j:j_end] = blended_patch

        return out

    @staticmethod
    def blend_chessboard(img1, img2, size=16, alpha=0.5, blend_width=0):
        out = img1.copy()
        h_img, w_img, _ = img1.shape
        h_patch = w_patch = int(size)
        blend_width = int(np.clip(blend_width, 0, min(h_patch,w_patch)-1))

        for i in range(0, h_img, h_patch):
            for j in range(0, w_img, w_patch):
                i_end = min(i + h_patch, h_img)
                j_end = min(j + w_patch, w_img)

                patch1 = img1[i:i_end, j:j_end]
                patch2 = img2[i:i_end, j:j_end]

                use_patch2 = False
                row_flag = (i // h_patch) % 2
                col_flag = (j // w_patch) % 2
                use_patch2 = (row_flag + col_flag) % 2 == 1

                if use_patch2:
                    blended_patch = ImageBlender.blend_patch(patch1, patch2, alpha, blend_width)
                    out[i:i_end, j:j_end] = blended_patch

        return out