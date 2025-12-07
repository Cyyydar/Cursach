import cv2
import numpy as np

class YIQChannelFilter:
    def __init__(self, filter_callable, apply_Y=False, apply_I=False, apply_Q=False):
        self.filter = filter_callable
        self.apply_Y = apply_Y
        self.apply_I = apply_I
        self.apply_Q = apply_Q

    def __call__(self, image, **params):
        Y, I, Q = self.bgr_to_yiq(image)

        if self.apply_Y:
            Y = self.filter(Y, **params)
        if self.apply_I:
            I = self.filter(I, **params)
        if self.apply_Q:
            Q = self.filter(Q, **params)

        return self.yiq_to_bgr(Y, I, Q)
    
    @staticmethod
    def bgr_to_yiq(img):
        img = img.astype("float32") / 255.0
        B, G, R = cv2.split(img)

        Y = 0.299*R + 0.587*G + 0.114*B
        I = 0.596*R - 0.275*G - 0.321*B
        Q = 0.212*R - 0.523*G + 0.311*B

        return Y, I, Q
    
    @staticmethod
    def yiq_to_bgr(Y, I, Q):
        R = Y + 0.956*I + 0.621*Q
        G = Y - 0.272*I - 0.647*Q
        B = Y - 1.105*I + 1.702*Q

        img = cv2.merge([B, G, R])
        img = np.clip(img*255, 0, 255).astype("uint8")
        return img