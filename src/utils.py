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
    if index_name == "ndvi":
        result = ndvi_calc(raster_path)
    elif index_name == "ndmi":
        result = ndmi_calc(raster_path)
    elif index_name == "ndwi":
        result = ndwi_calc(raster_path)
    elif index_name == "reip":
        result = reip_calc(raster_path)
    else:
        print(
            "Your specified index cannot be calculated yet or doesn't exist.\n Please provide a valid request, choose from {ndvi, ndmi, ndwi, reip}."
        )
        sys.exit()
    return result


def ndvi_calc(raster_path):
    """Calculation of the NDVI (Normalized Difference Vegetation Index)"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R10m/*_B04*.jp2"):
        b4_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R10m/*_B08*.jp2"):
        b8_path = item
    b4 = read_raster(b4_path)
    b8 = read_raster(b8_path)
    np.seterr(divide="ignore", invalid="ignore")
    ndvi = (b8 - b4) / (b8 + b4)
    np.savetxt("./data/ndvi.txt", ndvi)
    return ndvi


def ndmi_calc(raster_path):
    """Calculation of the NDMI (Normalized Difference Moisture Index)"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R20m/*_B8A*.jp2"):
        b8a_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R20m/*_B11*.jp2"):
        b11_path = item
    b8a = read_raster(b8a_path)
    b11 = read_raster(b11_path)
    np.seterr(divide="ignore", invalid="ignore")
    ndmi = (b8a - b11) / (b8a + b11)
    np.savetxt("./data/ndmi.txt", ndmi)
    return ndmi


def ndwi_calc(raster_path):
    """Calculation of the NDWI (Normalized Difference Water Index)"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R10m/*_B03*.jp2"):
        b3_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R10m/*_B08*.jp2"):
        b8_path = item
    b3 = read_raster(b3_path)
    b8 = read_raster(b8_path)
    np.seterr(divide="ignore", invalid="ignore")
    ndwi = (b3 - b8) / (b3 + b8)
    np.savetxt("./data/ndwi.txt", ndwi)
    return ndwi


def reip_calc(raster_path):
    """Calculation of the REIP (Red-Edge Inflection Point)"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R20m/*_B04*.jp2"):
        b4_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R20m/*_B05*.jp2"):
        b5_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R20m/*_B06*.jp2"):
        b6_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R20m/*_B07*.jp2"):
        b7_path = item
    b4 = read_raster(b4_path)
    b5 = read_raster(b5_path)
    b6 = read_raster(b6_path)
    b7 = read_raster(b7_path)
    np.seterr(divide="ignore", invalid="ignore")
    reip = 705 + 40 * ((b4 + b7) / 2 - b5) / (b6 - b5)
    np.savetxt("./data/reip.txt", reip)
    return reip


def read_raster(in_raster):
    """
    Read the input files as Numpy arrays and preprocess them
    param in_dem: path to input file (string)
    output: returns a Numpy array (Null values are np.nan)
    """
    if len(sys.argv) == 3:
        print("...cutting raster {}...".format(in_raster))
        in_shape = "./data/shapes/" + sys.argv[1]
        raster = cut(in_raster, in_shape)
    else:
        raster = in_raster
    try:
        print("...reading raster {}...".format(raster))
        dataset = rasterio.open(raster, "r")
    except Exception as err:
        print("...unable to open file: ", str(err), "\nPlease check your input file.")
        sys.exit()
    # specify the band which shall be read
    band = dataset.read(1).astype("float64")
    dataset.close()
    print("...reading worked.")
    return band


def cut(in_raster, in_shape):
    """Cut raster file with shape file and generate new raster output file as TIF"""
    out_raster = "./data" + in_raster[-35:-4] + "_cut.tif"
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
