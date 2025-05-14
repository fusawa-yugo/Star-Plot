import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

from plot.detect_points_ver3 import Predict_keypoints_binary
from plot.plot_function import regularize_points,reshape_and_match_image_binary
from plot.plot_function import Local,Search_min

model = './plot/best.pt'

north=Local('north')
south=Local('south')
equator=Local('equator')
ex_equator=Local('ex_equator')
all_locals=Search_min([north,south,equator,ex_equator])

# 画像バイナリから骨格点
def skeletalize_points(img_binary):
    keypoints = Predict_keypoints_binary(model, img_binary)
    return keypoints

# 骨格点を受け取って元々の画像に重ねたものをバイナリで返す
def skeleton_plot(keypoints, img_binary):
    image = Image.open(io.BytesIO(img_binary))  # PILImage を使用
    image = np.array(image)

    name = keypoints['name']
    point_edge_list = keypoints['skelton']
    raw_points = np.array(keypoints['keypoints'])

    plt.imshow(image)
    for edge in point_edge_list:
        start = raw_points[edge[0]]
        end = raw_points[edge[1]]
        plt.plot([start[0], end[0]], [start[1], end[1]], 'y-')
    plt.scatter(raw_points[:, 0], raw_points[:, 1], c='red', label='Key Points')
    plt.axis('off')  # 軸を非表示にする
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='jpg')
    buf.seek(0)
    return buf.getvalue()

#座標点から骨格点を受け取って星にプロットしバイナリで返す
def match_skeleton_from_points(point_edge_list, raw_points, image_binary):
    point_edge_list=np.array(point_edge_list)
    raw_points=np.array(raw_points)
    points, points_norm, points_theta = regularize_points(raw_points)
    all_locals.set_para(len_min=0, len_max=0.2)
    all_locals.explore_local(points)
    direction = all_locals.search_min_local()
    resize_rate = direction.min_norm / points_norm
    rotate_theta = direction.min_theta - points_theta
    reshaped_image_array = reshape_and_match_image_binary(direction, image_binary, resize_rate, rotate_theta, raw_points[0])
    figs = all_locals.show_result(point_edge_list, reshaped_image_array)
    results=[]
    for fig in figs:
        buf = io.BytesIO()
        fig.savefig(buf, format='jpg')
        buf.seek(0)
        results.append(buf.getvalue())
        buf.close()
    return results

def fig_to_plot(img_binary):
    keypoints = skeletalize_points(img_binary)
    results=match_skeleton_from_points(keypoints['skelton'], keypoints['keypoints'], img_binary)
    return results

if __name__ == "__main__":
    with open('./plot/input/images/0.jpg', 'rb') as f:
        img_binary = f.read()
    keypoints = skeletalize_points(img_binary)
    print(keypoints)
    # result = match_skeleton_from_points(keypoints['skelton'], keypoints['keypoints'], img_binary)
    # with open('./static/images/output/0.jpg', 'wb') as f:
    #     f.write(result[0])
    # with open('./static/images/output/1.jpg', 'wb') as f:
    #     f.write(result[1])