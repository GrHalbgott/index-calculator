#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities (choose: index function, resolution, plot range; function to plot)"""


import indices
import writing
import sys
import matplotlib.pyplot as plt
import numpy as np


def index_calculator(index_name, resolution, raster_path, clip_shape, optional_val):
    """Calculates the desired index and returns a ndarray (raster)"""
    resolution = resolution_handler(index_name, resolution)
    np.seterr(divide="ignore", invalid="ignore")
    if index_name == "arvi":
        result, calc_resolution = indices.arvi_calc(resolution, raster_path, clip_shape, optional_val)
    elif index_name == "gci":
        result, calc_resolution = indices.gci_calc(resolution, raster_path, clip_shape)
    elif index_name == "gndvi":
        result, calc_resolution = indices.gndvi_calc(resolution, raster_path, clip_shape)
    elif index_name == "ndbi":
        result, calc_resolution = indices.ndbi_calc(resolution, raster_path, clip_shape)
    elif index_name == "ndmi":
        result, calc_resolution = indices.ndmi_calc(resolution, raster_path, clip_shape)
    elif index_name == "ndre":
        result, calc_resolution = indices.ndre_calc(resolution, raster_path, clip_shape)
    elif index_name == "ndsi":
        result, calc_resolution = indices.ndsi_calc(resolution, raster_path, clip_shape)
    elif index_name == "ndvi":
        result, calc_resolution = indices.ndvi_calc(resolution, raster_path, clip_shape)
    elif index_name == "ndwi":
        result, calc_resolution = indices.ndwi_calc(resolution, raster_path, clip_shape)
    elif index_name == "reip":
        result, calc_resolution = indices.reip_calc(resolution, raster_path, clip_shape)
    elif index_name == "savi":
        result, calc_resolution = indices.savi_calc(resolution, raster_path, clip_shape, optional_val)
    elif index_name == "sipi":
        result, calc_resolution = indices.sipi_calc(resolution, raster_path, clip_shape)
    else:
        print(
            "Your specified index cannot be calculated yet or doesn't exist.\n Please provide a valid request, check the README for a list of possible indices."
        )
        sys.exit()
    return result, calc_resolution


def resolution_handler(index_name, resolution):
    """Only specific indices can be calculated with a spatial resolution of 10 m"""
    if index_name in ["gndvi"]:
        if resolution == "":
            resolution = "60"
        elif resolution == "10" or resolution == "20":
            print("{} can only be calculated with a spatial resolution of 60 m.".format(index_name.upper()))
            resolution = "60"
    elif index_name in ["ndbi", "ndmi", "ndre", "ndsi", "reip"]:
        if resolution == "":
            resolution = "20"
        elif resolution == "10":
            print("{} cannot be calculated with a spatial resolution of 10 m.".format(index_name.upper()))
            resolution = "20"
    elif index_name in ["arvi", "gci", "ndvi", "ndwi", "savi", "sipi"]:
        if resolution == "":
            resolution = "10"
    return resolution


def index_plot(index_name, result):
    """Choose parameters for the plot depending on the calculated index"""
    if index_name in ["arvi"]:
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-0.2, 0.8)  # range -1 to 1
    elif index_name in ["gci"]:
        plt.imshow(result, cmap="Greens_r")
        plt.clim(0, 1.1)  # range 0 to 2
    elif index_name in ["ndbi"]:
        plt.imshow(result, cmap="BrBG")
        plt.clim(-0.1, 0.1)  # range -1 to 1
    elif index_name in ["ndmi"]:
        plt.imshow(result, cmap="jet_r")
        plt.clim(-0.2, 0.4)  # range -1 to 1
    elif index_name in ["ndwi"]:
        plt.imshow(result, cmap="BrBG")
        plt.clim(-0.5, 0.3)  # range -1 to 1
    elif index_name in ["gndvi", "ndre", "ndvi", "savi"]:
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-0.15, 0.45)  # range -1 to 1
    elif index_name in ["ndsi"]:
        plt.imshow(result, cmap="Blues")
        plt.clim(0.2, 0.42)  # range -1 to 1
    elif index_name in ["reip"]:
        plt.imshow(result, cmap="Greens")
        plt.clim(705, 740)  # range 705 to 740
    elif index_name in ["sipi"]:
        plt.imshow(result, cmap="Greens")
        plt.clim(0.7, 1.8)  # range 0 to 2
    else:
        plt.imshow(result)  # viridis is the default cmap


def plot_result(index_name, result, calc_resolution, want_plot_saved):
    """Depending on the index, this plots the calculated results differently"""
    plt.figure()
    plt.title(
        "Calculated {} for region of interest with spatial resolution of {} m".format(
            index_name.upper(), calc_resolution
        )
    )
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    # use different cmaps and limits depending on the calculated index
    index_plot(index_name, result)
    # plot a colorbar with the same height as the plot
    im_ratio = result.shape[0] / result.shape[1]
    plt.colorbar(fraction=0.04625 * im_ratio)
    writing.save_plot(index_name, calc_resolution, want_plot_saved)
    plt.tight_layout()
    plt.show()
