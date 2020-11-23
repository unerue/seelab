import os
import sys
import argparse
import json
import time
import pprint
from collections import Counter, defaultdict
import glob
import pprint
from PIL import Image
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from numba import jit


folders = [
    '01-Kyungsu', '02-Youngwoon', '03-Validation',
    '06-YouTube', '07-Private', '08-CCTV', '09-License']
# extract_labels = [
#     'person', 'hardhat', 'tower crane', 
#     'support', 'gang form', 'safety vest',
#     'sack', 'excavator', 'conduit pipe',
#     'concrete mixer truck', 'dump truck',
#     'aerial work platform', 'concrete pump truck',
# ]
extract_labels = []
removes = ['lumber', 'aerial work flatform', 'backhoe']


def check_labels():
    if os.path.split(os.getcwd())[-1] != 'Dataset':
        raise FileNotFoundError

    cwd = os.getcwd()
    total_images = 0
    total_jsons = 0
    labels = []
    num_jsons = []
    num_labels = []
    labels_by_image = defaultdict(int)
    error_path_files = []
    error_color_files = []
    error_remove_files = []
    bar_format = '{l_bar}{bar:20}{r_bar}{bar:-20b}'
    print('Checking consistency...')
    for folder in folders:
        images = glob.glob(f'{cwd}/{folder}/*.jpg')
        files = glob.glob(f'{cwd}/{folder}/*.json')

        if len(files) < 2:
            continue

        total_images += len(images)
        total_jsons += len(files)
        num_jsons.append(files)
        cnt = 0

        pbar = tqdm(total=len(files), desc=f'{folder:>17}', ascii=' ->=', bar_format=bar_format)
        for i, file in enumerate(files):
            labels_by_json = defaultdict(int)

            with open(file, 'r') as json_file:
                data = json.load(json_file)
                image_file = os.path.basename(file)[:-5] + '.jpg'
                if data['imagePath'] != os.path.basename(file)[:-5] + '.jpg':
                    error_path_files.append(file)

                image = Image.open(f'{folder}/{image_file}')
                if image.mode != 'RGB':
                    error_color_files.append((image.mode, image_file))

                for line in data['shapes']:
                    if line['label'] not in extract_labels:
                        labels.append(line['label'])
                        labels_by_json[line['label']] += 1
                        cnt += 1

                    if line['label'] in removes:
                        error_color_files.append(file)

            for k, _ in labels_by_json.items():
                labels_by_image[k] += 1

            pbar.update()
        pbar.close()
        num_labels.append(cnt)

    if len(error_path_files) > 0:
        print('Error!!!')
        print(error_path_files)
        print(error_remove_files)
        print(error_color_files)

    print(f'{"Total images":>17}: {total_images:<4} ({total_jsons})')
    print()
    df = pd.DataFrame(Counter(labels).items(), columns=['Label', 'Count'])
    df = df.sort_values(by='Count', ascending=False)
    df = df.reset_index(drop=True)
    df['Ratio'] = round((df['Count'] / df['Count'].sum()) * 100, 2)
    print('Summary of the construction dataset...')
    print(df)
    print()

    print('Number of images by labels...')
    df = pd.DataFrame(labels_by_image.items(), columns=['Label', 'Count'])
    df = df.sort_values(by='Count', ascending=False)
    df = df.reset_index(drop=True)
    df['Ratio'] = round((df['Count'] / df['Count'].sum()) * 100, 2)
    print(df)
    print()
    # print('\nCount by labelers:')
    # print(f'- Kyungsu: {len(num_jsons[0])} ({num_labels[0]})')
    # print(f'- Youngwoon: {len(num_jsons[1])} ({num_labels[1]})')
    # print(f'Total processed {len(num_jsons[0]) + len(num_jsons[1])} images...')

if __name__ == '__main__':
    check_labels()
