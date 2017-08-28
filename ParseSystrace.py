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
# Version 1.0
# Just catch doFrame and try to determine which is the last frame 
# when app starts, parse one html file within one second
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Import 
# -------------------------------------------------------------------------------
import os, re, sys
import math
import codecs
import shutil
import collections

# -------------------------------------------------------------------------------
# Macro 
# -------------------------------------------------------------------------------
_APP_BEGIN_TAG_ = 'ActivityThreadMain'
#_FUNC_BEGIN_TAG_ = "tracing_mark_write: B"
#_FUNC_END_TAG_ = "tracing_mark_write: E"
_FUNC_BEGIN_TAG_ = ": B"
_FUNC_END_TAG_ = ": E"
_DO_FRAME_TAG_ = '#doFrame'
#_KEYWORDS_ = ['#doFrame']
_KEYWORDS_ = ['bindApplication', 'activityStart', 'updateResourceParamsLocked', 'onSurfaceCreated', 'Choreographer#doFrame'] #'binder transaction' 
_SEGMENT_SIZE_ = 6
_STD_DIFF_THRESHOLD_ = 0.005
_AVG_DIFF_THRESHOLD_ = 0.01
_STD_PERCENT_DIFF_THRESHOLD_ = 0.5
_AVG_PERCENT_DIFF_THRESHOLD_ = 0.5
_TOP_K_ = 300

# -------------------------------------------------------------------------------
# Lambda Function and Regular Expression
# -------------------------------------------------------------------------------
_isHtml_ = lambda f: '.html' in f
_floatPattern_ = re.compile(r'(\d+\.\d*):')
_appTagPattern_ = re.compile(r'.+-\d+\s+\(.+\)')
_hasDoFrame_ = lambda s: _DO_FRAME_TAG_ in s

# -------------------------------------------------------------------------------
# User Defined Class: Record function start and end time in tracing app
# -------------------------------------------------------------------------------
class FuncTag:
    def __init__(self):
        #self.appTag = ''
        self.funcTag = ''    
        self.begin = 0  
        self.end = 0 
        self.duration = 0  

    def __init__(self, f, b, e):
            #self.appTag = ''
        self.funcTag = f    
        self.begin = b  
        self.end = e    
        self.duration = e - b

    def __str__(self):
        #return '[' + self.funcTag + ', ' + str(self.begin) + ', ' + str(self.end) + ']'
        return '[' + self.funcTag + ', ' + str(self.duration) + ']'

# -------------------------------------------------------------------------------
# Helper Function
# ------------------------------------------------------------------------------- 
def getFloat(str):
    return float(_floatPattern_.findall(str)[0])

def getMaxMinAvg(column):
    return max(column), min(column), sum(column)/len(column) 

# Calculate Standard Deviation
def calcSigma(segment):
    avg = sum(segment) / len(segment) 
    avg2 = sum([x*x for x in segment]) / len(segment)
    std = math.sqrt(avg2 - avg*avg)
    return std

# -------------------------------------------------------------------------------
# Statistics: Calulate the whole app start time
# ------------------------------------------------------------------------------- 
def keyFunctionDuration(RESULT):
    funcDuration = collections.OrderedDict()
    for keyword in _KEYWORDS_:
        if (keyword not in RESULT.keys()):
            funcDuration[keyword] = 0.0
            continue    
        funcTagList = RESULT[keyword]
        duration = 0.0
        for funcTag in funcTagList:
            duration += funcTag.duration
        funcDuration[keyword] = duration
    return funcDuration        

# -------------------------------------------------------------------------------
# Statistics: Calulate the whole app start time
# ------------------------------------------------------------------------------- 
def AppStartTime(RESULT):
    bFrame = RESULT[_APP_BEGIN_TAG_][0]
    eFrame = findLastDoFrame(RESULT)
    return eFrame.end - bFrame.begin

def findLastDoFrame(RESULT):
    doFrameTags = [key for key in RESULT.keys() if _DO_FRAME_TAG_ in key]
    if (len(doFrameTags) == 0):
        return FuncTag()
    doFrameTag = doFrameTags[0]
    frameList = RESULT[doFrameTag]
    last, index = slideTest(frameList)
    RESULT[doFrameTag] = trimDoFrame(frameList, index)
    return last

def trimDoFrame(frameList, index):
    return frameList[:index+1]

