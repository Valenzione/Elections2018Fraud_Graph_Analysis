# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:30:49 2018

@author: Lua
"""
putin = "Путин Владимир Владимирович"
total_voters = 'Число избирателей, включенных в список избирателей'
valid = "Число действительных избирательных бюллетеней"
invalid = 'Число недействительных избирательных бюллетеней'
lost = 'Число утраченных избирательных бюллетеней'


def z_score(uik_data):
    subregions = uik_data.groupby('subregion')
    uik_data['z_vw'] = (uik_data[putin] - subregions.transform('mean')[putin])/subregions.transform('std')[putin]
    uik_data['turnout'] = turnout(uik_data)
    uik_data['z_t'] =  (turnout(uik_data)-uik_data.groupby('subregion')['turnout'].transform('mean'))/uik_data.groupby('subregion')['turnout'].transform('std')
    uik_data = uik_data.dropna()
    
def turnout(uik_data):
    turnout = (uik_data[invalid] + uik_data[lost]+uik_data[valid])/uik_data[total_voters]
    return turnout

def draw_heatmap(uik_data,x_slice='z_t',y_slice='z_vw'):
    import matplotlib.pyplot as plt
    import numpy as np
    x = uik_data[x_slice].values
    y = uik_data[y_slice].values
    plt.hist2d(x, y, bins=60,normed=False,cmap='plasma')
    # Plot heatmap
    plt.title('Выборы-выборы кандидаты пидоры')
    plt.hlines(0,-1,2)
    plt.vlines(0,-1,2)
    plt.ylabel(y_slice)
    plt.xlabel(x_slice)
    plt.show()    
    

import pandas as pd

uik_data = pd.read_csv("uik_voting_data.csv", encoding='utf8')
uik_data['putin_pc'] = uik_data[putin]/uik_data[valid]

draw_heatmap(uik_data,y_slice='putin_pc',x_slice='turnout')


import benford as bf
from math import log10, floor
count = [0]*10*10

def most_significant_digits(num,n):  
    import math
    if (num == 0):
        return 0
    return int(str(num)[:2])

for i,row in uik_data.iterrows():
    x = abs(row[putin])
    if(x==0):
        continue
    count[ most_significant_digits(x,2) ] += 1
    
    
total = sum(count)
benford = [total*log10(1 + 1./i) for i in range(1, 101)]
plt.bar(range(1,101),count)
plt.bar(range(1,101),benford,alpha = 0.4)
plt.xlabel("Digit")
plt.ylabel("No of uik's")
plt.legend((putin, "Benford's Law"))
tests = []
tests = uik_data.groupby('region').apply(lambda x: bf.first_digits(x[putin].astype('float'), digs=1))


f1d = bf.first_digits(uik_data[valid].astype('float'), digs=1) # digs=1 for the first digit (1-9)
f1d = bf.first_digits(uik_data[putin].astype('float'), digs=2) # digs=1 for the first digit (1-9)
f1d = bf.first_digits(uik_data[total_voters].astype('float'), digs=2) # digs=1 for the first digit (1-9)
f3d = bf.first_digits(uik_data[putin].astype('float'), digs=1)