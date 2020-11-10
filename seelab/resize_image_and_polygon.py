import sys
import json
from PIL import Image
import glob

from collections import defaultdict
from typing import Tuple, List, Dict
import os
import numpy as np


folders = [
    '01-Kyungsu', '02-Youngwoon', '03-Validation', '06-YouTube', '07-Private', '08-CCTV', '09-License']
save_json = False

def resize_polygon(path: str, size: Tuple, resize: Tuple):
    global save_json
    image_path = os.path.basename(path)
    path = path[:-4] + '.json'
    
    try:
        with open(path) as json_file:
            shapes = json.load(json_file)

        for shape in shapes['shapes']:
            polygon = np.array(shape['points'])
            polygon[:, 0] *= resize[0] / size[0]
            polygon[:, 1] *= resize[1] / size[1]
            
            shape['points'] = polygon.tolist()
        
        shapes['imagePath'] = image_path
        shapes['imageData'] = None
        shapes['imageWidth'] = resize[0]
        shapes['imageHeight'] = resize[1]

        filename = os.path.basename(path)
        path = os.path.join(os.path.dirname(path), filename)
    
        with open(path, 'w') as json_file:
            json.dump(shapes, json_file)

        save_json = True

    except FileNotFoundError:
        save_json = False
        pass
    

def save_jpg(path, image):
    filename = os.path.basename(path)
    path = os.path.join(os.path.dirname(path), filename)        
    image.save(path, quality=80, optimize=True)


# def resize_shapes(folders: List[str]):
def check_size(base_height=720):
    for folder in folders:
        for path in glob.glob(f'{folder}/*.jpg'):
            image = Image.open(path)
            w, h = image.size
            
            if h > base_height and w > h:
                print(f'{path} size: {(w, h)}', end=' ')

                percent = base_height / h
                resized_width = int(w * percent)
                
                image = image.resize((resized_width, base_height))
                
                resize_polygon(path, (w, h), (resized_width, base_height))    
                save_jpg(path, image)
                
                if save_json:
                    print(f'-> resize: ({image.size}) and save json...')
                else:
                    print(f'-> resize: ({image.size})...')

            elif w > base_height and w < h:
                print(f'{path} size: {(w, h)}', end=' ')
                percent = base_height / w
                resized_height = int(h * percent)
                
                image = image.resize((base_height, resized_height))
                
                resize_polygon(path, (w, h), (base_height, resized_height))

                save_jpg(path, image)
    
                if save_json:
                    print(f'-> resize: ({image.size}) and save json...')
                else:
                    print(f'-> resize: ({image.size})...')
            
            elif w > base_height and h > base_height and w == h:
                print(f'{path} size: {(w, h)}', end=' ')
                
                image = image.resize((base_height, base_height))
                
                resize_polygon(path, (w, h), (base_height, base_height))

                save_jpg(path, image)
    
                if save_json:
                    print(f'-> resize: ({image.size}) and save json...')
                else:
                    print(f'-> resize: ({image.size})...')


if __name__ == '__main__':      
    check_size()