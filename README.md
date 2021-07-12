# Koalafinder

A YOLOv4 based solution for detecting koalas in thermal imaging

## Installation

### Ubuntu 18.04

```bash
sudo apt update
sudo apt install python3 python3-pip
git clone https://github.com/realtimshady1/Koalafinder.git
cd Koalafinder
pip3 install --upgrade -r requirements.txt

```

## Scripts

`write_bbox_txt.py`: generate bbox text from a csv file using [UltimateLabeling](https://github.com/alexandre01/UltimateLabeling/tree/master/ultimatelabeling)

`write_datasets.py`: generate train/validate/text text files for splitting the images



## Setup

### Dataset

The koala data needs to be downloaded from the [Google Drive](https://drive.google.com/drive/folders/1v_w4-pkDTD1CF5tU2WWyccbrTg-8ra98?usp=sharing) into a new `obj` folder the `data/` folder along with the annotations in the following structure

```bash

└───data
    └───obj
        ├───00001.jpg
        ├───00001.txt
        ├───00002.jpg
        ├───00002.txt
        └───...

```
The training data split files `[test.txt train.txt valid.txt]` are generated using the `write_dataset.py` script
```bash
python3 write_datasets.py 60 20 data/obj
```

### YOLOv4

#### GPU

Ideally there is a GPU provided for YOLO to run on but it doesn't necessarily need one. The following sections continue with the assumption that there is a GPU to train with. In the future, a section will be made for how to build without the use of a GPU.

Make sure that the correct GPU toolkit are installed. Run the following commands to verify that the versions are correct.

```bash
nvidia-smi
/usr/local/cuda/bin/nvcc --version

```

#### Build

A good tutorial for going through building darknet is by [DepthAI Tutorial: Training a Tiny YOLOv4 Object Detector with Your Own Data](https://colab.research.google.com/github/ibaiGorordo/Social-Distance-Feedback/blob/master/Part%202%20-%20Mask%20Detection/Face%20Mask%20Detection%20Inference%20Comparison/YOLOv4_tiny_Darknet_Mask_Detection.ipynb)

Otherwise, the outlined build method used the following component version setup

Component | Version
--- | --- 
GPU | Tesla T4 
CUDA | 11.0
NVCC | 11.0.221  
cuDNN | 8.0.5  
OpenCV | 3.2.0
 

```bash
git clone https://github.com/AlexeyAB/darknet
cd darknet
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
sed -i 's/LIBSO=0/LIBSO=1/' Makefile

sudo make
cp darknet ../Koalafinder/
cp libdarknet.so ../Koalafinder/
```

> Build errors attributed to `/bin/sh: 1: nvcc: not found` can be fixed by directing `NVCC=nvcc` to the location of CUDA's NVCC location

### Config

A config file is needed to run the YOLO model and the parameters can be modified to suit each differen application

The following is a recommendation on how best to tune the YOLO model configuration

```python

batch = 64
subdivisions = 1
width = 416 but anything divisible 32 is fine
height = 416 the same as width
max_batches = (# of classes) * 2000 but no less than 4000
steps = (80% of max_batches), (90% of max_batches)
filters = (# of classes + 5) * 3

```

## Usage

### Training

Training the neural network can be completed using 

```bash
./darknet detector train obj.data yolov4-tiny.cfg yolov4-tiny.conv.29 -dont_show -ext_output -map

```

### Evaluate

Evaluate the neural network on the test dataset

```bash
./darknet detector map obj.data yolov4-tiny.cfg backup/yolov4-tiny_best.weights -points 0

```

### Test

Test the neural network on one image. This should be one from the test.txt dataset

```bash
./darknet detector test obj.data yolov4-tiny.cfg backup/yolov4-tiny_best.weights data/obj/00001.jpg -ext_output

```

The neural network will generate a `predictions.jpg` file as the output

### Inference

To perform inference on a test image
```bash
python3 yolov4_inference.py yolov4-tiny.cfg obj.data yolov4-tiny.weights data/obj/00001.jpg
```

## Progress

The most recent run example is shown here

![chart.png](chart.png)