# 
def slideTest(frameList):
    pre = 0.0
    listLen = len(frameList)
    frameList.reverse()
    for i in range(0, listLen - _SEGMENT_SIZE_):
        segment = [frame.duration for frame in frameList[i:i+_SEGMENT_SIZE_]]
        # TODO: Add new strategy to determine last stamp
        # Rules
        std = calcSigma(segment)
        if ((std - pre) > _STD_DIFF_THRESHOLD_):
            index = i+_SEGMENT_SIZE_-1
            return frameList[i+_SEGMENT_SIZE_-1], index
    return FuncTag(), -1

# -------------------------------------------------------------------------------
# Worker: parse Systrace log 
# ------------------------------------------------------------------------------- 
def parseSystrace(filepath):
    RESULT = collections.OrderedDict()
    curfile = codecs.open(filepath, 'r', 'utf-8')
    # Find app start tag
    app_tag, bstamp= getAppTagAndTimestamp(curfile, _APP_BEGIN_TAG_)
    estamp = findEndTimestamp(curfile, app_tag)
    RESULT[_APP_BEGIN_TAG_]  = [FuncTag(_APP_BEGIN_TAG_, bstamp, estamp)]
    # Find keywords tags
    for i in range(0, _TOP_K_):
        funcTag, bstamp = getFuncTagAndTimestamp(curfile, app_tag)
        estamp = findEndTimestamp(curfile, app_tag)
        if (funcTag not in RESULT.keys()):
             RESULT[funcTag] = []
        RESULT[funcTag].append(FuncTag(funcTag, bstamp, estamp))
    curfile.close()
        '''
        for keyword in _KEYWORDS_:
            if keyword in funcTag:
                if (funcTag not in RESULT.keys()):
                    RESULT[funcTag] = []
                RESULT[funcTag].append(FuncTag(funcTag, bstamp, estamp))
        '''
    return RESULT

def getAppTagAndTimestamp(file, firstTag):
    while (True):
        line = file.readline()
        if firstTag in line:
            break
    try:
        appTag = _appTagPattern_.findall(line)[0]
        timestamp = getFloat(line)
    except Exception as e:
        return None, None
    return appTag, timestamp

def getFuncTagAndTimestamp(curfile, appTag):
    while (True):
        line = curfile.readline()
        if (appTag in line and _FUNC_BEGIN_TAG_ in line):
            break
    funcTag = line.split('|')[-1]
    timestamp = getFloat(line)
    return funcTag.strip(), timestamp

def findEndTimestamp(curfile, appTag):
    paircnt = 1
    while (True):
        line = curfile.readline()
        if (appTag in line):
            if (_FUNC_BEGIN_TAG_ in line):
                paircnt += 1
            elif (_FUNC_END_TAG_ in line):
                paircnt -= 1
        if (paircnt == 0):
            return getFloat(line)
    return -1.0

# -------------------------------------------------------------------------------
# Routine: Looper and Printer
# -------------------------------------------------------------------------------  
def LOOP(DIR):
    fileList = filter(_isHtml_, os.listdir(DIR))
    for index, filename in enumerate(fileList):
        filepath = os.path.join(DIR, filename)
        RESULT = parseSystrace(filepath)
        #PRINT(RESULT)    
        appTime = AppStartTime(RESULT)
        funcDuration = keyFunctionDuration(RESULT)
        HEADER_PRINT()
        APP_PRINT(filename, appTime)
        FUNCTION_PRINT(funcDuration)
    return 0

# TODO: output to file
def HEADER_PRINT():
    print('Filename', 'AppTime', sep=',', end=',')
    for keyword in _KEYWORDS_:
        print(keyword, end=',')
    print('Last-DoFrame-Index')

def APP_PRINT(filename, appTime):
    print('['+filename+']', appTime, sep=',', end=',')

def FUNCTION_PRINT(funcDuration):
    for k, v in funcDuration.items():
        print(v, end=',')
    print()

def PRINT(RESULT):
    for k, vlist in RESULT.items():
        print(k, len(vlist))
        for v in vlist:
            print(v, end=', ')
        print()

# -------------------------------------------------------------------------------
# main
# -------------------------------------------------------------------------------  
def main():  
    DIR = './traces' if len(sys.argv) < 2 else sys.argv[1]
    print('Start parsing ...')
    LOOP(DIR)
    print('End parsing ...')
    return 0

if __name__ == "__main__":
    main()

'''
        values = [getFloat(v) for v in result.values()]
        if len(values) > 0:
            myData.append([filename, values[0], values[1], values[1] - values[0]])    
    myData.sort(key=lambda x:x[3])
    column = [x[3] for x in myData]
    max, min, avg, std = getMaxMinAvg(column)
    myData.append(['max', 'min', 'avg', 'std'])
    myData.append([max, min, avg, std])
'''

