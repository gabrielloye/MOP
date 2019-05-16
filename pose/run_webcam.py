import argparse
import logging
import time

import cv2
import os
import numpy as np

import torch
import torch.nn as nn
from torchvision import models

import sys
sys.path.append(os.path.join(os.getcwd(),'pose'))

from estimator import ResEstimator
from networks import *
from network import CoordRegressionNetwork
from dataloader import crop_camera

# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_model(device):
    model_path = os.path.join("./pose/models", 'mobilenetv2'+"_%d_adam_best.t7"%224)
    net = CoordRegressionNetwork(n_locations=16, backbone='mobilenetv2').to(device)
    e = ResEstimator(model_path, net, 224)
    return e


def get_pose(cropped_img, e, device):
    try:
        humans = e.inference(cropped_img, device)
        image = ResEstimator.draw_humans(cropped_img, humans, imgcopy=False)
    except Exception as err:
        print(err)
        image = cropped_img
    return image, humans

