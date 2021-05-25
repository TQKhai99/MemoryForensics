#!/usr/bin/env python3

import argparse
import io
import math
import os
import sys
import glob
import cv2
import numpy as np

from tempfile import NamedTemporaryFile

from PIL import Image


class FileReader(object):
    def __init__(self, path_or_stream):
        self.tmpfile = None
        if hasattr(path_or_stream, "name") and path_or_stream.name != "<stdin>":
            self.length = os.path.getsize(path_or_stream.name)
            self.file = path_or_stream
            self.name = path_or_stream.name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmpfile is not None:
            self.file.close()
            os.unlink(self.tmpfile)
            self.tmpfile = None
            self.file = None

    @staticmethod
    def new(path_or_stream):
        if isinstance(path_or_stream, FileReader):
            return path_or_stream
        else:
            return FileReader(path_or_stream)

    def __len__(self):
        return self.length

    def read(self, n):
        return [i for i in self.file.read(n)]
        


def choose_file_dimensions(infile, input_dimensions=None):
    if input_dimensions is not None and len(input_dimensions) >= 2 and input_dimensions[0] is not None \
            and input_dimensions[1] is not None:
        # the dimensions were already fully specified
        return input_dimensions
    infile = FileReader.new(infile)
    num_bytes = len(infile)
    num_pixels = int(math.ceil(float(num_bytes) / 3.0))
    sqrt = math.sqrt(num_pixels)
    sqrt_max = int(math.ceil(sqrt))



    if input_dimensions is not None and len(input_dimensions) >= 1:
        if input_dimensions[0] is not None:
            # the width is specified but the height is not
            if num_pixels % input_dimensions[0] == 0:
                return input_dimensions[0], num_pixels // input_dimensions[0]
            else:
                return input_dimensions[0], num_pixels // input_dimensions[0] + 1
        else:
            # the height is specified but the width is not
            if num_pixels % input_dimensions[1] == 0:
                return num_pixels // input_dimensions[1], input_dimensions[1]
            else:
                return num_pixels // input_dimensions[1] + 1, input_dimensions[1]
	
    best_dimensions = None
    best_extra_bytes = None
   
    for i in range(int(sqrt_max), 0, -1):
        is_perfect = num_pixels % i == 0
        if is_perfect:
            return (i, num_pixels // i)
        else:
            dimensions = (i, num_pixels // i + 1)
        extra_bytes = dimensions[0] * dimensions[1] * 3 - num_bytes
        if dimensions[0] * dimensions[1] >= num_pixels and (best_dimensions is None or extra_bytes < best_extra_bytes):
            best_dimensions = dimensions
            best_extra_bytes = extra_bytes
        if dimensions[0] < dimensions[1]/3 :
            break
            
    return best_dimensions


def file_to_png(infile, outfile, dimensions=None,resize=None):
    reader = FileReader.new(infile)
    dimensions = choose_file_dimensions(reader, dimensions)
    print(dimensions)
    dim = (int(dimensions[0]), int(dimensions[1]))
    img = Image.new('RGB', dim)
    
    pixels = img.load()
    row = 0
    column = -1
    while True:
        b = reader.read(3)
        if not b:
            break

        column += 1
        if column >= img.size[0]:
            column = 0
            row += 1

            if row >= img.size[1]:
                raise Exception("Error: row %s is greater than maximum rows in image, %s." % (row, img.size[1]))

        color = [b[0], 0, 0]
        if len(b) > 1:
            color[1] = b[1]
        if len(b) > 2:
            color[2] = b[2]
        if not row >= img.size[1]:
            pixels[column, row] = tuple(color)
    if sys.version_info.major >= 3 and outfile.name == '<stdout>' and hasattr(outfile, 'buffer'):
        outfile = outfile.buffer
    
    if resize is not None:
    	cv_interpolation = cv2.INTER_LANCZOS4
    	img = cv2.resize(np.array(img), dsize=(resize[0],resize[1]), interpolation=cv_interpolation)
    	img = Image.fromarray(img)
    	
    img.save(outfile, format="PNG")


def main(argv=None):
    parser = argparse.ArgumentParser(description="A simple cross-platform script for encoding any binary file into a "
                                                 "lossless PNG.", prog="bin2png")
    read_mode = 'rb'
    write_mode = 'wb'
    out_default = sys.stdout.buffer

    parser.add_argument('file', type=argparse.FileType(read_mode), default=sys.stdin,
                        help="the file to encode as a PNG (defaults to '-', which is stdin)")
    parser.add_argument('-infile', type=argparse.FileType(read_mode), default=sys.stdin,
                        help="the file to encode as a PNG (defaults to '-', which is stdin)")
    parser.add_argument("-o", "--outfile", type=argparse.FileType(write_mode), default=out_default,
                        help="the output file (defaults to '-', which is stdout)")
    parser.add_argument("-d", "--decode", action="store_true", default=False,
                        help="decodes the input PNG back to a file")
    parser.add_argument("-w", "--width", type=int, default=None,
                        help="constrain the output PNG to a specific width")
    parser.add_argument("-l", "--height", type=int, default=None,
                        help="constrain the output PNG to a specific height")
    parser.add_argument("-resize",type=int, nargs="+", default=None,
                        help="Resizing an image with size (w,h)")
    if argv is None:
        argv = sys.argv

    args = parser.parse_args(argv)
    dims = None
    
    if args.height is not None or args.width is not None:
        dims = (args.width, args.height)
        
    file_to_png(args.infile, args.outfile, dimensions=dims,resize=args.resize)


if __name__ == "__main__":
    main()
