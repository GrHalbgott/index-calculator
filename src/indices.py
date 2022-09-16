#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to calculate the indices"""

import reading
import glob

# The functions all have the same structure:
# 1. handle resolution input (test if empty -> highest, if not 10 -> change 08 to 8A)
# 2. look for files with specific bands in their names using glob.glob and *
# 3. parse the path to the files into read_raster() with clip information
# 4. calculate index with read rasterfiles and return the index as ndarray next to the final resolution after handling


def arvi_calc(resolution, raster_path, clip_shape, optional_val):
    """Calculation of the ARVI"""
    if optional_val == "":
        optional_val = 2
    if resolution == "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
            b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B02*.jp2"):
        b2_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"):
        b4_path = item
    b2 = reading.read_raster(b2_path, clip_shape)
    b4 = reading.read_raster(b4_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    arvi = (b8 - b4 - optional_val * (b4 - b2)) / (b8 + b4 - optional_val * (b4 - b2))
    return arvi, resolution


def gci_calc(resolution, raster_path, clip_shape):
    """Calculation of the GCI"""
    if resolution == "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
            b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B03*.jp2"):
        b3_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    gci = b8 / b3 - 1
    return gci, resolution


def gndvi_calc(resolution, raster_path, clip_shape):
    """Calculation of the GNDVI"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B03*.jp2"):
        b3_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B09*.jp2"):
        b9_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b9 = reading.read_raster(b9_path, clip_shape)
    gndvi = (b9 - b3) / (b9 + b3)
    return gndvi, resolution


def ndbi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDBI"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
        b8a_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B11*.jp2"):
        b11_path = item
    b8a = reading.read_raster(b8a_path, clip_shape)
    b11 = reading.read_raster(b11_path, clip_shape)
    ndbi = (b11 - b8a) / (b11 + b8a)
    return ndbi, resolution


def ndmi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDMI"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
        b8a_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B11*.jp2"):
        b11_path = item
    b8a = reading.read_raster(b8a_path, clip_shape)
    b11 = reading.read_raster(b11_path, clip_shape)
    ndmi = (b8a - b11) / (b8a + b11)
    return ndmi, resolution


def ndre_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDRE"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
        b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B05*.jp2"):
        b5_path = item
    b5 = reading.read_raster(b5_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    ndre = (b8 - b5) / (b8 + b5)
    return ndre, resolution


def ndsi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDSI"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B03*.jp2"):
        b3_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B11*.jp2"):
        b11_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b11 = reading.read_raster(b11_path, clip_shape)
    ndsi = (b3 - b11) / (b3 + b11)
    return ndsi, resolution


def ndvi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDVI"""
    if resolution == "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
            b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"):
        b4_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    ndvi = (b8 - b4) / (b8 + b4)
    return ndvi, resolution


def ndwi_calc(resolution, raster_path, clip_shape):
    """Calculation of the NDWI (McFeeters 1996)"""
    if resolution == "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
            b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B03*.jp2"):
        b3_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    ndwi = (b3 - b8) / (b3 + b8)
    return ndwi, resolution


def reip_calc(resolution, raster_path, clip_shape):
    """Calculation of the REIP"""
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"):
        b4_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B05*.jp2"):
        b5_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B06*.jp2"):
        b6_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B07*.jp2"):
        b7_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    b6 = reading.read_raster(b6_path, clip_shape)
    b7 = reading.read_raster(b7_path, clip_shape)
    reip = 700 + 40 * ((b4 + b7) / 2 - b5) / (b6 - b5)
    return reip, resolution


def savi_calc(resolution, raster_path, clip_shape, optional_val):
    """Calculation of the SAVI"""
    if optional_val == "":
        optional_val = 0.5
    if resolution == "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
            b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"):
        b4_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    savi = ((b8 - b4) / (b8 + b4 + optional_val)) * (1 + optional_val)
    return savi, resolution


def sipi_calc(resolution, raster_path, clip_shape):
    """Calculation of the SIPI"""
    if resolution == "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B08*.jp2"):
            b8_path = item
    elif resolution != "10":
        for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B8A*.jp2"):
            b8_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B02*.jp2"):
        b2_path = item
    for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + resolution + "m/*_B04*.jp2"):
        b4_path = item
    b2 = reading.read_raster(b2_path, clip_shape)
    b4 = reading.read_raster(b4_path, clip_shape)
    b8 = reading.read_raster(b8_path, clip_shape)
    sipi = (b8 - b2) / (b8 - b4)
    return sipi, resolution
