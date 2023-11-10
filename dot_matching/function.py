import pandas as pd
import numpy as np

def csv_to_data(filename):
    df=pd.read_csv(filename)
    x=df['x'].values
    y=df['y'].values
    lum=df['lum'].values
    HIPnum=df['HIPnum'].values
    return x,y,lum,HIPnum


def calc_dist(p1,p2):
    return np.sqrt(sum((p1-p2)**2))


def calc_theta(x,y):
    if x==0:
        if y<0:
            return (-1)*np.pi/2
        else:
            return np.pi/2
    theta=np.argtan(y/x)
    if x<0:
        if y>=0:
            theta+=np.pi
        else:
            theta-=np.pi
    return theta

