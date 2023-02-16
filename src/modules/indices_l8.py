#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to calculate the indices for Landsat 8/9 images"""


import modules.reading as reading
import glob


# The functions all have the same structure:
# 1. handle resolution and/or optional_val input
# 2. look for files with specific bands in their names using glob.glob and *
# 3. parse the path to the files into read_raster() with clip information
# 4. calculate index with read rasterfiles and return the index as ndarray next to the final resolution


def arvi_calc(raster_path, clip_shape, optional_val):
    """Calculation of the ARVI"""
    if optional_val == "":
        optional_val = 2
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B2.tif"):
        b2_path = item
    for item in glob.glob(raster_path + "L*/*_B4.tif"):
        b4_path = item
    b2 = reading.read_raster(b2_path, clip_shape)
    b4 = reading.read_raster(b4_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    arvi = (b5 - b4 - optional_val * (b4 - b2)) / (b5 + b4 - optional_val * (b4 - b2))
    return arvi


def gci_calc(raster_path, clip_shape):
    """Calculation of the GCI"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B3.tif"):
        b3_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    gci = b5 / b3 - 1
    return gci


def nbr_calc(raster_path, clip_shape):
    """Calculation of the NBR"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B7.tif"):
        b7_path = item
    b5 = reading.read_raster(b5_path, clip_shape)
    b7 = reading.read_raster(b7_path, clip_shape)
    nbr = (b5 - b7) / (b5 + b7)
    return nbr


def nbr2_calc(raster_path, clip_shape):
    """Calculation of the NBR2"""
    for item in glob.glob(raster_path + "L*/*_B6.tif"):
        b6_path = item
    for item in glob.glob(raster_path + "L*/*_B7.tif"):
        b7_path = item
    b6 = reading.read_raster(b6_path, clip_shape)
    b7 = reading.read_raster(b7_path, clip_shape)
    nbr2 = (b6 - b7) / (b6 + b7)
    return nbr2


def ndbi_calc(raster_path, clip_shape):
    """Calculation of the NDBI"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B6.tif"):
        b6_path = item
    b5 = reading.read_raster(b5_path, clip_shape)
    b6 = reading.read_raster(b6_path, clip_shape)
    ndbi = (b6 - b5) / (b6 + b5)
    return ndbi


def ndmi_calc(raster_path, clip_shape):
    """Calculation of the NDMI"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B6.tif"):
        b6_path = item
    b5 = reading.read_raster(b5_path, clip_shape)
    b6 = reading.read_raster(b6_path, clip_shape)
    ndmi = (b5 - b6) / (b5 + b6)
    return ndmi


def ndsi_calc(raster_path, clip_shape):
    """Calculation of the NDSI"""
    for item in glob.glob(raster_path + "L*/*_B3.tif"):
        b3_path = item
    for item in glob.glob(raster_path + "L*/*_B6.tif"):
        b6_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b6 = reading.read_raster(b6_path, clip_shape)
    ndsi = (b3 - b6) / (b3 + b6)
    return ndsi


def ndvi_calc(raster_path, clip_shape):
    """Calculation of the NDVI"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B4.tif"):
        b4_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    ndvi = (b5 - b4) / (b5 + b4)
    return ndvi


def ndwi_calc(raster_path, clip_shape):
    """Calculation of the NDWI"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B3.tif"):
        b3_path = item
    b3 = reading.read_raster(b3_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    ndwi = (b3 - b5) / (b3 + b5)
    return ndwi


def savi_calc(raster_path, clip_shape, optional_val):
    """Calculation of the SAVI"""
    if optional_val == "":
        optional_val = 0.5
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B4.tif"):
        b4_path = item
    b4 = reading.read_raster(b4_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    savi = ((b5 - b4) / (b5 + b4 + optional_val)) * (1 + optional_val)
    return savi


def sipi_calc(raster_path, clip_shape):
    """Calculation of the SIPI"""
    for item in glob.glob(raster_path + "L*/*_B5.tif"):
        b5_path = item
    for item in glob.glob(raster_path + "L*/*_B2.tif"):
        b2_path = item
    for item in glob.glob(raster_path + "L*/*_B4.tif"):
        b4_path = item
    b2 = reading.read_raster(b2_path, clip_shape)
    b4 = reading.read_raster(b4_path, clip_shape)
    b5 = reading.read_raster(b5_path, clip_shape)
    sipi = (b5 - b2) / (b5 - b4)
    return sipi
