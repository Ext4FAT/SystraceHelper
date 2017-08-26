#!/usr/bin/env python
# encoding: utf-8

import shutil
import codecs
import math
import os, re, sys
import collections

### 
_isHtml_ = lambda f: '.html' in f
_floatPattern_ = re.compile(r'(\d+\.\d*):')
_appTagPattern_ = re.compile(r'.+-\d+\s+\(.+\)')

_APP_BEGIN_TAG_ = 'ActivityThreadMain'
_FUNC_BEGIN_TAG_ = "tracing_mark_write: B"
_FUNC_END_TAG_ = "tracing_mark_write: E"
_KEYWORDS_ = ['bindApplication', 'activityStart', '#doFrame'] 

### 
class FuncTag:
    def __init__(self):
        #self.appTag = ''
        self.funcTag = ''    
        self.begin = 0  
        self.end = 0    

    def __init__(self, f, b, e):
            #self.appTag = ''
        self.funcTag = f    
        self.begin = b  
        self.end = e    

    def __str__(self):
        #return '[' + self.funcTag + ', ' + str(self.begin) + ', ' + str(self.end) + ']'
        return '[' + self.funcTag + ', ' + str(self.duration()) + ']'

    def duration(self):
        return self.end - self.begin

### Helper Function
def getFloat(str):
    return float(_floatPattern_.findall(str)[0])

def getMaxMinAvg(column):
    avg = sum(column) / len(column) 
    avg2 = sum([x*x for x in column]) / len(column)
    std = math.sqrt(avg2 - avg*avg)
    return max(column), min(column), avg, std 

### Worker
def parseSystrace(filepath):
    RESULT = collections.OrderedDict()
    # Construct filepath and open
    print('[', filepath, ']')
    curfile = codecs.open(filepath, 'r', 'utf-8')
    # Find app start tag
    app_tag, bstamp= getAppTagAndTimestamp(curfile, _APP_BEGIN_TAG_)
    estamp = findEndTimestamp(curfile, app_tag)
    RESULT[_APP_BEGIN_TAG_]  = [FuncTag(app_tag, bstamp, estamp)]
    # Find keywords tags
    for i in range(0, 100):
        funcTag, bstamp = getFuncTagAndTimestamp(curfile, app_tag)
        estamp = findEndTimestamp(curfile, app_tag)
        for keyword in _KEYWORDS_:
            if keyword in funcTag:
                if (funcTag not in RESULT.keys()):
                    RESULT[funcTag] = []
                RESULT[funcTag].append(FuncTag(funcTag, bstamp, estamp))
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

### Routine
def LOOP(DIR):
    fileList = filter(_isHtml_, os.listdir(DIR))
    for filename in fileList:
        filepath = os.path.join(DIR, filename)
        RESULT = parseSystrace(filepath)
        outResult(RESULT)        
    return 0

def outResult(RESULT):
    for k, vlist in RESULT.items():
        print(k)
        for v in vlist:
            print(v, end=', ')
        print()
    return 0

### Main
def main():
    DIR = './traces' if len(sys.argv) < 2 else sys.argv[1]
    LOOP(DIR)
    return 0

if __name__ == "__main__":
    main()
