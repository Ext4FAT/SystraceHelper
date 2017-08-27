# SystraceHelper 

## Introduction

`SystraceHelper` is an automatically script, which can get app trace on Android easily based on systrace. `AutoSystrace.sh` start app activity and crawl trace. `ParseSystrace.py` extract each function duration of tracing app from systrace log.


## Usage 

- Set start app activity. `AutoSystrace.sh` contains about 70 popular app start activities, you can choose which you are interested in.
- Elect data from log. Set trace directory, and run `ParseSystrace.py`.


## P.S

Please use `Python 3.x` to run script `ParseSystrace.py`. If you have python2.x and python3.x simultaneously, you can run `ParseSystrace.py` with 
``` sh
py -3 ParseSystrace.py
```


## Welcome to contact me

If you have any problem, you can contact me with the e-mail exFAT@foxmail.com.
