import pandas as pd
import numpy as np
import random



def csv_to_data(filename):
    df=pd.read_csv(filename)
    x=df['x'].values
    y=df['y'].values
    lum=df['lum'].values
    HIPnum=df['HIPnum'].values
    return x,y,lum,HIPnum


def calc_dist(p1,p2):
    return np.sqrt(sum((p1-p2)**2))


def calc_theta(point):
    x,y=point[0],point[1]
    if x==0:
        if y<0:
            return (-1)*np.pi/2
        else:
            return np.pi/2
    theta=np.arctan(y/x)
    if x<0:
        if y>=0:
            theta+=np.pi
        else:
            theta-=np.pi
    return theta


def rotate_point(point, theta):
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])
    rotated_point = np.dot(rotation_matrix, point)
    return rotated_point

def match_points(points,norm,theta,center):
    data_len=len(points)
    a_points=np.zeros((data_len,2))
    for i in range(data_len):
        if i!=0:
            a_points[i]=rotate_point(points[i]*norm,theta)
        a_points[i]=a_points[i]+center
    return a_points

def do_possibility(probability):
    return random.random() < probability