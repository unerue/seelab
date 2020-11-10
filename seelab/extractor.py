import sys
import os
import argparse
import json
import glob
import shutil
import pprint
from collections import Counter, defaultdict


# folders = ['LABEL1', 'LABEL2']
folders = [
    'temporary', '01-Kyungsu', '02-Youngwoon', '03-Validation', '06-YouTube', '07-Private', '08-CCTV', '09-License']
new_dir = 'data'

# extract_labels = ['person', 'hardhat']
# extract_labels = config = [
#     'person', 'hardhat', 'tower crane', 
#     'support', 'gang form', 'safety vest', 'sack', 'excavator', 'conduit pipe',
#     'concrete mixer truck', 'dump truck'
# ]

extract_labels = config = [
    'person', 'hardhat', 'safety vest', 
    'excavator', 'concrete mixer truck', 'dump truck'
]

if not os.path.exists(new_dir):
    os.mkdir(os.path.join(os.getcwd(), new_dir))
    os.mkdir(os.path.join(os.getcwd(), new_dir, 'train'))
    os.mkdir(os.path.join(os.getcwd(), new_dir, 'valid'))

count = 0
objects = 0
for folder in folders:
    files = glob.glob(os.path.join(os.getcwd(), folder, '*.json'))
    for file in files:
        print(f'Processing "{folder}/{os.path.basename(file)}":', end=' ')

        with open(file, 'r') as json_file:
            json_data = json.load(json_file)

        if os.path.basename(file)[:-5] != json_data['imagePath'][:-4]:
            raise ValueError

        data = {
            'version': '4.2.10', 
            'flags': {}, 
            'shapes': [], 
            'imagePath': json_data['imagePath'], 
            'imageData': json_data['imageData'],
            'imageHeight': json_data['imageHeight'], 
            'imageWidth': json_data['imageWidth']}

        # Group ID가 있는 폴리곤 좌표 병합하여 바운딩 박스 그리기
        shapes = []
        group_ids = defaultdict(list)
        labels = defaultdict(list)
        for shape in json_data['shapes']:
            if shape['label'] in extract_labels:
                shapes.append({
                        'label': shape['label'], 
                        'points': shape['points'], 
                        'group_id': shape['group_id'],
                        'shape_type': shape['shape_type'],
                        'flags': {}
                })
            
                if shape['group_id'] is None:
                    xs = []
                    ys = []
                    for p in shape['points']:
                        xs.append(p[0])
                        ys.append(p[1])
                    
                    x_min, y_min = min(xs), min(ys)
                    x_max, y_max = max(xs), max(ys)

                    # shapes.append({
                    #     'label': shape['label'], 
                    #     'points': [[x_min, y_min], [x_max, y_max]], 
                    #     'group_id': None,
                    #     'shape_type': 'rectangle',
                    #     'flags': {}
                    # })
                else:
                    group_ids[shape['group_id']] += shape['points']
                    labels[shape['group_id']] = shape['label']

        if len(group_ids) > 0:
            for k, v in group_ids.items():
                xs = []
                ys = []    
                for p in v:
                    xs.append(p[0])
                    ys.append(p[1])
                
                x_min, y_min = min(xs), min(ys)
                x_max, y_max = max(xs), max(ys)
                # shapes.append({
                #     'label': labels[k], 
                #     'points': [[x_min, y_min], [x_max, y_max]], 
                #     'group_id': None,
                #     'shape_type': 'rectangle',
                #     'flags': {}
                # })
                
        if not len(shapes):
            print(' No objects...')
            continue

        print(f'{len(shapes):>3} objects...')
        data['shapes'] += shapes
        image_id = json_data['imagePath']
        data['imagePath'] = image_id
        
        src = os.path.join(folder, image_id)
        # dst = os.path.join(os.path.join(os.getcwd(), new_dir, 'train'), image_id)
        # print(folder, src, dst)
        # shutil.copy(src, dst)
        
        if folder in ['01-Kyungsu', '02-Youngwoon', '06-YouTube', '07-Private', '08-CCTV', '09-License']:
            dst = os.path.join(os.path.join(os.getcwd(), new_dir, 'train'), image_id)
            shutil.copy(src, dst)
            
            with open(os.path.join(new_dir, 'train', os.path.basename(file)), 'w') as json_file:
                json.dump(data, json_file, indent='\t')

        if folder in ['02-Youngwoon', '03-Validation', 'temporary']:
            dst = os.path.join(os.path.join(os.getcwd(), new_dir, 'valid'), image_id)
            shutil.copy(src, dst)

            with open(os.path.join(new_dir, 'valid', os.path.basename(file)), 'w') as json_file:
                json.dump(data, json_file, indent='\t')
        
        count += 1
        objects += len(shapes)

print(f'Total {count} images, {objects} objects')
