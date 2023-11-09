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