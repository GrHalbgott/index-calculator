#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to read data (raster/vector)"""


import utils
import writing
import sys
import os
import fiona
import rasterio
import rasterio.mask


def read_raster(in_raster, clip_shape):
    """
    Read the input files as Numpy arrays and preprocess them
    param in_dem: path to input file (string)
    output: returns a Numpy array (Null values are np.nan)
    """
    # test if a clip is found as argument, if so change the filepath
    if clip_shape != "":
        print("...clipping raster ./data/.../{}...".format(in_raster[-34:]))
        in_shape = "./data/shapes/" + clip_shape
        raster = clip(in_raster, in_shape)
        print("...reading raster ./data/{}...".format(raster[7:]))
    else:
        # otherwise just take the original path to the rasterfile
        raster = in_raster
        print("...reading raster ./data/../{}...".format(raster[-34:]))
    try:
        # open the rasterfile in reading mode
        dataset = rasterio.open(raster, "r")
    except Exception as err:
        print(
            "...unable to open raster file: ",
            str(err),
            "\nPlease check your input file.",
        )
        sys.exit()
    # specify the band which shall be read and read as float64 (important!)
    band = dataset.read(1).astype("float64")
    dataset.close()

    # delete clipped file after reading
    # if clip_shape != "":
    #     os.remove(raster)
    #     print("...deleting raster ./data/{}...".format(raster[7:]))
    # else:
    #     pass
    return band


def clip(in_raster, in_shape):
    """Clip raster file with shape file and generate new raster output file as TIF"""
    # Since the in_raster variable is a long filepath, we want to cut it to only the filename
    out_raster = "./data" + in_raster[-35:-4] + "_clipped.tif"
    try:
        # open the shapefile in reading mode
        with fiona.open(in_shape, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        # open the raster in reading mode to be able to write the info to a new raster file
        with rasterio.open(in_raster, "r") as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            # take the metadata of the original rasterfile
            out_meta = src.meta
        writing.write_clip(out_raster, out_image, out_transform, out_meta)
    except Exception as err:
        print(
            "...unable to clip raster with shapefile: ",
            str(err),
            "\nPlease check your input files.",
        )
        sys.exit()
    return out_raster
