import argparse
import numpy
import sys
import math
# from pyfastpfor import *
import time
import lz4.frame
import io
import lzma
import json
import os


parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", default="../input")
parser.add_argument(
    "-o", default="../output")
parser.add_argument(
    "-l",  type=int, default=10)


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


def readBuffer(filePath):
    f = open(filePath, "rb")
    buffer = f.read()
    return buffer

def writeBuffer(buffer, filepath):
    f = open(filepath, "wb")
    f.write(buffer)


# === COLOR FILE

def convert_color_buffer_to_array(decompressed_buffer: bytes, colorbit: int = 16):
    print("Size of decompressed buffer = ", len(decompressed_buffer))
    ints = list(decompressed_buffer)
    
    colorbyte = (colorbit // 8) + (1 if (colorbit % 2 > 0) else 0)        
    rgb = [0 for i in range(0, len(ints) // colorbyte)]

    for i in range(0, (len(ints) // colorbyte)):
        cint = 0
        for j in range(colorbyte):
            cint += int(ints[i*colorbyte + j] << (8 * j))
        r,g,b = 0,0,0
        if (colorbyte == 1):
            raise NotImplementedError()
        elif (colorbyte == 2):
            if (colorbit == 15):            # r,g,b bits = 5,5,5
                r = cint >> 10
                g = (cint >> 5) - (r << 5)
                b = cint - (g << 5) - (r << 10)
            elif (colorbit == 16):          # 5,6,5
                r = cint >> 11
                g = (cint >> 5) - (r << 6)
                #b = cint % (1 << 5)
                b = cint - (g << 6) - (r << 11)
        elif (colorbyte == 3):          # 24-bit, (8,8,8) 
            r = cint >> 16
            g = (cint >> 8) - (r << 8)
            b = cint % (1 << 8)
        rgb[i] = [r,g,b] 
    return rgb

def convert_16bit_to_24bit(rgb:numpy.ndarray):
    return numpy.round( (rgb / 32) * 255).astype("uint8")



# === ALGOs

# FastPFOR

# default_fastpfor_codec = "simdfastpfor256"

# def fastpfor_encode(arr: numpy.ndarray, codec: str):
#     encoder = getCodec(codec)
#     notCompSize = arr.shape[0]
#     compArr = numpy.zeros(notCompSize + 10, dtype=numpy.uint32, order='C')

#     time_start = time.time()
#     compSize = encoder.encodeArray(carr, notCompSize, compArr, notCompSize)
#     encode_time = (time.time() - time_start)*1000           # in ms
#     return compArr, compSize, encode_time

# def fastpfor_decode(buffer, codec):
#     decoder = getCodec(codec)
#     decompArr = numpy.zeros(len(buffer) * 10, dtype=numpy.uint32)

#     time_start = time.time()
#     decompSize = decoder.decodeArray(buffer, len(buffer), decompArr, len(buffer) * 10)
#     decode_time = (time.time() - time_start)*1000
#     return decompArr, decompSize, decode_time

# def fastpfor_benchmark(buffer):
#     ori_size = len(buffer)
#     color_arr = convert_16bit_to_24bit( numpy.array(convert_color_buffer_to_array(buffer)) )
#     comp_arr, comp_size, encode_time = fastpfor_encode(color_arr, default_fastpfor_codec)
#     decomp_arr, decomp_size, decode_time = fastpfor_decode(comp_arr, default_fastpfor_codec)
#     keep_content = (color_arr == decomp_arr).all()            # two array must be equivalent
#     ratio = (comp_size / ori_size)
#     return encode_time, decode_time, ratio, keep_content

# Lz4

def lz4_encode(buffer):
    time_start = time.time()
    compressed = lz4.frame.compress(buffer)
    return compressed, len(compressed), (time.time() - time_start)*1000

def lz4_decode(buffer):
    time_start = time.time()
    decompressedBuffer = lz4.frame.decompress(buffer)
    return decompressedBuffer, len(decompressedBuffer), (time.time() - time_start)*1000
    
def lz4_benchmark(buffer):
    ori_size = len(buffer)
    #color_arr = convert_16bit_to_24bit( numpy.array(convert_color_buffer_to_array(buffer)) )
    comp_buffer, comp_size, encode_time = lz4_encode(buffer)
    decomp_buffer, decomp_size, decode_time = lz4_decode(comp_buffer)
    keep_content = (buffer == decomp_buffer)           # two array must be equivalent
    #ratio = (comp_size / ori_size)
    ratio = (comp_size / decomp_size)
    return encode_time, decode_time, ratio, keep_content, comp_buffer, decomp_buffer


# lzma (main algo for 7z)

def lzma_encode(buffer):
    start_time = time.time()
    comp_buffer = lzma.compress(buffer)
    return comp_buffer, len(comp_buffer), (time.time() - start_time)*1000

def lzma_decode(buffer):
    start_time = time.time()
    decomp_buffer = lzma.decompress(buffer)
    return decomp_buffer, len(decomp_buffer), (time.time() - start_time)*1000

def lzma_benchmark(buffer):
    ori_size = len(buffer)
    comp_buffer, comp_size, encode_time = lzma_encode(buffer)
    decomp_buffer, decomp_size, decode_time = lzma_decode(comp_buffer)
    keep_content = (buffer == decomp_buffer)           # two array must be equivalent
    #ratio = (comp_size / ori_size)
    ratio = (comp_size / decomp_size)
    return encode_time, decode_time, ratio, keep_content, comp_buffer, decomp_buffer


benchmark_algorithms = [lz4_benchmark, lzma_benchmark]

def algorithm_names(algos:list):
    names = []
    for algo in algos:
        names.append( algo.__name__.split("_")[0])
    return names



# === INPUT

def read_all_inputs(inputPath):
    input_files = [f for f in os.listdir(inputPath) if os.path.isfile(os.path.join(inputPath, f))]
    input_count = len(input_files)
    input_buffers = []
    for filename in input_files:
        filepath = os.path.join(inputPath, filename)
        input_buffers.append(readBuffer(filepath))
    print("Input from: ", inputPath, " read, with length = ", len(input_buffers))
    print("Length of byte of each input = ", [len(input_buffers[i]) for i in range(len(input_buffers))])
    return input_buffers



# === OUTPUT

def create_output(output_path:str, loop_time:int, 
                algorithm_names:list, encode_avg_times:list, decode_avg_times:list, 
                min_ratio:list, avg_ratio:list, max_ratio:list, keep_content_bools:list):
                
    output_time = time.asctime().replace(" ", "_").replace(":","-")
    output_dict = {
        "output_time": output_time,
        "loop_time": loop_time,
        "algorithms": algorithm_names,
        "encode_time": encode_avg_times,
        "decode_time": decode_avg_times,
        "min_ratio": min_ratio,
        "avg_ratio": avg_ratio,
        "max_ratio": max_ratio,
        "keep_content": keep_content_bools
    }
    output_json = json.dumps(output_dict, indent=2)
    fo = open(os.path.join(output_path, output_time + ".json"), "w")
    fo.write(output_json)
    fo.close()
    print("Output saved: ", output_time)


# === MAIN

loop_time = args.l

def Benchmark(inputPath, outputPath, algorithms): 
    encode_avg_times, decode_avg_times = [0 for i in range(len(algorithms))], [0 for i in range(len(algorithms))]
    min_ratios, avg_ratios, max_ratios = [99999 for i in range(len(algorithms))], [0 for i in range(len(algorithms))], [-1 for i in range(len(algorithms))]
    keep_content_bools = [True for i in range(len(algorithms))]
    comp_size, decomp_size = [-1 for i in range(len(algorithms))], [-1 for i in range(len(algorithms))]


    inputs = read_all_inputs(inputPath)
    algo_idx = -1

    for algo in algorithms:
        algo_idx += 1
        print("\nAlgo ", algo_idx)
        for input_idx in range(len(inputs)):    
            print("Input ", input_idx)
            for l in range(loop_time):
                encode_avg_time, decode_avg_time, ratio, keep_content, comp_buffer, decomp_buffer = algo(inputs[input_idx])
                # if (comp_size[algo_idx] > -1):
                #     assert (len(comp_buffer) > 0) 
                #     print(len(comp_buffer), comp_size[algo_idx])
                #     assert (len(comp_buffer) == comp_size[algo_idx])     # check if algo produce same result
                # else:
                #     comp_size[algo_idx] = len(comp_buffer)

                keep_content_bools[algo_idx] &= keep_content
                encode_avg_times[algo_idx] = (encode_avg_times[algo_idx] * (input_idx*loop_time + l) + encode_avg_time) / (input_idx*loop_time + l+1)
                decode_avg_times[algo_idx] = (decode_avg_times[algo_idx] * (input_idx*loop_time + l) + decode_avg_time) / (input_idx*loop_time + l+1)
                min_ratios[algo_idx], max_ratios[algo_idx] = min(min_ratios[algo_idx], ratio), max(max_ratios[algo_idx], ratio)
                avg_ratios[algo_idx] = (avg_ratios[algo_idx] * (input_idx*loop_time + l) + ratio) / (input_idx*loop_time + l+1)

    create_output(outputPath, loop_time, algorithm_names(algorithms), encode_avg_times, decode_avg_times,
                min_ratios, avg_ratios, max_ratios, keep_content_bools)


Benchmark(args.i, args.o, benchmark_algorithms)