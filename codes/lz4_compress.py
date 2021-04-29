import argparse
import numpy
import sys
import math
from pyfastpfor import *
import time
import lz4.frame

parser = argparse.ArgumentParser()
# mode 0 = encode/compress, 1 = decode/extract
parser.add_argument(
    "-m", "--mode", default=0)
parser.add_argument(
    "-i", default=None)
parser.add_argument(
    "-o", default=None)

args = parser.parse_args()


def compressToLz4(inpPath, outPath):
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
    read_end_time = time.time()
    print("Read time = ", read_end_time - read_start_time)

    lz4_comp_time = time.time()
    compArr = lz4.frame.compress(bytes(arr))
    print("Compress time = ", time.time()-lz4_comp_time)

    write_start_time = time.time()
    print("Input array length = ", len(arr))
    fw = open(outPath, "wb")
    fw.write(compArr)
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)

def decompressFromLz4(inpPath, outPath):
    buffer = None
    with open(inpPath, "rb") as fr:
        buffer = fr.read()
    bufferList = list(buffer)
    decompressedBuffer = lz4.frame.decompress(buffer)
    print("Size of decompressed buffer = ", len(decompressedBuffer))
    ints = list(decompressedBuffer)
    rgb16 = [0 for i in range(0, len(ints) // 2)]
    for i in range(0, (len(ints) // 2)):
            #fw.write("%d %d %d\n" % (ints[i*3] ,ints[i*3 + 1], ints[i*3 + 2]))
            b1 = int(ints[i*2])
            b2 = int(ints[i*2 + 1])
            cint = (b2 << 8) + b1
            r = cint >> 10
            g = (cint >> 5) - (r << 5)
            b = cint - (r << 10) - (g << 5)
            rgb16[i] = [r,g,b]

    with open(outPath, "w") as fw:
        for c in rgb16:
            fw.write("%d %d %d\n" % (c[0], c[1], c[2]))
            #fw.write(ints)

time_start = time.time()
mode = int(args.mode)
if (mode == 0):
    compressToLz4(args.i, args.o)
else :
    decompressFromLz4(args.i, args.o)
print("Completed. Time = ", time.time() - time_start)