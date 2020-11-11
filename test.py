# from utils import _mask_to_box
from seelab.visualize import get_labelme_annotations


print(get_labelme_annotations('00000178.json')['boxes'])
