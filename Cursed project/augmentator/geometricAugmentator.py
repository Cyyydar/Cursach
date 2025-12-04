import cv2
import numpy as np

class GeometricAugmentor:
    @staticmethod
    def scale(image, fx=1.0, fy=1.0):
        return cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def translate_rotate(image, tx=0, ty=0, angle=0):
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        M[0,2] += tx
        M[1,2] += ty
        return cv2.warpAffine(image, M, (w, h))

    @staticmethod
    def glass_effect(image, block_size=5):
        h, w = image.shape[:2]
        out = np.zeros_like(image)
        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                dx = np.random.randint(-block_size//2, block_size//2+1)
                dy = np.random.randint(-block_size//2, block_size//2+1)
                i_end = min(i+block_size, h)
                j_end = min(j+block_size, w)
                for c in range(image.shape[2]):
                    out[i:i_end, j:j_end, c] = np.roll(image[i:i_end, j:j_end, c], shift=(dy, dx), axis=(0,1))
        return out

    @staticmethod
    def motion_blur(image, size=15):
        kernel = np.zeros((size, size))
        kernel[size//2, :] = np.ones(size)
        kernel /= size
        return cv2.filter2D(image, -1, kernel)

    @staticmethod
    def wave1(image, amplitude=20, period=60):
        h, w = image.shape[:2]
        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        map_x = map_x + amplitude * np.sin(2 * np.pi * map_y / period)
        map_y = map_y.astype(np.float32)
        map_x = map_x.astype(np.float32)
        return cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def wave2(image, amplitude=20, period=30):
        h, w = image.shape[:2]
        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        map_x = map_x + amplitude * np.sin(2 * np.pi * map_x / period)
        map_y = map_y.astype(np.float32)
        map_x = map_x.astype(np.float32)
        return cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
