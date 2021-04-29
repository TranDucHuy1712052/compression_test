import argparse
import numpy
import sys
import math
from pyfastpfor import *
import time
import lz4.frame
import torch

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
        r = int(rgb_str[0]) 
        g = int(rgb_str[1])
        b = int(rgb_str[2])
        cint = (r << 10) + (g << 5) + b
        b1 = cint >> 8
        b2 = cint - (b1 << 8)
        # arr.append(r)
        # arr.append(g)
        # arr.append(b)
        arr.append(b1)
        arr.append(b2)
    read_end_time = time.time()
    print("Read time = ", read_end_time - read_start_time)

    #compArr = lz4.frame.compress(bytes(arr))
    compArr = bytes(arr)

    write_start_time = time.time()
    print("Input array length = ", len(compArr))
    fw = open(outPath, "wb")
    fw.write(bytes(compArr))
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)

def readBytes(inpPath):
    with open(inpPath, "rb") as f:
        return f.read()

def ints_to_rgb16(ints):
    rgb16 = []
    for num in ints:
        r = (num >> 10)
        g = (num >> 5) - (r << 5)
        b = num - (r << 10) - (g << 5)
    

time_start = time.time()


print("Completed. Time = ", time.time() - time_start)