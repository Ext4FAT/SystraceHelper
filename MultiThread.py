#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Filename:    AutoGetHtrace.sh
# Revision:    1.0
# Date:        2017/08/26
# Author:      _IDLER_
# Email:       exFAT@foxmail.com
# Website:     http://ext4FAT.github.io
# Description: Systrace Helper, elect function data from Systrace's log
# Notes:       
# -------------------------------------------------------------------------------
# Copyright:   2017 (c) _IDLER_
# License:     GPL
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Import 
# -------------------------------------------------------------------------------
import os, re, sys
import ctypes
import math
import codecs
import shutil
import time
import collections
from multiprocessing import cpu_count
from multiprocessing import Process
from multiprocessing import Pool

def myTask(filePath):
    time.sleep(1)
    print(filePath)

def multiProc():
    cpu = getCpuKernelCount()
    memory = getLeftMemory()
    processNum = cpu - 1 
    procPool = Pool(processNum)
    for i in range(100):
        filePath = str(i)
        procPool.apply_async(myTask, (filePath,))
    procPool.close()
    procPool.join()
    
def getCpuKernelCount():
    return cpu_count()

def getLeftMemory():
    '''
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024  
    '''    
    return 0

def main():  
    multiProc()

if __name__ == "__main__":
    main()

