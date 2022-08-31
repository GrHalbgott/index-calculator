#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to calculate indices"""

import sys
import glob
import fiona
import rasterio
import rasterio.mask
import rasterio.features
import rasterio.warp
import numpy as np


def calc_index(index_name, raster_path):
    """Calculates the desired index and returns a ndarray (raster)"""
    if index_name in {"NDMI", "ndmi", 1}:
        result = ndmi_calc(raster_path)
    elif index_name in {"NDVI", "ndvi", 2}:
        result = ndvi_calc(raster_path)
    elif index_name in {"REIP", "reip", 3}:
        result = reip_calc(raster_path)
    elif index_name in {"RGB", "rgb", 4}:
        result = rgb_calc(raster_path)
    return result


def ndmi_calc(raster_path):
    """Calculation of the NDMI-index (Normalized Difference Moisture Index)"""
    for item in glob.glob(raster_path + "*_B8A*.jp2"):
        b8a_path = item
    for item in glob.glob(raster_path + "*_B11*.jp2"):
        b11_path = item
    b8a = read_raster(b8a_path)
    b11 = read_raster(b11_path)
    np.seterr(divide="ignore", invalid="ignore")
    ndmi = (b8a - b11) / (b8a + b11)
    np.savetxt("ndmi.txt", ndmi)
    print(str(np.nanmax(ndmi)) + " max | min " + str(np.nanmin(ndmi)))
    return ndmi


def ndvi_calc(raster_path):
    """Calculation of the NDVI-index (Normalized Difference Vegetation Index)"""
    for item in glob.glob(raster_path + "*_B04*.jp2"):
        b4_path = item
    for item in glob.glob(
        raster_path + "*_B8A*.jp2"
    ):  # Band 8 not existent with 20m resolution
        b8_path = item
    b4 = read_raster(b4_path)
    b8 = read_raster(b8_path)
    np.seterr(divide="ignore", invalid="ignore")
    ndvi = (b8 - b4) / (b8 + b4)
    np.savetxt("ndvi.txt", ndvi)
    print(str(np.nanmax(ndvi)) + " max | min " + str(np.nanmin(ndvi)))
    return ndvi


def reip_calc(raster_path):
    """Calculation of the REIP-index (Red-Edge Inflection Point)"""
    for item in glob.glob(raster_path + "*_B04*.jp2"):
        b4_path = item
    for item in glob.glob(raster_path + "*_B05*.jp2"):
        b5_path = item
    for item in glob.glob(raster_path + "*_B06*.jp2"):
        b6_path = item
    for item in glob.glob(raster_path + "*_B07*.jp2"):
        b7_path = item
    b4 = read_raster(b4_path)
    b5 = read_raster(b5_path)
    b6 = read_raster(b6_path)
    b7 = read_raster(b7_path)
    np.seterr(divide="ignore", invalid="ignore")
    reip = 700 + 40 * ((b4 + b7) / 2 - b5) / (b6 - b5)
    np.savetxt("reip.txt", reip)
    print(str(np.nanmax(reip)) + " max | min " + str(np.nanmin(reip)))
    return reip


def rgb_calc(raster_path):
    """Calculation of RGB-Composite (Red Green Blue Image)"""
    for item in glob.glob(raster_path + "*_B02*.jp2"):
        b2_path = item
    for item in glob.glob(raster_path + "*_B03*.jp2"):
        b3_path = item
    for item in glob.glob(raster_path + "*_B04*.jp2"):
        b4_path = item
    b2 = read_raster(b2_path)
    b3 = read_raster(b3_path)
    b4 = read_raster(b4_path)
    np.seterr(divide="ignore", invalid="ignore")
    rgb = b2 + b3 + b4
    np.savetxt("rgb.txt", rgb)
    print(str(np.nanmax(rgb)) + " max | min " + str(np.nanmin(rgb)))
    return rgb


def read_raster(in_raster):
    """
    Read the input files as Numpy arrays and preprocess them
    param in_dem: path to input file (string)
    output: returns a Numpy array (Null values are np.nan)
    """
    if len(sys.argv) == 3:
        print("...cutting raster {}...".format(in_raster))
        in_shape = r"./data/shapes/" + sys.argv[1]
        raster = cut(in_raster, in_shape)
    else:
        raster = in_raster
    try:
        print("...reading raster {}...".format(raster))
        dataset = rasterio.open(raster, "r+")
    except Exception as err:
        print("...unable to open file: ", str(err), "\nPlease check your input file.")
        sys.exit()
    # Read the dataset's valid data mask as a ndarray.
    dataset.nodata = None
    dataset.indexes
    # specify the band which shall be read
    band = dataset.read(1)
    print("...reading worked.")
    return band


def cut(in_raster, in_shape):
    """Cut raster file with shape file and generate new raster output file as TIF"""
    out_raster = in_raster[:-4] + "_cut.tif"
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
        with rasterio.open(out_raster, "w", **out_meta) as dest:
            dest.write(out_image)
    except Exception as err:
        print("...unable to cut raster: ", str(err), "\nPlease check your input files.")
        sys.exit()
    print("...cutting worked.")
    return out_raster
