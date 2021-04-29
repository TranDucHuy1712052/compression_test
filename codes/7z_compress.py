import argparse
import numpy
import sys
import math
from pyfastpfor import *
import time
import py7zr

parser = argparse.ArgumentParser()
# mode 0 = encode/compress, 1 = decode/extract
parser.add_argument(
    "-m", "--mode", default=0)
parser.add_argument(
    "-i", default=None)
parser.add_argument(
    "-o", default=None)

args = parser.parse_args()
start_time = time.time()
with py7zr.SevenZipFile(args.o, 'w') as archive:
    archive.writeall(args.i, 'base')
print("7z compression time = ", time.time() - start_time)