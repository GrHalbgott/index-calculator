#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to read data (raster/vector)"""

import sys
import fiona
import rasterio
import rasterio.mask


def read_raster(in_raster, clip_shape):
    """
    Read the input files as Numpy arrays and preprocess them
    param in_dem: path to input file (string)
    output: returns a Numpy array (Null values are np.nan)
    """
    # test if a cut is found as argument, change the filepath if so
    if clip_shape is not None:
        print("...cutting raster ./data/{}...".format(in_raster[-34:]))
        in_shape = "./data/shapes/" + clip_shape
        raster = cut(in_raster, in_shape)
    else:
        # otherwise just take the original path to the rasterfile
        raster = in_raster
    try:
        # open the rasterfile in reading mode
        print("...reading raster ./data/{}...".format(raster[7:]))
        dataset = rasterio.open(raster, "r")
    except Exception as err:
        print("...unable to open file: ", str(err), "\nPlease check your input file.")
        sys.exit()
    # specify the band which shall be read and read as float54 (important!)
    band = dataset.read(1).astype("float64")
    dataset.close()
    return band


def cut(in_raster, in_shape):
    """Cut raster file with shape file and generate new raster output file as TIF"""
    # Since the in_raster variable is a long filepath, we want to cut it to only the filename
    out_raster = "./data" + in_raster[-35:-4] + "_cut.tif"
    try:
        # open the shapefile in reading mode
        with fiona.open(in_shape, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        # open the raster in reading mode to be able to write the info to a new raster file
        with rasterio.open(in_raster, "r") as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            # take the metadata of the original rasterfile
            out_meta = src.meta
        # update the metadata of the new rasterfile
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
            }
        )
        # open a new raster file and write the information into it
        with rasterio.open(out_raster, "w", **out_meta) as dest:
            dest.write(out_image)
    except Exception as err:
        print("...unable to cut raster: ", str(err), "\nPlease check your input files.")
        sys.exit()
    return out_raster
