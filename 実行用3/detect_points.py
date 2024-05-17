import cv2
import sys
import os
from ultralytics import YOLO

def calc_joint(n, data, isperson):
    if isperson == 1:
        if n == 0: return (data[5] + data[6]) / 2
        elif n == 1: return (data[11] + data[12]) / 2
        elif n < 5: return data[n - 2]
        elif n < 9: return data[n + 2]
        else: return data[n + 4]
    else: 
        if n < 2: return data[n + 18]
        else: return data[n - 2]

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
    '''
    point_dict = {
        0: 'Nose',
        1: 'L_eye',
        2: 'R_eye',
        3: 'L_ear',
        4: 'R_ear',
        5: 'L_shoulder',
        6: 'R_shoulder',
        7: 'L_elbow',
        8: 'R_elbow',
        9: 'L_wrist',
        10: 'R_wrist',
        11: 'L_waist',
        12: 'R_waist',
        13: 'L_knee',
        14: 'R_knee',
        15: 'L_ankle',
        16: 'R_ankle',
        17: 'Throat',
        18: 'Wither',
        19: 'Tailbase',
        20: 'M_waist',
        21: 'M_shoulder'
    }
    point_human_dict = {
        0: 'M_shoulder'
        1: 'M_waist',
        2: 'Nose',
        3: 'L_eye',
        4: 'R_eye',
        5: 'L_elbow',
        6: 'R_elbow',
        7: 'L_wrist',
        8: 'R_wrist',
        9: 'L_knee',
        10: 'R_knee',
        11: 'L_ankle',
        12: 'R_ankle',
    }
    point_animal_dict = {
        0: 'Wither',
        1: 'Tailbase',
        2: 'Nose',
        3: 'L_eye',
        4: 'R_eye',
        5: 'L_ear',
        6: 'R_ear',
        7: 'L_shoulder',
        8: 'R_shoulder',
        9: 'L_elbow',
        10: 'R_elbow',
        11: 'L_wrist',
        12: 'R_wrist',
        13: 'L_waist',
        14: 'R_waist',
        15: 'L_knee',
        16: 'R_knee',
        17: 'L_ankle',
        18: 'R_ankle',
    }
    '''
    skelton_person = [[0,1],[0,2],[0,5],[0,6],[1,9],[1,10],[2,3],[2,4],[5,7],[6,8],[9,11],[10,12]]
    skelton_animal = [[0,1],[0,2],[0,7],[0,8],[1,13],[1,14],[2,3],[2,4],[3,4],[3,5],[4,6],[7,9],[8,10],[9,11],[10,12],[13,15],[14,16],[15,17],[16,18]]
    skelton = [skelton_animal, skelton_person]
    results = model(cap)
    result_keypoints = []

    imageWidth = results[0].orig_shape[0]
    imageHeight = results[0].orig_shape[1]
    names = results[0].names
    classes = results[0].boxes.cls
    boxes = results[0].boxes
    keypoints = results[0].keypoints
    annotatedFrame = results[0].plot()
    isperson = 0
    p_points = [0,1,2,5,6,7,8,9,10,11,12,13,14,15,16]
    a_points =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19]
    points = [a_points,p_points]

    for i in range(len(classes)):
        cls = int(classes[i])
        if cls == 5: isperson = 1
        else: isperson = 0
        keypoint = {"class": int(classes[i]),"name": names[cls],"skelton": skelton[isperson], "keypoints": calc_point(keypoints[i].data[0], isperson), "valid": valid(keypoints[i].data[0], isperson, points)}
        if keypoint["valid"] == 1: result_keypoints.append(keypoint)

    '''
    # 検出したオブジェクトのバウンディングボックス座標とオブジェクト名を取得し、ターミナルに出力
    for box, cls in zip(boxes, classes):
        name = names[int(cls)]
        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
        print(f"Object: {name} Coordinates: StartX={x1}, StartY={y1}, EndX={x2}, EndY={y2}")
        # バウンディングBOXの座標情報を書き込む
        cv2.putText(annotatedFrame, f"{x1} {y1} {x2} {y2}", (x1, y1 - 40), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0), 2, cv2.LINE_AA)
    #骨格点を出力
    n = 0
    result_keypoint.write('Body_Joint:\n')
    for keypoint in keypoints:
        n += 1
        ok = 1
        result_keypoint.write(f'	Person{n}:\n')
        for i in range(17):
            if (i != 3 and i != 4) and keypoint.data[0][i][2] < 0.5:
                n -= 1
                ok = 0
                break
        if ok == 1:
            body_joint = [17, 18, 0, 1, 2, 7, 8, 9, 10, 13, 14, 15, 16]
            t = 0
            for m in body_joint:
                node = calc_joint(m, keypoint.data[0])
                result_keypoint.write(f'		-{pose_dict[m]}: Index={t}, X={int(node[0])}, Y={int(node[1])}\n')
                t += 1
        else: 
            result_keypoint.write('Not detected properly\n')
    result_keypoint.close()
    '''

    # プレビューウィンドウに画像出力
    #cv2.imshow("YOLOv8 Inference", annotatedFrame)
    #resultimg = cv2.imwrite(os.getcwd() + '/result/images/result_' + args[1],annotatedFrame)
    # 終了処理
    cv2.destroyAllWindows()
    if result_keypoints == []:
        print("Error: Key points were not calculated properly", file=sys.stderr)
        sys.exit(1)
    return result_keypoints