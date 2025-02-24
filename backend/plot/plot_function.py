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
            figs=plot_stars([self.local_list[0]],point_edge_list,reshaped_image_array)
        elif self.min_local.direction=='south':
            figs=plot_stars([self.local_list[1]],point_edge_list,reshaped_image_array)
        elif self.min_local.direction=='equator' or self.min_local.direction=='ex_equator':
            figs=plot_stars([self.local_list[2],self.local_list[3]],point_edge_list,reshaped_image_array)
        else:
            print('error')
            return
        return figs
    
    def set_para(self,len_min=0,len_max=0.2):
        for direction in self.local_list:
            star_data_url=f'./plot/data/{direction.direction}/star_data.npy'
            near_dot_url=f'./plot/data/{direction.direction}/near_dot.npy'
            reshaped_position_url=f'./plot/data/{direction.direction}/reshaped_position.npy'
            direction.star_data=np.load(star_data_url)
            direction.near_dot=np.load(near_dot_url)
            direction.reshaped_position=np.load(reshaped_position_url)
            if direction.direction=='north' or direction.direction=='south':
                direction.dotsize_x=200
                direction.dotsize_y=200
            elif direction.direction=='equator':
                direction.dotsize_x=400
                direction.dotsize_y=100
            else:
                direction.dotsize_x=200
                direction.dotsize_y=100

            x,y=direction.star_data[:,0],direction.star_data[:,1]
            direction.edge_list=calc_edge_list(x,y,len_min,len_max)
        return

    def explore_local(self,points):
        points_size=len(points)
        for direction in self.local_list: 
            print(direction)
            star_data=direction.star_data  
            reshaped_position=direction.reshaped_position
            x,y,lum,HIPnum=star_data[:,0],star_data[:,1],star_data[:,2],star_data[:,3]
            a_x=reshaped_position[:,0]
            a_y=reshaped_position[:,1]
            size=7*np.exp(-1*(lum+2)*np.log(2))
            penalty_of_size=8*np.exp(-5*size*np.log(2)-1)
            direction.min_dist=float('inf')
            for edge in direction.edge_list:
                node1,node2=edge
                star_1=reshaped_position[node1]
                star_2=reshaped_position[node2]
                norm=np.linalg.norm(star_2-star_1)
                theta=calc_theta(star_2-star_1)
                a_points=match_points(points,norm,theta,star_1)
                near_stars=[-1 for _ in range(points_size)]
                dist=0
                for i in range(points_size):
                    a_point=a_points[i]
                    a_point_x=int(round(a_point[0],0))
                    a_point_y=int(round(a_point[1],0))
                    #ここの処理は変えたほうがいいかも
                    if a_point_x<0 or a_point_x>=direction.dotsize_x or a_point_y<0 or a_point_y>=direction.dotsize_y:
                        break
                    indice3=direction.near_dot[a_point_y][a_point_x]
                    nearest_star=np.array([a_x[indice3],a_y[indice3]]).reshape(-1)
                    dist+=np.sum((a_point-nearest_star)**2)/(norm**(2))
                    near_stars[i]=indice3
                    if dist>direction.min_dist:
                        break
                    if i==points_size-1:
                        shape_penalty_rate=0
                        for j in range(points_size):
                            #shape_penalty_rate+=penalty_of_size[near_stars[j]]
                            for k in range(j+1,points_size):
                                if near_stars[j]==near_stars[k]:
                                    if (j,k) in direction.edge_list:
                                        shape_penalty_rate+=0.2
                                    else:
                                        shape_penalty_rate+=0.4
                        dist=dist*(1+shape_penalty_rate)
                        if dist>direction.min_dist:
                            break
                        direction.min_dist=dist 
                        direction.min_stars=near_stars
                        direction.min_a_points=a_points
                        direction.min_theta=theta
                        direction.min_norm=norm
                    if dist>direction.min_dist:
                        break
            print(direction.min_dist)
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
    images = []
    if len(directions)==1:
        direction=directions[0]
        if direction.direction=='north' or direction.direction=='south':
            a_points=direction.min_a_points
            a_x=direction.reshaped_position[:,0]
            a_y=direction.reshaped_position[:,1]
            lum=direction.star_data[:,2]
            size=20*np.exp(-1*(lum+2)*np.log(2))
            fig,ax=plt.subplots(figsize=(direction.dotsize_x/100,direction.dotsize_y/100))
            ax.set_facecolor('black')
            ax.scatter(a_x,a_y,s=size,color='white')
            ax.set_xlim([0,200])
            ax.set_ylim([0,200])
            ax.scatter(direction.min_a_points[:,0],direction.min_a_points[:,1],color='red',s=5)
            for edge in point_edge_list:
                p1=direction.min_a_points[edge[0]]
                p2=direction.min_a_points[edge[1]]
                ax.plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=1)
            images.append(fig)
            fig,ax=plt.subplots(figsize=(direction.dotsize_x/100,direction.dotsize_y/100))
            ax.set_facecolor('black')
            ax.scatter(a_x,a_y,s=size,color='white')
            for edge in point_edge_list:
                p1=direction.reshaped_position[direction.min_stars[edge[0]]]
                p2=direction.reshaped_position[direction.min_stars[edge[1]]]
                ax.plot((p1[0],p2[0]),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=1)
            ax.imshow(reshaped_image_array,alpha=0.7)
            ax.invert_yaxis()
            images.append(fig)
            return images
        else:
            raise ValueError("error")
    elif len(directions)==2:
        if directions[0].direction!='equator':
            raise ValueError("error")
        if directions[0].direction=='equator' and directions[1].direction=='ex_equator':
            fig,ax=plt.subplots(figsize=(directions[0].dotsize_x*5/4/100,directions[0].dotsize_y/100))
            a_x=directions[0].reshaped_position[:,0]
            a_y=directions[0].reshaped_position[:,1]
            ex_a_x=directions[1].reshaped_position[:,0]+3/4*directions[0].dotsize_x
            ex_a_y=directions[1].reshaped_position[:,1]
            lum=directions[0].star_data[:,2]
            size=20*np.exp(-1*(lum+2)*np.log(2))
            ex_lum=directions[1].star_data[:,2]
            ex_size=20*np.exp(-1*(ex_lum+2)*np.log(2))
            if directions[0].min_dist>directions[1].min_dist:
                less_direction=directions[1]
                translation=3/4*directions[0].dotsize_x
            else:
                less_direction=directions[0]
                translation=0
            print(less_direction,translation)
            min_a_points=less_direction.min_a_points
            min_stars=less_direction.min_a_points
            ax.set_facecolor('black')
            ax.scatter(ex_a_x,ex_a_y,s=ex_size,color='lightgreen')
            ax.scatter(a_x,a_y,s=size,color='white')
            ax.set_xlim([0,500])
            ax.set_ylim([0,100])
            ax.scatter(less_direction.min_a_points[:,0]+translation,less_direction.min_a_points[:,1],color='red',s=5)
            for edge in point_edge_list:
                p1=less_direction.min_a_points[edge[0]]
                p2=less_direction.min_a_points[edge[1]]
                ax.plot((p1[0]+translation,p2[0]+translation),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=1)
            images.append(fig)
            fig,ax=plt.subplots(figsize=(directions[0].dotsize_x*5/4/100,directions[0].dotsize_y/100))
            ax.set_facecolor('black')
            ax.scatter(ex_a_x,ex_a_y,s=ex_size,color='lightgreen')
            ax.scatter(a_x,a_y,s=size,color='white')
            for edge in point_edge_list:
                p1=less_direction.reshaped_position[less_direction.min_stars[edge[0]]]
                p2=less_direction.reshaped_position[less_direction.min_stars[edge[1]]]
                ax.plot((p1[0]+translation,p2[0]+translation),(p1[1],p2[1]),color='yellow',alpha=0.5,lw=1)
            ax.imshow(reshaped_image_array,alpha=0.7)
            ax.invert_yaxis()
            images.append(fig)
            return images
        else:
            return images
    return images
        



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
            if ro_j+x_destination+1+x_move>=direction.dotsize_x+x_add_size:
                continue
            try:
                if np.all(reshaped_image_array[ro_i + y_destination][ro_j + x_destination + 1 + x_move] == np.array([0, 0, 0])):
                    reshaped_image_array[ro_i+y_destination][ro_j+x_destination+1+x_move]=reshaped_image_array[ro_i+y_destination][ro_j+x_destination+x_move]
            except IndexError:
                continue

    return reshaped_image_array

