#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to calculate indices"""

import sys
import fiona
import rasterio
import rasterio.mask
import rasterio.features
import rasterio.warp


def calc_index(index_name, cut_raster):
    """Calculates the desired index and returns a ndarray (raster)"""
    if index_name in {"NDMI", "ndmi", 1}:
        result = ndmi_calc(cut_raster)
    elif index_name in {"NDVI", "ndvi", 2}:
        result = ndvi_calc(cut_raster)
    elif index_name in {"REIP", "reip", 3}:
        result = reip_calc(cut_raster)
    elif index_name in {"RGB", "rgb", 4}:
        result = rgb_calc(cut_raster)
    print("...reading worked.")
    return result


def read_raster(in_raster, band_num):
    """
    Read the input files as Numpy arrays and preprocess them
    param in_dem: path to input file (string)
    output: returns a Numpy array (Null values are np.nan)
    """
    try:
        dataset = rasterio.open(in_raster, "r+")
    except Exception as err:
        print("...unable to open file: ", str(err), "\nPlease check your input file.")
        sys.exit()
    # Read the dataset's valid data mask as a ndarray.
    dataset.nodata = None
    dataset.indexes
    print("...reading the raster {}...".format(in_raster))
    # specify the band which shall be read
    band = dataset.read(band_num)
    return band


def cut(in_raster, in_shape):
    """Cut raster file with shape file and generate new raster output file"""
    output = in_raster[:-3] + "_cut.tif"
    try:
        with fiona.open(in_shape, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        with rasterio.open(in_raster) as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_meta = src.meta
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
            }
        )
        with rasterio.open(output, "w", **out_meta) as dest:
            dest.write(out_image)
    except Exception as err:
        print("...unable to cut raster: ", str(err), "\nPlease check your input files.")
        sys.exit()
    print("...cutting worked.")
    return output


def ndmi_calc(in_raster):
    """Calculation of the NDMI-index (Normalized Difference Moisture Index)"""
    b8a = read_raster(in_raster, 9)
    b11 = read_raster(in_raster, 12)
    ndmi = (b8a - b11) / (b8a + b11)
    return ndmi


def ndvi_calc(in_raster):
    """Calculation of the NDVI-index (Normalized Difference Vegetation Index)"""
    b8 = read_raster(in_raster, 8)
    b4 = read_raster(in_raster, 4)
    ndvi = (b8 - b4) / (b8 + b4)
    return ndvi


def reip_calc(in_raster):
    """Calculation of the REIP-index (Red-Edge Inflection Point)"""
    b4 = read_raster(in_raster, 4)
    b5 = read_raster(in_raster, 5)
    b6 = read_raster(in_raster, 6)
    b7 = read_raster(in_raster, 7)
    reip = 700 + 40 * ((b4 + b7) / 2 - b5) / (b6 - b5)
    return reip


def rgb_calc(in_raster):
    """Calculation of RGB-Composite (Red Green Blue Image)"""
    b1 = read_raster(in_raster, 1)
    b2 = read_raster(in_raster, 2)
    b3 = read_raster(in_raster, 3)
    rgb = b1 + b2 + b3
    return rgb
