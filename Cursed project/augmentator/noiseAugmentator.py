import cv2
import numpy as np

class NoiseAugmentator():
    
    @staticmethod
    def gaussian_channel(channel, mean=0.0, std=0.05):
        ch_range = channel.max() - channel.min()
        noise = np.random.normal(mean, ch_range * std, channel.shape)
        ch_noisy = channel + noise
    
        ch_noisy = np.clip(ch_noisy, channel.min(), channel.max())
        return ch_noisy
    
    @staticmethod
    def rayleigh_channel(channel, scale=0.05):
        ch_range = channel.max() - channel.min()
        noise = np.random.rayleigh(scale=ch_range * scale, size=channel.shape)
        
        noise = noise - noise.mean()
        
        ch_noisy = channel + noise
        ch_noisy = np.clip(ch_noisy, channel.min(), channel.max())
        return ch_noisy
    
    @staticmethod
    def exponential_channel(channel, scale=0.05):
        ch_range = channel.max() - channel.min()
        noise = np.random.exponential(scale=ch_range * scale, size=channel.shape)
        
        noise = noise - noise.mean()
        
        ch_noisy = channel + noise
        ch_noisy = np.clip(ch_noisy, channel.min(), channel.max())
        return ch_noisy

    @staticmethod
    def gaussian(image, mean=0, std=15):
        noise = np.random.normal(mean, std, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)

    @staticmethod
    def rayleigh(image, scale=20):
        noise = np.random.rayleigh(scale, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)

    @staticmethod
    def exponential(image, scale=0.02):
        noise = np.random.exponential(1.0 / scale, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        return np.clip(noisy, 0, 255).astype(np.uint8)
