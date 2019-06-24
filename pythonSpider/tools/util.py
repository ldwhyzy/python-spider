# -*- coding: utf-8 -*-

# Define here the models for yourself tools

import os

def createFolder(path, abpath='d:\\fun\\'):
    folderPath = os.path.join(abpath, path) 
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    return folderPath
        
#if __name__ == '__main__':
#    createFolder('TEST1')        