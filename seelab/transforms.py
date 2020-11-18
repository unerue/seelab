from PIL import Image
from torchvision import transforms
import torchvision.transforms.functional as TF


class Compose:
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, image, boxes=None, masks=None, labels=None):
        for transform in self.transforms:
            image, masks, boxes, labels = transform(
                image, masks, boxes, labels)

        return image, boxes, masks, labels


class Resize:
    def __init__(self, size, interpolation=Image.BILINEAR):
        self.size = size
        self.interpolation = interpolation

    def __call__(self, image, boxes=None, masks=None, labels=None):
        w, h = image.size
        image = image.resize(self.size)
        masks = TF.resize(masks, self.size, self.interpolation)

        boxes[:, [0, 2]] *= self.size[0] / w
        boxes[:, [1, 3]] *= self.size[1] / h

        return image, boxes, masks, labels
        

class HorizontalFlip:
    def __init__(self):
        pass

    def __call__(self, image, boxes=None, masks=None, labels=None):
        image = image[::-1, :]
        masks = masks[:, ::-1, :]
        boxes = boxes.copy()
        
        return image, boxes, masks, labels
