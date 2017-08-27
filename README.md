# SystraceHelper 

## Introduction
`SystraceHelper` is an automatically script, which can get app trace on Android easily based on systrace. `AutoSystrace.sh` start app activity and crawl trace. `ParseSystrace.py` extract each function duration of tracing app from systrace log.

## Usage 
- Set start app activity. `AutoSystrace.sh` contains about 70 popular app start activities, you can choose which you are interested in.
- Elect data from log. Set trace directory, and run `ParseSystrace.py`.

## P.S
Please use `Python 3.x` to run script `ParseSystrace.py`
