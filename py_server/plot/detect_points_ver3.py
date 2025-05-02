import cv2
import sys
import os
from ultralytics import YOLO
import numpy as np

def calc_joint(n, data, isperson):
    if isperson == 1:
        if n == 0: return (data[5] + data[6]) / 2
        elif n == 1: return (data[11] + data[12]) / 2
        elif n < 5: return data[n - 2]
        elif n < 9: return data[n + 2]
        else: return data[n + 4]
    else: 
        flip_point = [18,19,2,0,1,3,4,5,6,9,10,13,14,7,8,11,12,15,16]
        return data[flip_point[n]]

def calc_point(keypoint, isperson):
    if isperson == 1:
        return [calc_joint(i, keypoint, isperson)[0:2].tolist() for i in range(13)]
    else: 
        return [calc_joint(i, keypoint, isperson)[0:2].tolist() for i in range(19)]

def valid(keypoint, isperson, points):
    for i in points[isperson]:
        if keypoint[i][0] == 0 or keypoint[i][1] == 0: return 0
    return 1

def Predict_keypoints(model_path, img_path):
    model = YOLO(model_path)
    #args = sys.argv
    #cap = cv2.imread(os.getcwd() + '/input/images/' + args[1])
    cap = cv2.imread(img_path)
    skelton_person = [[0,1],[0,2],[0,5],[0,6],[1,9],[1,10],[2,3],[2,4],[5,7],[6,8],[9,11],[10,12]]
    skelton_animal = [[0,1],[0,2],[0,7],[0,8],[1,13],[1,14],[2,3],[2,4],[3,4],[3,5],[4,6],[7,9],[8,10],[9,11],[10,12],[13,15],[14,16],[15,17],[16,18]]
    skelton = [skelton_animal, skelton_person]
    results = model(cap)

    cls = int(results[0].boxes.cls[0])
    isperson = 0
    if cls == 5: 
        isperson = 1
        model = YOLO('yolov8n-pose')
        results = model(cap)
    imageWidth = results[0].orig_shape[0]
    imageHeight = results[0].orig_shape[1]
    name = results[0].names[0]
    box = results[0].boxes[0]
    keypoint = results[0].keypoints[0]
    annotatedFrame = results[0].plot()
    p_points = [0,1,2,5,6,7,8,9,10,11,12,13,14,15,16]
    a_points =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19]
    points = [a_points,p_points]
    data = keypoint[0].data[0]

    result_keypoints = {
        "class": cls,
        "name": name,
        "skelton": skelton[isperson], 
        "keypoints": calc_point(data, isperson), 
        "valid": valid(data, isperson, points)
        }
    cv2.destroyAllWindows()
    if result_keypoints["valid"] == 0:
        print("Error: Key points were not calculated properly", file=sys.stderr)
        sys.exit(1)
    return result_keypoints

def Predict_keypoints_binary(model_path, img_binary):
    # バイナリデータから画像に変換
    model = YOLO(model_path)
    img_array = np.frombuffer(img_binary, np.uint8)
    cap = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    skelton_person = [[0,1],[0,2],[0,5],[0,6],[1,9],[1,10],[2,3],[2,4],[5,7],[6,8],[9,11],[10,12]]
    skelton_animal = [[0,1],[0,2],[0,7],[0,8],[1,13],[1,14],[2,3],[2,4],[3,4],[3,5],[4,6],[7,9],[8,10],[9,11],[10,12],[13,15],[14,16],[15,17],[16,18]]
    skelton = [skelton_animal, skelton_person]
    results = model(cap)

    cls = int(results[0].boxes.cls[0])
    isperson = 0
    if cls == 5: 
        isperson = 1
        model = YOLO('yolov8n-pose')
        results = model(cap)
    imageWidth = results[0].orig_shape[0]
    imageHeight = results[0].orig_shape[1]
    name = results[0].names[0]
    box = results[0].boxes[0]
    keypoint = results[0].keypoints[0]
    annotatedFrame = results[0].plot()
    p_points = [0,1,2,5,6,7,8,9,10,11,12,13,14,15,16]
    a_points =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19]
    points = [a_points,p_points]
    data = keypoint[0].data[0]

    result_keypoints = {
        "class": cls,
        "name": name,
        "skelton": skelton[isperson], 
        "keypoints": calc_point(data, isperson), 
        "valid": valid(data, isperson, points)
        }
    cv2.destroyAllWindows()
    if result_keypoints["valid"] == 0:
        print("Error: Key points were not calculated properly", file=sys.stderr)
        sys.exit(1)
    return result_keypoints