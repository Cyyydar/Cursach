import cv2
import numpy as np

class HistogramAugmentator:


    @staticmethod
    def equalize_channel(channel):
        ch_min = np.min(channel)
        ch_max = np.max(channel)


        if ch_max - ch_min < 1e-6:
            return channel.copy()

        ch_uint8 = cv2.normalize(channel, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')

        eq = cv2.equalizeHist(ch_uint8)

        eq = eq.astype(np.float64) / 255.0
        eq = eq * (ch_max - ch_min) + ch_min

        return eq.astype(channel.dtype)
    
    @staticmethod
    def statistical_channel(channel, target_mean=0.5, target_std=0.1):
        min_val, max_val = channel.min(), channel.max()

        ch_norm = (channel - min_val) / (max_val - min_val + 1e-8)

        mean = ch_norm.mean()
        std = ch_norm.std() + 1e-8

        ch_corr = (ch_norm - mean) / std * target_std + target_mean

        ch_corr = np.clip(ch_corr, 0, 1)

        ch_out = ch_corr * (max_val - min_val) + min_val
        return ch_out

    @staticmethod
    def equalize(img):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.equalizeHist(img)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        L, A, B = cv2.split(lab)
        L_eq = cv2.equalizeHist(L)
        lab_eq = cv2.merge([L_eq, A, B])
        return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

    @staticmethod
    def statistical(img: np.ndarray):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = img.astype(np.float32)
        means = img.mean(axis=(0, 1), keepdims=True)
        stds = img.std(axis=(0, 1), keepdims=True) + 1e-5

        target_mean = 128.0
        target_std = 50.0

        corrected = (img - means) / stds * target_std + target_mean
        corrected = np.clip(corrected, 0, 255).astype(np.uint8)

        return corrected
