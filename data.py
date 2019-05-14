#!/usr/bin/python3.6
import pandas as pd
import os

LIST_FILES = os.listdir()

for item in LIST_FILES:
    global data
    if '.csv' in item:
        data = pd.read_csv(item)
        break


sinhvien_id = list(data['Unnamed: 0'])
class_id = list(data['Unnamed: 1'])
names = list(data['Unnamed: 2'])
birth_days = list(data['Unnamed: 3'])
role = list(data['Unnamed: 4'])
pwd = list(data['Unnamed: 5'])


def getInfo():
    """
        get all info from data
    """
    for id, lop, name, birth, rol, p in zip(sinhvien_id, class_id, names, birth_days, role, pwd):
        yield id, lop, name, birth, rol, p
    pass