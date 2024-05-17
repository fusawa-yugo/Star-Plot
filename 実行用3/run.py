import cv2
import sys
import os
from ultralytics import YOLO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import importlib
from PIL import Image

import plot_function
import detect_points_ver3
importlib.reload(plot_function)
importlib.reload(detect_points_ver3)

from detect_points_ver3 import Predict_keypoints
from plot_function import calc_theta,match_points,calc_edge_list,regularize_points,reshape_and_match_image
from plot_function import Local,Search_min

model = os.getcwd() + '/best.pt'
args = sys.argv
img = os.getcwd() + '/input/images/' + args[1]
keypoints = Predict_keypoints(model, img)
print(keypoints)

name=keypoints['name']
point_edge_list=keypoints['skelton']
raw_points=np.array(keypoints['keypoints'])


north=Local('north')
south=Local('south')
equator=Local('equator')
ex_equator=Local('ex_equator')

all_locals=Search_min([north,south,equator,ex_equator])

points,points_norm,points_theta=regularize_points(raw_points)

all_locals.set_para(len_min=0,len_max=0.2)

all_locals.explore_local(points)

direction=all_locals.search_min_local()

image_path=img

resize_rate=direction.min_norm/points_norm
rotate_theta=direction.min_theta-points_theta

reshaped_image_array=reshape_and_match_image(direction,image_path,resize_rate,rotate_theta ,raw_points[0])
all_locals.show_result(point_edge_list,reshaped_image_array)

