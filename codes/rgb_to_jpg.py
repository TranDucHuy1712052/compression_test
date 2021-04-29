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
        arr.append(r)
        arr.append(g)
        arr.append(b)
        #arr.append(cint)
    print(arr[0])
    read_end_time = time.time()
    print("Read time = ", read_end_time - read_start_time)

    img = write_rgb_to_png(arr)

    write_start_time = time.time()
    img.save(outPath, "JPEG")
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)


def write_rgb_to_png(rgbArr):
    from PIL import Image
    ndarr = numpy.array(rgbArr, dtype=numpy.uint8)
    print(ndarr.shape)
    img = Image.fromarray(ndarr)
    return img

time_start = time.time()
do(args.i, args.o)
print("Completed. Time = ", time.time() - time_start)