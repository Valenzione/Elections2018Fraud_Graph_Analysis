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
    uik_data['z_t'] =  (uik_data[putin] - subregions.transform('mean')[putin])/subregions.transform('std')[putin]
    
def turnout(uik_data):
    turnout = (uik_data[invalid] + uik_data[lost]+uik_data[valid])/uik_data[total_voters]
    return turnout
    
def turnout_subregions(subregions,transform):
    turnout_series = subregions.apply(lambda x: x.assign(turnout = (x[invalid] + x[lost]+x[valid])/x[total_voters])).reset_index('subregion', drop = True)
    return turnout_series

    
    

import pandas as pd

uik_data = pd.read_csv("uik_voting_data.csv", encoding='utf8')
