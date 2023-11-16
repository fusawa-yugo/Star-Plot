import pandas as pd
import numpy as np
import random



def csv_to_stardata(filename):
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

#各座標点から距離が最小の星のHIPnumを返す
def polar_calc_near_dot(reshaped_position,dotsize,HIPnum):
    near_dot=[[-1 for _ in range(dotsize)] for _ in range(dotsize)]
    near_dist=[[float('inf') for _ in range(dotsize)] for _ in range(dotsize)]
    for i in range(dotsize):
        for j in range(dotsize):
            x_dot,y_dot=j,i
            dot=np.array([x_dot,y_dot])
            for k in range(len(reshaped_position)):
                dist=calc_dist(dot,reshaped_position[k])
                if dist<near_dist[i][j]:
                    near_dist[i][j]=dist
                    near_dot[i][j]=k
    return near_dot

#各座標点から距離が最小の星のHIPnumを返す
def equator_calc_near_dot(reshaped_position,dotsize_x,dotsize_y,HIPnum):
    near_dot=[[-1 for _ in range(dotsize_x)] for _ in range(dotsize_y)]
    near_dist=[[float('inf') for _ in range(dotsize_x)] for _ in range(dotsize_y)]
    for i in range(dotsize_y):
        for j in range(dotsize_x):
            x_dot,y_dot=j,i
            dot=np.array([x_dot,y_dot])
            for k in range(len(reshaped_position)):
                dist=calc_dist(dot,reshaped_position[k])
                if dist<near_dist[i][j]:
                    near_dist[i][j]=dist
                    near_dot[i][j]=k
    return near_dot

#min以上max未満の距離の2点(インデックス表示)をタプルのリストで返す
def calc_edge_list(x,y,HIPnum,min,max):
    edge_list=[]
    position=np.column_stack((x,y))
    for i in range(len(x)):
        if i==len(x)-1:
            break
        for j in range(i+1,len(x)):
            dist=calc_dist(position[i],position[j])
            if dist<max and dist>=min:
                edge_list.append((i,j))
    return edge_list

