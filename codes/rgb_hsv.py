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

    hsvColors = convert_rgb_to_hsv_array(arr)

    write_start_time = time.time()
    print("Output array length = ", len(hsvColors))
    print(hsvColors[0])
    fw = open(outPath, "w")
    for c in hsvColors:
        fw.write("%d %d %d\n" % (c[0], c[1], c[2]))
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)


def convert_rgb_to_hsv_array(rgbArr):
    length = len(rgbArr)
    hsvArr = []

    maxH = -1
    maxS = -1
    maxV = -1
    minH = 361
    minS = 101 
    minV = 101

    for c in rgbArr:
        hsv_c = convert_rgb_to_hsv(c[0], c[1], c[2])
        hsvArr.append(hsv_c)

        maxH = max(maxH, hsv_c[0])
        maxS = max(maxS, hsv_c[1])
        maxV = max(maxV, hsv_c[2])

        minH = min(minH, hsv_c[0])
        minS = min(minS, hsv_c[1])
        minV = min(minV, hsv_c[2])
    
    print(" max = %d %d %d, min = %d %d %d\n" % (maxH, maxS, maxV, minH, minS, minV))
    return hsvArr

def convert_rgb_to_hsv(r, g, b):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    cmax = max(r, max(g,b))
    cmin = min(r, min(g,b))
    d = cmax - cmin

    v = cmax

    s = -1
    if (cmax == 0):
        s = 0
    else:
        s = d * 1.0 / cmax

    h = -1
    if (d == 0):
        h = 0
    elif (cmax == r):
        h = (60 * ((g - b) / d) + 360) % 360
    elif (cmax == g):
        h = (60 * ((b - r) / d) + 120) % 360
    elif (cmax == b):
        h = (60 * ((r - g) / d) + 240) % 360

    h = int(h)
    s = int(s * 100)
    v = int(v * 100)
    return [h,s,v]

time_start = time.time()
do(args.i, args.o)
print("Completed. Time = ", time.time() - time_start)