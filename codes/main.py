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
parser.add_argument(
    "--codec", 
   default="simdfastpfor256"
#    default="simdbinarypacking"
)
parser.add_argument(
    "--cycle", default=1)

args = parser.parse_args()


import gc
import sys

# https://stackoverflow.com/questions/13530762/how-to-know-bytes-size-of-python-object-like-arrays-and-dictionaries-the-simp
def get_obj_size(obj):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz


def readColorFile(filePath):
    f = open(filePath, "r")
    lines = f.readlines()
    arr = []
    for line in lines:
        rgb_str = line.split(' ')
        # r = int(float(rgb_str[0]) * 255.0)
        # g = int(float(rgb_str[1]) * 255.0)
        # b = int(float(rgb_str[2]) * 255.0)
        r = int(rgb_str[0])
        g = int(rgb_str[1])
        b = int(rgb_str[2])
        # arr.append(r)
        # arr.append(g)
        # arr.append(b)
        cint = (r << 16) + (g << 8) + b
        arr.append(cint)
    #print("Array data = ", arr)
    print("Input array length = ", len(arr))
    return arr

def writeColorFile(filepath, colors):
    f = open(filepath, "w")
    for c in colors:
        one8 = (1 << 8) - 1
        one16 = one8 << 8
        one24 = one16 << 8
        r = ((c & one24) >> 16)
        g = ((c & one16) >> 8)
        b = c & one8
        f.write('%d %d %d\n' % (r,g,b))

def compressArray(carr, codec):
    encoder = getCodec(codec)
    notCompSize = carr.shape[0]
    compArr = numpy.zeros(notCompSize + 10, dtype=numpy.uint32, order='C')

    time_start = time.time()
    compSize = encoder.encodeArray(carr, notCompSize, compArr, notCompSize)
    time_end = time.time()

    print("Compress time = ", time_end - time_start, " seconds")
    #print(compArr[compSize-100:compSize+100].tolist())
    print("Compressed file size = ", compSize)
    print("Compress ratio = ", compSize / notCompSize)
    return compArr, compSize

def decompressBuffer(buffer, codec):
    decoder = getCodec(codec)
    decompArr = numpy.zeros(len(buffer) * 10, dtype=numpy.uint32)
    print("Bytes count = ", len(buffer))

    time_start = time.time()
    decompSize = decoder.decodeArray(buffer, len(buffer), decompArr, len(buffer) * 10)
    time_end = time.time()

    print("Decompress time = ", time_end - time_start, " seconds")
   #print(decompArr.tolist())
    print("Decompressed file size = ", decompSize)
    print("Compress ratio = ", len(buffer)/decompSize)

    return decompArr, decompSize
    
def writeBufferOutput(filepath, buffer, size=None):
    f = open(filepath, "wb")
    if (size is not None):
        f.write(buffer[0:size])
    else:
        f.write(buffer)

def EncodeMode(inputPath, outputPath, codec, cycle): 
    read_start_time = time.time()
    carr = readColorFile(inputPath)
    ndcarr = numpy.array(carr, dtype=numpy.uint32, order='C')
    compArr = ndcarr.copy()
    print("Read time = ", time.time() - read_start_time)

    start_time = time.time()
    compArr, compSize = compressArray(compArr, codec)
    print(compArr[compSize])
    compArr2 = compArr[0: compSize + 10]          # resize
    print("Output array bytes size = ", get_obj_size(compArr2))
    print("FastPFor codec encoding time = ", time.time() - start_time)

    lz4_start_time = time.time()
    lz4_compArr = EncodeLZ4(compArr)
    print("Lz4 file size = ", sys.getsizeof(lz4_compArr))
    print("Lz4 compression time = ", time.time() - lz4_start_time)

    write_start_time = time.time()
    #writeBufferOutput(outputPath, compArr2)
    writeBufferOutput(outputPath, lz4_compArr)
    print("Write time = ", time.time() - write_start_time)
    
    print("COMPLETED. Total time = ", time.time() - read_start_time)

def DecodeMode(inputPath, outputPath, codec, cycle):
    f = open(inputPath, "rb")
    buffer = f.read()
    decompBuffer = DecodeLZ4(buffer)            # decompress lz4 to original buffer
    buffer_ndarr = numpy.frombuffer(buffer, dtype=numpy.uint32)
    decompArr, decompSize = decompressBuffer(buffer_ndarr, codec)
    writeColorFile(outputPath, decompArr[0:decompSize])


def EncodeLZ4(buffer):
    compressed = lz4.frame.compress(buffer)
    return compressed

def DecodeLZ4(buffer):
    decompressedBuffer = lz4.frame.decompress(buffer)
    return decompressedBuffer

if __name__ == '__main__':
    if (int(args.mode) == 0):
        EncodeMode(args.i, args.o, args.codec, args.cycle)
    else:
        DecodeMode(args.i, args.o, args.codec, args.cycle)


