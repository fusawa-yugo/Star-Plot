import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt



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
def equator_calc_near_dot(reshaped_position,dotsize_x,dotsize_y):
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
def calc_edge_list(x,y,min,max):
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


def plot_stars(directions,point_edge_list):
    if len(directions)==1:
        direction=directions[0]
        if direction.direction=='north' or direction.direction=='south':
            a_points=direction.min_a_points
            a_x=direction.reshaped_position[:,0]
            a_y=direction.reshaped_position[:,1]
            lum=direction.star_data[:,2]
            size=200*np.exp(-1*(lum+2)*np.log(2))
            fig,axes=plt.subplots(nrows=2,ncols=1,figsize=(direction.dotsize_x/10,direction.dotsize_y*2/10))
            for ax in axes:
                ax.set_facecolor('black')
                ax.scatter(a_x,a_y,s=size,color='white')
            axes[0].scatter(direction.min_a_points[:,0],direction.min_a_points[:,1],color='red',s=5)
            for edge in point_edge_list:
                p1=direction.min_a_points[edge[0]]
                p2=direction.min_a_points[edge[1]]
                axes[0].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            for edge in point_edge_list:
                p1=direction.reshaped_position[direction.min_stars[edge[0]]]
                p2=direction.reshaped_position[direction.min_stars[edge[1]]]
                axes[1].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            plt.show()
            return
        else:
            print('error')
            return
    elif len(directions)==2:
        if directions[0].direction!='equator':
            print('error')
            return
        if directions[0].direction=='equator' and directions[1].direction=='ex_equator':
            fig,axes=plt.subplots(nrows=2, ncols=1,figsize=(directions[0].dotsize_x*5/4/10,directions[0].dotsize_y/10*2))
            a_x=directions[0].reshaped_position[:,0]
            a_y=directions[0].reshaped_position[:,1]
            ex_a_x=directions[1].reshaped_position[:,0]+3/4*directions[0].dotsize_x
            ex_a_y=directions[1].reshaped_position[:,1]
            lum=directions[0].star_data[:,2]
            size=200*np.exp(-1*(lum+2)*np.log(2))
            ex_lum=directions[1].star_data[:,2]
            ex_size=200*np.exp(-1*(ex_lum+2)*np.log(2))
            if directions[0].min_dist>directions[1].min_dist:
                less_direction=directions[1]
            else:
                less_direction=directions[0]

            min_a_points=less_direction.min_a_points
            min_stars=less_direction.min_a_points


            for ax in axes:
                ax.set_facecolor('black')
                ax.scatter(ex_a_x,ex_a_y,s=ex_size,color='lightgreen')
                ax.scatter(a_x,a_y,s=size,color='white')

            axes[0].scatter(less_direction.min_a_points[:,0],less_direction.min_a_points[:,1],color='red',s=5)
            for edge in point_edge_list:
                p1=less_direction.min_a_points[edge[0]]
                p2=less_direction.min_a_points[edge[1]]
                axes[0].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            for edge in point_edge_list:
                p1=less_direction.reshaped_position[less_direction.min_stars[edge[0]]]
                p2=less_direction.reshaped_position[less_direction.min_stars[edge[1]]]
                axes[1].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            plt.show()
            return
        else:
            print('error')
            return

