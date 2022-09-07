#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to calculate the indices"""

import reading
import glob
import numpy as np

# The functions all have the same structure:
# 1. handle resolution input (test if empty -> highest, if not 10 -> change 08 to 8A)
# 2. look for files with specific bands in their names using glob.glob and *
# 3. parse the path to the files into read_raster() with clip information
# 4. calculate index with read rasterfiles, save results as txt-file and return the index as ndarray next to the final resolution after handling


def ndvi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDVI (Normalized Difference Vegetation Index)"""
    if resolution == "" or resolution == "10":
        resolution = "10"
        for item in glob.glob(
            raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"
        ):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(
            raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"
        ):
            b8_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"
    ):
        b4_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    np.seterr(divide="ignore", invalid="ignore")
    ndvi = (b8 - b4) / (b8 + b4)
    np.savetxt("./data/ndvi.txt", ndvi)
    return ndvi, resolution


def ndmi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDMI (Normalized Difference Moisture Index)"""
    if resolution == "":
        resolution = "20"
    elif resolution == "10":
        print("NDMI cannot be calculated with a spatial resolution of 10m.")
        resolution = "20"
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"
    ):
        b8a_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B11*.jp2"
    ):
        b11_path = item
    b8a = reading.read_raster(b8a_path, clip_shape)
    b11 = reading.read_raster(b11_path, clip_shape)
    np.seterr(divide="ignore", invalid="ignore")
    ndmi = (b8a - b11) / (b8a + b11)
    np.savetxt("./data/ndmi.txt", ndmi)
    return ndmi, resolution


def ndwi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDWI (Normalized Difference Water Index)"""
    if resolution == "" or resolution == "10":
        resolution = "10"
        for item in glob.glob(
            raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"
        ):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(
            raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"
        ):
            b8_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B03*.jp2"
    ):
        b3_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    np.seterr(divide="ignore", invalid="ignore")
    ndwi = (b3 - b8) / (b3 + b8)
    np.savetxt("./data/ndwi.txt", ndwi)
    return ndwi, resolution


def savi_calc(resolution, raster_path, clip_shape, optional_val):
    """Calculation of the NDWI (Normalized Difference Water Index)"""
    if optional_val == "":
        optional_val = 0.5
    if resolution == "" or resolution == "10":
        resolution = "10"
        for item in glob.glob(
            raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"
        ):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(
            raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"
        ):
            b8_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"
    ):
        b4_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    np.seterr(divide="ignore", invalid="ignore")
    savi = ((b8 - b4) / (b8 + b4 + optional_val)) * (1 + optional_val)
    np.savetxt("./data/savi.txt", savi)
    return savi, resolution


def reip_calc(resolution, raster_path, clip_shape):
    """Calculation of the REIP (Red-Edge Inflection Point)"""
    if resolution == "":
        resolution = "20"
    elif resolution == "10":
        print("REIP cannot be calculated with a spatial resolution of 10m.")
        resolution = "20"
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"
    ):
        b4_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B05*.jp2"
    ):
        b5_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B06*.jp2"
    ):
        b6_path = item
    for item in glob.glob(
        raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B07*.jp2"
    ):
        b7_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    b6 = reading.read_raster(b6_path, clip_shape)
    b7 = reading.read_raster(b7_path, clip_shape)
    np.seterr(divide="ignore", invalid="ignore")
    reip = 700 + 40 * ((b4 + b7) / 2 - b5) / (b6 - b5)
    np.savetxt("./data/reip.txt", reip)
    return reip, resolution
