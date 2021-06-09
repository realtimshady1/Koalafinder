# Koalafinder

A YOLOv4 based solution for detecting koalas

## Installation

```bash
git clone https://github.com/realtimshady1/Koalafinder.git
cd Koalafinder
pip install -r requirementts.txt

```



## Scripts

`write_bbox_txt.py`: generate bbox text from a csv file

`write_datasets.py`: generate train/validate/text text files for splitting the images

## Configuration

A config file is needed to run the YOLO model and the parameters can be modified to suit each differen application

The following is a recommendation on how best to tune the YOLO model configuration

```python

batch = 64
subdivisions = 16
width = 416 but anything divisible 32 is fine
height = 416 the same as width
max_batches = (# of classes) * 2000 but no less than 6000
steps = (80% of max_batches), (90% of max_batches)
filters = (# of classes + 5) * 3

```

## Usage

```bash
git clone https://github.com/AlexeyAB/darknet
cd darknet
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile

cd darknet/
make

```