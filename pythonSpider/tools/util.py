# -*- coding: utf-8 -*-

# Define here the models for yourself tools

import os
import re

def pathValidate(path):
    pattern = re.compile(r'[<>/\|:"*?]')
    return re.sub(pattern, r'-', path)

def createFolder(path, abpath='d:\\fun\\'):
    folderPath = os.path.join(abpath, path) 
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    return folderPath
        
if __name__ == '__main__':
    #createFolder('TEST1')
    print(pathValidate('(C72) [サークルOUTERWORLD (千葉秀作)] Midgard <ラグ> (ああっ女神さまっ)'))    