import argparse
import base64
import io
import logging
import time
from typing import List, Any

import numpy as np
import cv2
from PIL import Image
from rknnlite.api import RKNNLite
from ekuiper import Function, Context

cwd = 'plugins/portable/pyairknn/'
RKNN_MODEL = cwd + 'mobilenet_v1.rknn'
LABELS = cwd + 'labels.txt'


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


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

def show_outputs(outputs):
    output = outputs[0][0]
    output_sorted = sorted(output, reverse=True)
    top5_str = 'mobilenet_v1\n-----TOP 5-----\n'
    for i in range(5):
        value = output_sorted[i]
        index = np.where(output == value)
        for j in range(len(index)):
            if (i + j) >= 5:
                break
            if value > 0:
                topi = '{}: {}\n'.format(index[j], value)
            else:
                topi = '-1: 0.0\n'
            top5_str += topi
    print(top5_str)

def label(file_bytes):
    logging.info('image object detecting...')

    encoded = base64.decodebytes(file_bytes.encode("ascii"))
    input_data = np.array(Image.open(io.BytesIO(encoded)))

    image = cv2.cvtColor(input_data, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    t0 = time.time()
    outputs = rknn_lite.inference(inputs=[image])
    print('rknn inference time: {:.3f}ms'.format((time.time() - t0) * 1000))
    show_outputs(outputs)
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
                top5.append({"index": labels[index[j][0]], "value": float(value)})
            else:
                top5.append({"index": "-1", "value": 0.0})
    return top5


class LabelImageFunc(Function):

    def __init__(self):
        load_rknn_model()
        pass

    def validate(self, args: List[Any]):
        if len(args) != 1:
            return "invalid arg length"
        return ""

    def exec(self, args: List[Any], ctx: Context):
        logging.debug("executing label")
        return label(args[0])

    def is_aggregate(self):
        return False


labelIns = LabelImageFunc()
