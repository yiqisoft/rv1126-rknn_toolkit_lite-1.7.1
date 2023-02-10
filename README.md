# rv1126-rknn_toolkit_lite-1.8.0
Dockerfiles for RV1126 rknn_toolkit_lite v1.8.0 environment

# Build opencv 3.4.3 docker image base on Debian 10 slim

## Docker Hub repository

https://hub.docker.com/r/jiekechoo/debian10-python3-opencv3.4.3

## Use buildx build cross-platform

```
cd docker-opencv

docker buildx build --platform=linux/arm/v7 --build-arg OPENCV_VERSION=3.4.3 . -t debian10-python3.7-opencv3.4.3
```
## Run docker container in RV1126 EVK
```
docker run -it --rm debian10-python3.7-opencv3.4.3 /bin/bash
```
## Verify opencv installation for python
```
root@5e86b90bc062:/opt/build# python3
Python 3.7.3 (default, Oct 31 2022, 14:04:00) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>>   
```
comfirm no ERRORs

# Build rknn-toolkit-lite v1.8.0 docker image and run exmample python code

## Docker Hub repository

https://hub.docker.com/r/jiekechoo/rv1126-rknn_toolkit_lite

## Use buildx build cross-platform for rknn-tookit-lite
```
cd docker-rknn-toolkit-lite

docker buildx build --platform=linux/arm/v7 . -t rv1126-rknn_toolkit_lite  
```
## Run docker container in RV1126 EVK
```
docker run -it --rm --name rv1126 --privileged -v /dev/dri/card0:/dev/dri/card0 -v /opt/devel/:/opt/devel rv1126-rknn_toolkit_lite /bin/bash
```
## Verify rknn-toolkit-lite installation
```
root@5e86b90bc062:/opt/build# python3
Python 3.7.3 (default, Oct 31 2022, 14:04:00) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from rknnlite.api import RKNNLite
>>> rknn_lite = RKNNLite()
>>> rknn_lite.list_support_target_platform()
**************************************************
All RKNN Toolkit supported target platforms:
chip family 1: RK1806,RK1808,RK3399PRO
chip family 2: RV1109,RK1109,RV1126,RK1126
**************************************************
>>> 
```
rknn-toolkit-lite works ok.

## Run python example code with rknn-toolkit-lite
you should replace `resnet_18.rknn` file in my folder.
```
root@743eeb4de2f7:/opt/devel/rknn-toolkit/rknn-toolkit-lite/examples/inference_with_lite# time python3 test.py 
--> list devices:
*************************
None devices connected.
*************************
done
--> query support target platform
**************************************************
Target platforms filled in RKNN model:         ['RV1109']
Target platforms supported by this RKNN model: ['RV1109', 'RK1109', 'RV1126', 'RK1126']
**************************************************
done
--> Load RKNN model
done
--> Init runtime environment
librknn_runtime version 1.8.0 (97198ce build: 2021-11-24 09:32:17 base: 1131)
done
--> get sdk version:
==============================================
RKNN VERSION:
  API: librknn_runtime version 1.8.0 (97198ce build: 2021-11-24 09:32:17 base: 1131)
  DRV: 6.4.6.5.351518
==============================================

done
--> Running model
resnet18
-----TOP 5-----
[812]: 0.9993900656700134
[404]: 0.0004593880439642817
[657 833]: 2.9284517950145528e-05
[657 833]: 2.9284517950145528e-05
[895]: 1.850890475907363e-05

done

real	0m24.747s
user	0m24.492s
sys	0m0.705s

```
it takes about 25s, too slow...

