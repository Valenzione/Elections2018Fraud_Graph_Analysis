# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 19:21:38 2018

@author: Bulat
"""

import pandas as pd
import os

fl = os.listdir('tables/')
columns = ['Число избирателей, включенных в список избирателей'
           ,'Число избирательных бюллетеней, полученных участковой избирательной комиссией'
           ,'Число избирательных бюллетеней, выданных избирателям, проголосовавшим досрочно'
           ,'Число избирательных бюллетеней, выданных в помещении для голосования в день голосования'
           ,'Число избирательных бюллетеней, выданных вне помещения для голосования в день голосования'
           ,'Число погашенных избирательных бюллетеней'
           ,'Число избирательных бюллетеней в переносных ящиках для голосования'
           ,'Число бюллетеней в стационарных ящиках для голосования'
           ,'Число недействительных избирательных бюллетеней'
           ,'Число действительных избирательных бюллетеней'
           ,'Число утраченных избирательных бюллетеней'
           ,'Число избирательных бюллетеней, не учтенных при получении '
           ,'Бабурин Сергей Николаевич'
           ,'Грудинин Павел Николаевич'
           ,'Жириновский Владимир Вольфович'
           ,'Путин Владимир Владимирович'
           ,'Собчак Ксения Анатольевна'
           ,'Сурайкин Максим Александрович'
           ,'Титов Борис Юрьевич'
           ,'Явлинский Григорий Алексеевич']




from stat import S_ISREG, ST_CTIME, ST_MODE,ST_MTIME
import os, sys, time

# path to the directory (relative or absolute)
dirpath =  r'tables'

# get all entries in the directory w/ stats
entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_MTIME], path[7:])
           for stat, path in entries if S_ISREG(stat[ST_MODE]))
z = list(entries)
z.sort(key=lambda x:x[0])
z1 = list(map(lambda x: "_".join(x[1].split("_")[:2]),z))

import pandas as pd
z1 = pd.DataFrame(z1).drop_duplicates()


def add_region():
    
    
total = pd.DataFrame(columns=columns)
fl = fl[1:]
for file in fl:
    ff = open('tables/'+file,'rb')
    o = pd.read_csv(ff,encoding='utf8')
    o = o.T
    
    o.columns= columns
    total = pd.concat((total,o))
for file in files:
    