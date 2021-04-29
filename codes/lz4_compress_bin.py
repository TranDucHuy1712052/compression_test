import argparse
import numpy
import sys
import math
from pyfastpfor import *
import time
import lz4.frame

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", default=None)
parser.add_argument(
    "-o", default=None)
# mode 0 = encode/compress, 1 = decode/extract
parser.add_argument(
    "-m", "--mode", default=0)

args = parser.parse_args()


def compressToLz4(inpPath, outPath):
    print("Start compressing!")
    read_start_time = time.time()
    f = open(inpPath, "rb")
    buffer  = f.read()
    print("Read time = ", time.time() - read_start_time)

    lz4_comp_time = time.time()
    compBuffer = lz4.frame.compress(buffer)
    print("Compress time = ", time.time()-lz4_comp_time)

    write_start_time = time.time()
    print("Input array length = ", len(compBuffer))
    fw = open(outPath, "wb")
    fw.write(compBuffer)
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)

def decompressFromLz4(inpPath, outPath):
    print("Start decompressing!")
    read_start_time = time.time()
    f = open(inpPath, "rb")
    buffer  = f.read()
    print("Read time = ", time.time() - read_start_time)

    lz4_comp_time = time.time()
    decompBuffer = lz4.frame.decompress(buffer)
    print("Compress time = ", time.time()-lz4_comp_time)

    write_start_time = time.time()
    print("Input array length = ", len(decompBuffer))
    fw = open(outPath, "wb")
    fw.write(decompBuffer)
    write_end_time = time.time()
    print("Write time = ", write_end_time - write_start_time)

mode = int(args.mode)
print("Mode = ", mode)
if (mode == 0):
    compressToLz4(args.i, args.o)
else:
    decompressFromLz4(args.i, args.o)