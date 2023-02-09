import argparse
import base64
import io
import logging
import time
from typing import Any, List

import cv2
import numpy as np
from ekuiper import Context, Function
from PIL import Image
from rknnlite.api import RKNNLite

cwd = 'plugins/portable/pyrknn/'
RKNN_MODEL = cwd + 'resnet_18.rknn'
LABELS = cwd + 'labels.txt'

rknn_lite = RKNNLite()

def load_rknn_model():
        
    logging.info('--> query support target platform: %s', RKNN_MODEL)
    rknn_lite.list_support_target_platform(rknn_model=RKNN_MODEL)
    logging.info('done')
    
    # load RKNN model
    logging.info('--> Load RKNN model')
    ret = rknn_lite.load_rknn(RKNN_MODEL)
    if ret != 0:
        logging.info('Load RKNN model failed')
        exit(ret)
    else:
        logging.info('Load RKNN model: success!')
    # Init runtime environment
    logging.info('--> Init runtime environment')
    ret = rknn_lite.init_runtime(target=None)
    if ret != 0:
        logging.info('Init runtime environment failed!')
        exit(ret)
    else:
        logging.info('Init runtime success!')

def init_camera():
    global cap
    cap = cv2.VideoCapture('rtsp://192.168.120.231/ch01_sub.h264')
    if not cap.isOpened():
        raise RuntimeError('Could not open camera.')

def get_frame(self):
    ret, frame = cap.read()
    if ret:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        outputs = rknn_lite.inference(inputs=[image])
        return outputs
    else:
        return None

def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def object_detect(file_bytes):
    logging.info('image object detecting...')
    ret, frame = cap.read()
    if ret:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224,224))
        cv2.imwrite('/tmp/image-{}.jpg'.format(time.time()), image)
        outputs = rknn_lite.inference(inputs=[image])
        output = outputs[0].reshape(-1)
        # softmax
        output = np.exp(output)/sum(np.exp(output))
        output_sorted = sorted(output, reverse=True)
        labels = load_labels(LABELS)
        top5 = []
        for i in range(5):
            value = output_sorted[i]
            index = np.where(output == value)
            for j in range(len(index)):
                if (i + j) >= 5:
                    break
                if value > 0:
                    top5.append({"index": labels[index[j][0]], "value":float(value)})
                else:
                    top5.append({"index": "-1", "value":0.0})
        return top5

class ObjectDetectFunc(Function):

    def __init__(self):
        load_rknn_model()
        init_camera()
        pass

    def validate(self, args: List[Any]):
        if len(args) != 1:
            return "invalid arg length"
        return ""

    def exec(self, args: List[Any], ctx: Context):

        logging.debug("executing object detect")
        return object_detect(args[0])

    def is_aggregate(self):
        return False


detectIns = ObjectDetectFunc()
