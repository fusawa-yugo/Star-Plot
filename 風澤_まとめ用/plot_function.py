import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from PIL import Image

class Local:
    def __init__(self,direction=None):
        self.direction=direction
        self.min_dist=None
        self.min_stars=None
        self.min_a_points=None
        self.edge_list=None
        self.near_dot=None
        self.star_data=None
        self.dotsize_x=None
        self.dotsize_y=None
        self.reshaped_position=None
        self.min_norm=None
        self.min_theta=None

    def __str__(self):
        return self.direction


class Search_min:
    def __init__(self,local_list=[]):
        self.local_list=local_list
        self.min_local=None

    def add_local(self,local):
        self.local_list.append(local)
        
    def search_min_local(self):
        min_dist=float('inf')
        min_local=None
        for local in self.local_list:
            if local.min_dist<min_dist:
                min_dist=local.min_dist
                min_local=local
        self.min_local=min_local
        return min_local
    
    def show_result(self,point_edge_list,reshaped_image_array):
        if self.min_local.direction=='north':
            plot_stars([self.local_list[0]],point_edge_list,reshaped_image_array)
        elif self.min_local.direction=='south':
            plot_stars([self.local_list[1]],point_edge_list,reshaped_image_array)
        elif self.min_local.direction=='equator' or self.min_local.direction=='ex_equator':
            plot_stars([self.local_list[2],self.local_list[3]],point_edge_list,reshaped_image_array)
        else:
            print('error')
        return
    
        





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
        for j in range(len(x)):
            if i==j:
                continue
            dist=calc_dist(position[i],position[j])
            if dist<max and dist>=min:
                edge_list.append((i,j))
    return edge_list


def plot_stars(directions,point_edge_list,reshaped_image_array):
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
            axes[0].set_xlim([0,200])
            axes[0].set_ylim([0,200])
            axes[0].scatter(direction.min_a_points[:,0],direction.min_a_points[:,1],color='red',s=5)
            for edge in point_edge_list:
                p1=direction.min_a_points[edge[0]]
                p2=direction.min_a_points[edge[1]]
                axes[0].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            for edge in point_edge_list:
                p1=direction.reshaped_position[direction.min_stars[edge[0]]]
                p2=direction.reshaped_position[direction.min_stars[edge[1]]]
                axes[1].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            axes[1].imshow(reshaped_image_array,alpha=0.5)
            axes[1].invert_yaxis()
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
            axes[0].set_xlim([0,500])
            axes[0].set_ylim([0,100])
            axes[0].scatter(less_direction.min_a_points[:,0],less_direction.min_a_points[:,1],color='red',s=5)
            for edge in point_edge_list:
                p1=less_direction.min_a_points[edge[0]]
                p2=less_direction.min_a_points[edge[1]]
                axes[0].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            for edge in point_edge_list:
                p1=less_direction.reshaped_position[less_direction.min_stars[edge[0]]]
                p2=less_direction.reshaped_position[less_direction.min_stars[edge[1]]]
                axes[1].plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=5)
            axes[1].imshow(reshaped_image_array,alpha=0.5)
            axes[1].invert_yaxis()
            plt.show()
            return
        else:
            print('error')
            return

def regularize_points(raw_points):
    points_size=len(raw_points)
    points=np.zeros((points_size,2))
    for i in range(1,points_size):
        points[i]=raw_points[i]-raw_points[0]
    points[0]=np.array([0,0])
    points_norm=np.linalg.norm(points[1])
    points_theta=calc_theta(points[1])
    for i  in range(1,points_size):
        points[i]=rotate_point(points[i]/points_norm,(-1)*points_theta)
    return points,points_norm,points_theta


def reshape_and_match_image(direction,image_path,resize_rate,rotate_theta,point):
    image = Image.open(image_path)
    width, height = image.size
    center_x=point[0]
    center_y=point[1]
    resized_image = image.resize((int(width*resize_rate), int(height*resize_rate)))
    image_array = np.array(resized_image)
    reshaped_image_array=np.zeros((direction.dotsize_y,direction.dotsize_x,3),dtype=int)
    y_size=image_array.shape[0]
    x_size=image_array.shape[1]

    if direction.direction=='ex_equator':
        x_move=300
    else:
        x_move=0
    if direction.direction=='ex_equator':
        x_add_size=300
    elif direction.direction=='equator':
        x_add_size=100
    else:
        x_add_size=0


    reshaped_image_array=np.zeros((direction.dotsize_y,direction.dotsize_x+x_add_size,3),dtype=int)
    y_size=image_array.shape[0]
    x_size=image_array.shape[1]

    x_center=int(round(point[0]*resize_rate,0))
    y_center=int(round(point[1]*resize_rate,0))
    x_destination=int(round(direction.min_a_points[0][0],0))
    y_destination=int(round(direction.min_a_points[0][1],0))
    x_diff=int(x_destination-x_center)
    y_diff=int(y_destination-y_center)



    for i in range(y_size):
        for j in range(x_size):
            re_i=i-y_center
            re_j=j-x_center
            p=np.array([re_j,re_i])
            rotated_p=rotate_point(p,rotate_theta)
            ro_i=int(round(rotated_p[1],0))
            ro_j=int(round(rotated_p[0],0))
            if ro_i+y_destination<0 or ro_j+x_destination<0:
                continue
            try:
                reshaped_image_array[ro_i+y_destination][ro_j+x_destination+x_move]=image_array[i][j]
            except IndexError:
                pass

    '''
    for i in range(y_size):
        for j in range(x_size):
            re_i=i-y_center
            re_j=j-x_center
            try:
                reshaped_image_array[i+y_diff][j+x_diff]=image_array[i][j]
            except IndexError:
                pass


    reshaped_image_array = reshaped_image_array.astype(np.uint8)

    fig, ax = plt.subplots()
    ax.imshow(reshaped_image_array)
    ax.invert_yaxis()
    plt.show()



    reshaped_image = Image.fromarray(reshaped_image_array)

    reshaped_image=reshaped_image.rotate(-rotate_theta*180/np.pi,center=(x_destination,y_destination))

    reshaped_image_array=np.array(reshaped_image) 
    '''

    return reshaped_image_array