import sys
import numpy as np
import matplotlib.pyplot as plt

from plot.detect_points_ver3 import Predict_keypoints
from plot.plot_function import regularize_points,reshape_and_match_image
from plot.plot_function import Local,Search_min


def star_plot(input='./plot/input/images/0.jpg'):
    model = './plot/best.pt'
    keypoints = Predict_keypoints(model, input)

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

    resize_rate=direction.min_norm/points_norm
    rotate_theta=direction.min_theta-points_theta

    reshaped_image_array=reshape_and_match_image(direction,input,resize_rate,rotate_theta ,raw_points[0])
    figs=all_locals.show_result(point_edge_list,reshaped_image_array)
    return figs

def fig_to_img(figs):
    for fig in figs:
        fig.savefig('star_plot.png', format="png")



if __name__ == "__main__":
    figs=star_plot()
    for fig in figs:
        fig.show()
    plt.show()


