import json
import shutil
import random
import pandas as pd
from sklearn.model_selection import train_test_split

# def train_test_split():
#     return NotImplementedError


info = {
    'images': [],
    'type': None,
    'annotations': None,
    'categories': None, 
}   



def split_annotations(image_dir, info_path, valid_ratio=0.2):
    with open(info_path, 'r') as json_file:
        annots = json.load(json_file)

    print(annots.keys())
    print(annots['annotations'][0])
    print(annots['categories'])
    info = {
        'images': [], 
        'annotations': [], 
        'categories': annots['categories']}

    df = pd.DataFrame(annots['annotations'])
    print(df.head())
    print(df.tail())
    print(df['category_id'].value_counts())

    X = df.drop(['category_id'], axis=1)
    y = df['category_id']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    print(X_train.head())
    print(y_train.head())
    print(X_test.head())
    print(y_test.head())

    print(X_train.shape, X_test.shape)
    print(y_train.value_counts())
    print(y_test.value_counts())

    print(df.groupby(by='image_id')['category_id'].head())
    pivoted = pd.pivot_table(df, values='iscrowd', index='image_id', columns=['category_id'], aggfunc='count', fill_value=0)
    print(pivoted.head())
    print(pivoted.sum())
    print(pivoted / pivoted.sum())

    image = {
        'file_name': None,
        'height': None,
        'width': None,
        'id':None,
    }

    annotations = {
        'id': None,
        'image_id': None,
        'category_id': None,
        'segmentation': [[]],
        'area': None, 
        'bbox': [],
        'iscrowd': 0,
    }

    image_ids = [annot['id'] for annot in annots['images']]
    random.shuffle(image_ids)

    train_image_ids = image_ids[:int(len(image_ids)*(1-valid_ratio))]
    valid_image_ids = image_ids[int(len(image_ids)*valid_ratio):]

    for image_id in train_image_ids:
        for annot in annots['annotations']:
            if annot['image_id'] == 0:
                print(annot)
                # break
        break
split_annotations('', './cocotrain/annotations.json')

                


    