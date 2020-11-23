import sys
import json
import os
import random
import argparse
import math
import tqdm
from collections import defaultdict
from typing import Any, Callable, TypeVar

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection

import pycocotools
from pycocotools import mask


class Visualizer:
    def __init__(self, image_dir: str, info_path: str, num_images: int, annot_type: str):
        self.image_dir = image_dir
        self.info_path = info_path
        self.num_images = num_images
        self.annot_type = annot_type.split(',')

        with open(self.info_path, 'r') as json_file:
            self.annots = json.load(json_file)

        self.classes = {v['id']: v['name'] for v in self.annots['categories']}
        raise NotImplementedError

    def get_label_and_color(self, alpha=1.0):
        label = self.classes
        return NotImplementedError
        
F = TypeVar('F', bound=Callable[..., Any])


def color_cache(func: F) -> F:
    cached_colors = defaultdict()
    def wrapping_function(*args):
        k, v = func(*args)
        if k not in cached_colors:
            cached_colors[k] = v
        return k, cached_colors[k]
    return wrapping_function


@color_cache
def get_label_color_map(category_id, classes):
    label = classes[category_id]
    color = tuple(round(random.random(), 3) for _ in range(3))
    mask = color + (.5,)
    bbox = color + (1.,)
    colors = (mask, bbox)
    return label, colors


def draw_ground_truth(annots, image_id=None, ax=None, annot_type='bbox', classes=None):
    for annot in annots['annotations']:
        if annot['image_id'] == image_id:
            if annot_type == 'bbox':
                draw_bbox(ax, annot, classes)


def draw_bbox(ax, annot, classes):
    label, color = get_label_color_map(annot['category_id'], classes)
    box = annot['bbox']
    # if color is None:
    # color = ((0.96, 0.26, 0.21, 0.2), (0.96, 0.26, 0.21, 1.0))
    ractangle = Rectangle((box[0], box[1]), box[2], box[3], fill=None, ec=color[1])
    ax.add_patch(ractangle)
    ax.annotate(
        label, (box[0], box[1]), color='w', weight='bold', 
        fontsize=3, ha='left', va='bottom',
        bbox=dict(facecolor=color[1], edgecolor=color[1], pad=0.0))


def visualize_coco(image_dir, info_path, num_images):
    if num_images > 9:
        raise ValueError

    with open(info_path, 'r') as json_file:
        annots = json.load(json_file)
    
    classes = {v['id']: v['name'] for v in annots['categories']}
    images = {annot['id']: annot['file_name'] for annot in annots['images']}
    
    shuffle = True
    if shuffle:
        shuffled_ids = list(images.keys())
        random.shuffle(shuffled_ids)
    
    images = {key: images[key] for key in shuffled_ids}

    # fig, axes = plt.subplots(2, 2, dpi=50)
    # print(math.gcd(10, 4))
    sizes = [i for i in range(1, num_images+1) if num_images % i == 0]
    figsize = []
    for i in range(len(sizes), 0, -1):
        for j in range(i, len(sizes)):
            if sizes[i] * sizes[j] == num_images:
                figsize.append((sizes[i], sizes[j]))
            if len(figsize) > 1:
                break
                
    try:
        row, col = figsize[0]
    except IndexError:
        row, col = 1, num_images
    
    fig = plt.figure(dpi=200)
    dpi = fig.get_dpi()
   
    for i, (image_id, file_name) in enumerate(images.items()):
        image = Image.open(f'{image_dir}/{os.path.basename(file_name)}').convert('RGB')
        w, h = image.size
        if i == 0:
            fig.set_size_inches(
                w*col / dpi, h*row / dpi)
        
        ax = fig.add_subplot(int(f'{row}{col}{i+1}'))
        ax.imshow(image)
        ax.set_title(f'{image_id}({os.path.basename(file_name)})', fontsize=int(w*col/dpi))
        ax.axis('off')

        draw_ground_truth(annots, image_id=image_id, ax=ax, annot_type='bbox', classes=classes)
        # axes.flatten()[i].imshow(image)
        # axes.flatten()[i].imshow(image)
        
        # draw_prediction(image_id=image_id, ax=axes.flatten()[i-1], annot_type=annot_type)
        # draw_ground_truth(image_id=image_id, ax=axes.flatten()[i], annot_type='bbox')
        # axes.flatten()[i].axis('off')
        # axes.flatten()[i].axis('off')
    
        if i+1 == num_images:
            break

    
    fig.tight_layout()
    plt.show()
    print('Save coco.png...')
    fig.savefig('coco.png')


# if __name__ == '__main__':
#     visualize_coco(image_dir=None, )





# with open(f'data/{path}/bbox_detections.json', 'r') as json_file:
#     bbox_detections = json.load(json_file)

# with open(f'data/{path}/mask_detections.json', 'r') as json_file:
#     mask_detections = json.load(json_file)

# coco_img_root = '/home/youngwoon/Documents/Tutorial/yolact/data/coco/images/'



# def shuffle():
#     pass


# def generate_center_point(boxes):
#     x1, y1, w, h = boxes[0], boxes[1], boxes[2], boxes[3]
#     cx = x1 + (w/2)
#     cy = y1 + (h/2)
#     return cx, cy

# from typing import Tuple, List, Dict, Any, Optional

# def get_label_color_map(data: Dict) -> Tuple:
#     """ Get label color map

#     argument
#         data : 

