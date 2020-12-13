from typing import Tuple
import cv2
import numpy as np
from torch import Tensor


class AddDarkness:
    """Add darkness

    Argument:
        gamma (float): Darkness coefficient
        
    Returns:
        image (numpy.ndarray)
        mask (Tensor)
        boxes (Tensor)
        labels (Tensor)
    """
    def __init__(self, gamma: float = 0.9):
        if gamma >= 0.99:
            self.gamma = 0.99
        elif gamma <= 0.5:
            self.gamma = 0.5
        else:
            self.gamma = gamma
    
    def __call__(
        self, image: np.ndarray, masks: Tensor = None, boxes: Tensor = None, labels: Tensor = None) -> Tuple:
        image = np.array(image)[...,  ::-1]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS) 
        image[...,  1] = image[...,  1] * self.gamma
        image[...,  1][image[...,  1] > 255] = 255

        image = image.astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_HLS2RGB)
        
        return image, masks, boxes, labels


class AddBrightness:
    """Add brigntness

    Argument:
        gamma (float): Brightness coefficient
    """
    def __init__(self, gamma: float = 1.5):
        if gamma >= 1.5:
            self.gamma = 1.5
        elif gamma <= 1.01:
            self.gamma = 1.01
        else:
            self.gamma = gamma
    
    def __call__(self, image, masks=None, boxes=None, labels=None) -> Tuple:
        image = np.array(image)[...,  ::-1]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        image = image.astype(np.float64)
        
        image[...,  1] = image[...,  1] * self.gamma
        image[...,  1][image[...,  1] > 255]  = 255
        
        image = image.astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_HLS2RGB)
        
        return image, masks, boxes, labels


class AddSnow:
    """Add snow

    Arguments:
        gamma (float):
        snow_points (int): Number of points 
    """
    def __init__(self, gamma: float = 2.5):
        self.gamma = gamma
        self.snow_points = 100

    def __call__(self, image, masks=None, boxes=None, labels=None):
        image = np.array(image)[..., ::-1]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

        image[..., 1][image[..., 1] < self.snow_points] =\
            image[...,  1][image[...,  1] < self.snow_points] * self.gamma

        image[...,  1][image[..., 1] > 255]  = 255

        image = image.astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_HLS2RGB)
        
        return image, masks, boxes, labels


class AddRain:
    """Add rain

    Arguments:
        gamma (int)
        slant_extreme (int)
        drop_length (int)
        drop_width (int)
        drop_color (Tuple[int])
        brightness_coef (float)
    """
    def __init__(
        self, 
        gamma: int = 1500, 
        slant_extreme: int = 10, 
        drop_length: int = 20, 
        drop_width: int = 2, 
        drop_color: Tuple[int] = (200, 200, 200), 
        brightness_coef: float = 0.7):

        self.gamma = gamma
        self.slant_extreme = slant_extreme
        self.drop_length = drop_length    
        self.drop_width = drop_width
        self.drop_color = drop_color
        self.brightness_coef = brightness_coef
    
    def __call__(self, image, masks=None, boxes=None, labels=None) -> Tuple:
        image = np.array(image)
        image_shape = image.shape
        slant = np.random.randint(-self.slant_extreme, self.slant_extreme)
        drops = []
        for _ in range(self.gamma):
            if slant < 0:
                x = np.random.randint(slant, image_shape[1])
            else:
                x = np.random.randint(0, image_shape[1] - slant)
            y = np.random.randint(0, image_shape[0] - self.drop_length)       
            drops.append((x, y))
            
        for drop in drops:
            cv2.line(
                image, 
                (drop[0], drop[1]), 
                (drop[0] + slant, drop[1] + self.drop_length), 
                self.drop_color, 
                self.drop_width)    
            
        image = cv2.blur(image, (7, 7))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        image[...,  1] = image[...,  1] * self.brightness_coef
        image = cv2.cvtColor(image, cv2.COLOR_HLS2RGB)
           
        return image, masks, boxes, labels