## Verify C binary program in docker container
```
root@743eeb4de2f7:/opt/devel/yolov5_detect_demo_release# time ./yolov5_detect_demo 
librknn_runtime version 1.8.0 (97198ce build: 2021-11-24 09:32:17 base: 1131)
time_use is 126.657997
car @ (258 909 583 1109) 0.841335
car @ (534 736 739 859) 0.831931
bus  @ (930 413 1206 531) 0.818415
car @ (1766 578 1872 657) 0.810571
car @ (721 760 927 921) 0.792803
car @ (563 950 801 1115) 0.770443
car @ (956 809 1138 968) 0.752421
car @ (801 991 1071 1115) 0.719339
person @ (1431 619 1461 686) 0.699269
car @ (0 495 137 598) 0.674166
person @ (1819 651 1863 739) 0.639357
car @ (1208 431 1261 472) 0.632317
car @ (862 402 936 469) 0.618040
car @ (1781 446 1845 504) 0.575020
person @ (1543 677 1590 771) 0.561444
person @ (375 481 399 528) 0.538842
car @ (1684 431 1737 478) 0.505462
motorbike  @ (1508 748 1564 836) 0.475376
person @ (1200 589 1232 677) 0.471330
car @ (1839 451 1878 501) 0.438286
traffic light @ (1587 548 1608 607) 0.411564
car @ (715 390 777 425) 0.394160
truck  @ (472 451 745 557) 0.392559
car @ (812 416 874 469) 0.387184
car @ (466 425 575 481) 0.358873
car @ (1622 410 1669 454) 0.350634
car @ (1481 331 1578 378) 0.340664
car @ (1191 357 1235 404) 0.321087

real	0m0.690s
user	0m0.454s
sys	0m0.191s
```
wow, 0.69s 

## Run rknn and tflite AI model in RV1126
It looks rknn(based on RV11126 NPU) inference speed more than tflite(based on host CPU) 100 times in python.

There is a screenshot in `images` folder.
```
rknn inference time: 6.874ms
mobilenet_v1
-----TOP 5-----
[ 701 1000]: 0.19482421875
[ 701 1000]: 0.19482421875
[722]: 0.0833740234375
[800]: 0.07501220703125
[887]: 0.0606689453125


0.999801: 89:macaw
0.000175: 91:lorikeet
0.000017: 93:bee eater
0.000003: 90:sulphur-crested cockatoo, Kakatoe galerita, Cacatua galerita
0.000001: 137:European gallinule, Porphyrio porphyrio
tflite inference time: 722.458ms


rknn inference time: 7.054ms
mobilenet_v1
-----TOP 5-----
[89]: 0.88134765625
[91]: 0.055877685546875
[85]: 0.03656005859375
[825]: 0.01407623291015625
[776]: 0.004871368408203125


0.367082: 87:partridge
0.218766: 84:prairie chicken, prairie grouse, prairie fowl
0.200458: 83:ruffed grouse, partridge, Bonasa umbellus
0.097814: 139:bustard
0.026214: 134:bittern
tflite inference time: 727.791ms


rknn inference time: 6.665ms
mobilenet_v1
-----TOP 5-----
[84]: 0.2236328125
[ 9 83]: 0.2010498046875
[ 9 83]: 0.2010498046875
[139]: 0.10638427734375
[87]: 0.0626220703125

0.501498: 875:trolleybus, trolley coach, trackless trolley
0.113881: 655:minibus
0.094743: 830:streetcar, tram, tramcar, trolley, trolley car
0.060285: 800:sliding door
0.030508: 887:vending machine
tflite inference time: 703.747ms

```

# Some tips
## Requirements

- A rv1126 EVK board;
- A high performance PC, Windows based for precompile RKNN models, or macOS based for development;
- Docker develop skills for build docker images and run containers;
- Linux develop skills for build HOST run envrionment;
- Python develop skills for python script debug;
- AI/ML develop skills for deep learning debug;
- GO lang program skills;

... so, you `MUST` be a full-stack programmer :D


## Directory info
 - docker-opencv

Build OPENCV3.4.3 environment, there is an example Dockerfile.

 - docker-rknn-toolkit-lite-ekuiper

 Build rknn-toolkit-lite 1.7.1(`it must be 1.7.1, do not use 1.7.3`) and eKuiper 1.8.0(pre-built eKuiper) base on opencv image.

 - inference_with_lite

An rknn-toolkit-lite python script, run in docker container.

 - yolov5_detect_demo_release

C binary program runs in docker container.

- docker-ekuiper

There is a pyairknn(based on pyai from eKuiper repository) package for eKuiper pipeline testing in RV1126.