#     return
#         lable, color
#     """
#     if path == 'custom':
#         label = CONSTRUCTION_CLASSES[data['category_id']-1]
#         color = CONSTRUCTION_COLORS_MAP.get(label)
#     else:
#         coco_colors_map = {}
#         i = 0
#         for label in COCO_LABEL_MAP.keys():
#             coco_colors_map[label] = rgb2rgba(COLORS[i], 0.2)
#             i += 1
#             if i >= len(COLORS):
#                 i = 0
#         label = COCO_CLASSES[COCO_LABEL_MAP.get(data['category_id'], 0)]
#         color = coco_colors_map.get(COCO_LABEL_MAP.get(data['category_id'], ((0.96, 0.26, 0.21, 0.2), (0.96, 0.26, 0.21, 1.0))))

#     return label, color


# def draw_bbox(ax, data):
#     label, color = get_label_color_map(data)
#     box = data['bbox']
#     if color is None:
#         color = ((0.96, 0.26, 0.21, 0.2), (0.96, 0.26, 0.21, 1.0))
#     ractangle = Rectangle((box[0], box[1]), box[2], box[3], fill=None, ec=color[1])
#     ax.add_patch(ractangle)
#     ax.annotate(
#         label, (box[0], box[1]), color='w', weight='bold', 
#         fontsize=3, ha='left', va='bottom',
#         bbox=dict(facecolor=color[1], edgecolor=color[1], pad=0.0))


# def draw_mask(ax, data, pred: bool = True):
#     label, color = get_label_color_map(data)
#     polygons = data['segmentation']

#     if pred:
#         boxes = mask.toBbox(polygons)
#         cx, cy = generate_center_point(boxes)
#         binary_mask = mask.decode(polygons)
#         contours = measure.find_contours(binary_mask, 0.5)
#         for contour in contours:
#             contour = np.flip(contour, axis=1)
#             polygon = contour.ravel().tolist()
#             polygon = np.array(polygon).reshape(-1, 2)
#             if color is None:
#                 color = ((0.96, 0.26, 0.21, 0.2), (0.96, 0.26, 0.21, 1.0)) 
#             patch = Polygon(polygon, True, fc=color[0], ec=color[1], lw=0.5)
#             ax.add_patch(patch)
        
#         if annot_type != 'both':
#             ax.annotate(
#                 label, xy=(cx,cy), color='w', weight='bold', ha='center', va='center', fontsize=3)

#     else:
#         boxes = data['bbox']
#         cx, cy = generate_center_point(boxes)

#         for polygon in polygons:
#             # print(polygon == 'counts') # 이상한거 하나 껴있음 ㅇㅅㅇ
#             try:
#                 polygon = np.asarray(polygon).reshape(-1, 2)
#                 if polygon.shape[0] == 4:
#                     continue
#                 if color is None:
#                     color = ((0.96, 0.26, 0.21, 0.2), (0.96, 0.26, 0.21, 1.0)) 
#                 patch = Polygon(polygon, True, fc=color[0], ec=color[1], lw=0.5)
#                 ax.add_patch(patch)
#             except:
#                 pass
        
#         if annot_type != 'both':
#             ax.annotate(
#                 label, xy=(cx,cy), color='w', weight='bold', ha='center', va='center', fontsize=3)


# def draw_ground_truth(image_id=None, ax=None, annot_type='bbox'):
#     for data in annotations['annotations']:
#         if data['image_id'] == image_id:
#             if annot_type == 'bbox':
#                 draw_bbox(ax, data)
#             elif annot_type == 'mask':
#                 draw_mask(ax, data, pred=False)
#             else:
#                 draw_bbox(ax, data)
#                 draw_mask(ax, data, pred=False)


# def draw_prediction(image_id=None, ax=None, annot_type='bbox'):
#     for bbox_data, mask_data in zip(bbox_detections, mask_detections):
#         if bbox_data['image_id'] == image_id:
#             if annot_type == 'bbox' and bbox_data['score'] > score_thresh:
#                 draw_bbox(ax, bbox_data)
#             elif annot_type == 'mask' and mask_data['score'] > score_thresh:
#                 draw_mask(ax, mask_data, pred=True)
#             elif annot_type == 'both' and mask_data['score'] > score_thresh:
#                 draw_bbox(ax, bbox_data)
#                 draw_mask(ax, mask_data, pred=True)

# import random

# def main():
#     # Get image ID, and file names from ground truth data
#     images = {annot['id']: annot['file_name'] for annot in annotations['images']}
    
#     shuffle = True
#     if shuffle:
#         shuffled_ids = list(images.keys())
#         random.shuffle(shuffled_ids)
    
#     images = {key: images[key] for key in shuffled_ids}

#     fig, axes = plt.subplots(num_imgs, 2, figsize=(6, 10), dpi=300)
    
#     i = 1
#     for image_id, file_name in images.items():
#         if path == 'custom':
#             image = Image.open(f'./data/{path}/' + file_name)
#         else:
#             image = Image.open(coco_img_root + os.path.basename(file_name))

#         axes.flatten()[i-1].imshow(image)
#         axes.flatten()[i].imshow(image)
        
#         draw_prediction(image_id=image_id, ax=axes.flatten()[i-1], annot_type=annot_type)
#         draw_ground_truth(image_id=image_id, ax=axes.flatten()[i], annot_type=annot_type)
#         axes.flatten()[i-1].axis('off')
#         axes.flatten()[i].axis('off')

#         if i == (num_imgs * 2 - 1): # 39
#             break

#         i += 2

#     fig.tight_layout()
#     fig.savefig('./results/' + annot_type + '_' + path + '_' + str(score_thresh).replace('.','_') + '.png')
#     if args.pop_up_img:
#         plt.show()

# if __name__ == '__main__':
#     main()


