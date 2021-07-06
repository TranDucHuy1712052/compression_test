import numpy
import lz4.frame
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", default="input/")
parser.add_argument(
    "-o", default="input/decoded/")

args = parser.parse_args()



def decode_vexc_files(input_folder_path:str, output_folder_path:str):
    input_files = [f for f in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, f))]
    input_count = len(input_files)
    input_buffers = []

    os.makedirs(output_folder_path, exist_ok=True)
    for filename in input_files:
        filepath = os.path.join(input_folder_path, filename)
        fi = open(filepath, "rb")
        comp_buffer = fi.read()
        decomp_buffer = lz4.frame.decompress(comp_buffer)
        fi.close()

        fo = open(os.path.join(output_folder_path, filename), "wb")
        fo.write(decomp_buffer)
        fo.close()
    print("Done decoding.")


decode_vexc_files(args.i, args.o)