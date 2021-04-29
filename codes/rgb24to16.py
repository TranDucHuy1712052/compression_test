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

    write_start_time = time.time()
    print("Output array length = ", len(arr))
    fw = open(outPath, "w")
    for c in arr:
        fw.write("%d %d %d\n" % (int(c[0]/8), int(c[1]/8), int(c[2]/8)))
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)

time_start = time.time()
do(args.i, args.o)
print("Completed. Time = ", time.time() - time_start)