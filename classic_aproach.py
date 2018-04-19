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
    
def turnout(uik_data):
    turnout = (uik_data[invalid] + uik_data[lost]+uik_data[valid])/uik_data[total_voters]
    return turnout

def draw_heatmap(uik_data):
    import matplotlib.pyplot as plt
    import numpy as np
    uik_data['turnout'] = uik_data['turnout']/100
    x = uik_data['z_t'].values
    y = uik_data[putin].values
    plt.hist2d(x, y, bins=60,normed=False,cmap='plasma')
    # Plot heatmap
    plt.title('Pythonspot.com heatmap example')
    plt.hlines(0,-1,2)
    plt.vlines(0,-1,2)
    plt.ylabel('z_vw')
    plt.xlabel('z_t')
    plt.show()    
    

import pandas as pd

uik_data = pd.read_csv("uik_voting_data.csv", encoding='utf8')
