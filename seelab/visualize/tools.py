import json
from collections import defaultdict
from typing import Tuple, List, Dict

# import pyximport
import numpy as np
from PIL import Image
# from pycocotools.coco import COCO
from ._cython_utils import mask_to_box
# from ._cython_utils import _mask_to_box


def get_coco_annotations(path: str, xywh: bool = True) -> Dict:
    """
    Arguments:
    Returns:
    TODO
        pycocotools
    """
    raise NotImplementedError


def get_labelme_annotations(path: str, xywh: bool = True) -> Dict:
    """Get annotaions from labelme format

    labelme polygon annotation has nested list [[x, y], [x, y],...,[]]
    Arguments:
        path: str read only json file
        xywh: bool
    Returns:
        Dict:
            boxes:
            polygons:
    """
    # {'include_dirs': np.get_include()},
    # pyximport.install(
    #     setup_args={'include_dirs': [np.get_include()]},
    #     reload_support=True, language_level='3', inplace=True)
    # from .cython_utils import _mask_to_box

    with open(path) as json_file:
        shapes = json.load(json_file)

    polygons = []
    for shape in shapes['shapes']:
        polygons.append({
            'group_id': shape['group_id'],
            'label': shape['label'],
            'points': shape['points']})

    boxes = []
    polygons_by_id = defaultdict(list)
    labels_by_id = defaultdict(list)
    for shape in polygons:
        if shape['group_id'] is None:
            box = mask_to_box(np.array(shape['points']), xywh)

            boxes.append({
                'group_id': shape['group_id'],
                'label': shape['label'],
                'points': box})
        else:
            polygons_by_id[shape['group_id']] += shape['points']
            labels_by_id[shape['group_id']] = shape['label']

    for k, v in polygons_by_id.items():
        box = mask_to_box(np.array(v), xywh)

        boxes.append({
            'group_id': k,
            'label': labels_by_id[k],
            'points': box})

    return {'boxes': boxes, 'polygons': polygons}


def rgb_to_rgba(rgb: Tuple, alpha: float = 0.3) -> Tuple:
    """
    Arguments:
        rgb (Tuple): (255, 255, 255)
        alpha (float): 0 ~ 1
    Returns:
        rgba (Tuple): ((0.0, 0.0, 0.0), 0.3)
    """
    rgb = np.asarray(rgb) / 255.
    c1 = np.insert(rgb, len(rgb), alpha).round(2)
    c2 = np.insert(rgb, len(rgb), 1.).round(2)
    return (tuple(c1), tuple(c2))


# def png_to_jpg(path):
#     # jpg파일을 저장하기 위한 디렉토리의 생성
#     if not os.path.exists(path+'_jpg'):
#         os.mkdir(path+'_jpg') 

#     # 모든 png 파일의 절대경로를 저장
#     all_image_files=glob.glob(path+'/*.png') 

#     for file_path in all_image_files:                   # 모든 png파일 경로에 대하여
#         img = Image.open(file_path).convert('RGB')  # 이미지를 불러온다.

#         directories=file_path.split('/')                # 절대경로상의 모든 디렉토리를 얻어낸다.
#         directories[-2]+='_jpg'                     # 저장될 디렉토리의 이름 지정
#         directories[-1]=directories[-1][:-4]+'.jpg'  # 저장될 파일의 이름 지정
#         save_filepath='/'.join(directories)          # 절대경로명으로 바꾸기
#         img.save(save_filepath, quality=85)       # jpg파일로 저장한다.
