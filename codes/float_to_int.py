import argparse
import numpy
import sys
import math
from pyfastpfor import *
import time

parser = argparse.ArgumentParser()
# mode 0 = encode/compress, 1 = decode/extract
parser.add_argument(
    "-m", "--mode", default=0)
parser.add_argument(
    "-i", default=None)
parser.add_argument(
    "-o", default=None)

args = parser.parse_args()


def convertFileToBin(inpPath, outPath):
    read_start_time = time.time()
    f = open(inpPath, "r")
    lines = f.readlines()
    arr = []
    for line in lines:
        rgb_str = line.split(' ')
        r = int(float(rgb_str[0]) * 255.0)
        g = int(float(rgb_str[1]) * 255.0)
        b = int(float(rgb_str[2]) * 255.0)
        c = [r,g,b]
        arr.append(c)
        #arr.append(cint)
    read_end_time = time.time()
    print("Read time = ", read_end_time - read_start_time)

    write_start_time = time.time()
    print("Input array length = ", len(arr))
    fw = open(outPath, "w")
    for c in arr:
        fw.write("%d %d %d\n" % (c[0], c[1], c[2]))
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)

time_start = time.time()
convertFileToBin(args.i, args.o)
print("Completed. Time = ", time.time() - time_start)