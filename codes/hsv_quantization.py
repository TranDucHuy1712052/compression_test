import argparse
import numpy
import sys
import math
from pyfastpfor import *
import time
import statistics

parser = argparse.ArgumentParser()
# mode 0 = encode/compress, 1 = decode/extract
parser.add_argument(
    "-m", "--mode", default=0)
parser.add_argument(
    "-i", default=None)
parser.add_argument(
    "-o", default=None)

args = parser.parse_args()



def do(inpPath, outPath):
    read_start_time = time.time()
    f = open(inpPath, "r")
    lines = f.readlines()
    arr = []
    for line in lines:
        rgb_str = line.split(' ')
        r = int(rgb_str[0])
        g = int(rgb_str[1])
        b = int(rgb_str[2])
        c = [r,g,b]
        arr.append(c)
        #arr.append(cint)
    print(arr[0])
    read_end_time = time.time()
    print("Read time = ", read_end_time - read_start_time)

    quanArr = quantization(arr)

    write_start_time = time.time()
    print("Output array length = ", len(quanArr))
    print(quanArr[0])
    fw = open(outPath, "w")
    for c in quanArr:
        fw.write("%d %d %d\n" % (c[0], c[1], c[2]))
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)


def quantization(arr):
    #maxH, maxS, maxV, minH, minS, minV = find_min_and_max(arr)
    arr2 = []
    for c in arr:
        arr2.append([ (c[0] // 8), (c[1] * (16/100)), (c[2] * (16/100)) ])
    return arr2


def find_min_and_max(arr):
    
    maxH = -1
    maxS = -1
    maxV = -1
    minH = 361
    minS = 101 
    minV = 101

    for hsv in arr:
        maxH = max(maxH, hsv[0])
        maxS = max(maxS, hsv[1])
        maxV = max(maxV, hsv[2])

        minH = min(minH, hsv[0])
        minS = min(minS, hsv[1])
        minV = min(minV, hsv[2])

    return maxH, maxS, maxV, minH, minS, minV
    

time_start = time.time()
do(args.i, args.o)
print("Completed. Time = ", time.time() - time_start)