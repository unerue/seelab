<p align="center">
  <img height=100em src="img/seelab.png">
</p>
<p align="center">
  <img alt="Kyungsu" src="https://img.shields.io/badge/created%20by-Kyungsu-orange.svg?style=flat&colorA=E1523D&colorB=blue" />
  <img alt="Kyungsu" src="https://img.shields.io/badge/version%20-0.0.1b-orange.svg?style=flat&colorA=E1523D&colorB=blue" />
  <!-- <img alt="SCIE" src="https://img.shields.io/badge/SCIE%20-orange.svg" /> -->
  <!-- <img alt="KCI" src="https://img.shields.io/badge/KCI%20-yellow.svg" /> -->
  <img alt="PythonVersion" src="https://camo.githubusercontent.com/08d69975ce61c30b175f504182ae3a335c6284cbadc26acd9b79e29db442ddea/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e36253230253743253230332e37253230253743253230332e382d626c7565" data-canonical-src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue" style="max-width:100%;" />
  <img src="https://badgen.net/badge/icon/terminal?icon=terminal&label" />
</p>

---

**seelab** is a Python module for extract, visualize, misc for `labelme`, `Pascal VOC` and `MS COCO` annotations built on top of PyTorch and is distributed under the 3-Clause BSD license.

### Contents
* #### [Installation](https://github.com/unerue/seelab#Installation)
* #### [Usage](https://github.com/unerue/seelab#Usage)
* #### [Vision-based construction](https://github.com/unerue/seelab#vision-based-construction)

### Installation

#### Requirements

```bash
git clone https://github.com/unerue/seelab.git
conda env create -f environment.yml
python setup.py install
```

```bash
conda create -n seelab python=3.7
conda activate seelab
pip install -r requirements.txt
pip install git+https://github.com/unerue/seelab.git#egg=seelab
```

### Usage
#### Check labels in dataset

`check` annotations

```bash
$ seelab check --labels
```
```bash
$ seelab check --size
```

`visualize` coco format

```zsh
$ seelab visualize image_dir/ annotations.json --num_images=6
```

### vision-based construction

![](img/fig-0001.png)
