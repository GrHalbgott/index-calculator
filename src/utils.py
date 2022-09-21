#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities (choose: index function, resolution, plot range; function to plot)"""


import indices_s2
import indices_l8
import writing
import os
import sys
import matplotlib.pyplot as plt
import numpy as np


def index_calculator_s2(index_name, resolution, raster_path, clip_shape, optional_val):
    """Calculates the desired index for Sentintel 2 data and returns a ndarray"""
    calc_resolution = resolution_handler(index_name, resolution)
    # ignore error messages during calculation
    np.seterr(divide="ignore", invalid="ignore")
    if index_name == "arvi":
        result, calc_resolution = indices_s2.arvi_calc(calc_resolution, raster_path, clip_shape, optional_val)
    elif index_name == "gci":
        result, calc_resolution = indices_s2.gci_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "gndvi":
        result, calc_resolution = indices_s2.gndvi_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "nbr":
        result, calc_resolution = indices_s2.nbr_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "nbr2":
        result, calc_resolution = indices_s2.nbr2_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "ndbi":
        result, calc_resolution = indices_s2.ndbi_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "ndmi":
        result, calc_resolution = indices_s2.ndmi_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "ndre":
        result, calc_resolution = indices_s2.ndre_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "ndsi":
        result, calc_resolution = indices_s2.ndsi_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "ndvi":
        result, calc_resolution = indices_s2.ndvi_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "ndwi":
        result, calc_resolution = indices_s2.ndwi_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "reip":
        result, calc_resolution = indices_s2.reip_calc(calc_resolution, raster_path, clip_shape)
    elif index_name == "savi":
        result, calc_resolution = indices_s2.savi_calc(calc_resolution, raster_path, clip_shape, optional_val)
    elif index_name == "sipi":
        result, calc_resolution = indices_s2.sipi_calc(calc_resolution, raster_path, clip_shape)
    else:
        print(
            "ERROR: Your specified index cannot be calculated yet or doesn't exist.\n Please provide a valid request, check the README for a list of possible indices."
        )
        sys.exit()
    return result, calc_resolution


def index_calculator_l8(index_name, raster_path, clip_shape, optional_val):
    """Calculates the desired index for Landsat 8 data and returns a ndarray"""
    # ignore error messages during calculation
    np.seterr(divide="ignore", invalid="ignore")
    if index_name == "arvi":
        result = indices_l8.arvi_calc(raster_path, clip_shape, optional_val)
    elif index_name == "gci":
        result = indices_l8.gci_calc(raster_path, clip_shape)
    elif index_name == "nbr":
        result = indices_l8.nbr_calc(raster_path, clip_shape)
    elif index_name == "nbr2":
        result = indices_l8.nbr2_calc(raster_path, clip_shape)
    elif index_name == "ndbi":
        result = indices_l8.ndbi_calc(raster_path, clip_shape)
    elif index_name == "ndmi":
        result = indices_l8.ndmi_calc(raster_path, clip_shape)
    elif index_name == "ndsi":
        result = indices_l8.ndsi_calc(raster_path, clip_shape)
    elif index_name == "ndvi":
        result = indices_l8.ndvi_calc(raster_path, clip_shape)
    elif index_name == "ndwi":
        result = indices_l8.ndwi_calc(raster_path, clip_shape)
    elif index_name == "savi":
        result = indices_l8.savi_calc(raster_path, clip_shape, optional_val)
    elif index_name == "sipi":
        result = indices_l8.sipi_calc(raster_path, clip_shape)
    else:
        print(
            "ERROR: Your specified index cannot be calculated yet or doesn't exist.\n Please provide a valid request, check the README for a list of possible indices."
        )
        sys.exit()
    return result


def resolution_handler(index_name, resolution):
    """Only specific indices can be calculated with a spatial resolution of 10 m"""
    if index_name in ["gndvi"]:
        if resolution == "":
            calc_resolution = "60"
        elif resolution == "10" or resolution == "20":
            print("{} can only be calculated with a spatial resolution of 60 m.".format(index_name.upper()))
            calc_resolution = "60"
    elif index_name in ["nbr", "nbr2", "ndbi", "ndmi", "ndre", "ndsi", "reip"]:
        if resolution == "":
            calc_resolution = "20"
        elif resolution == "10":
            print("{} cannot be calculated with a spatial resolution of 10 m.".format(index_name.upper()))
            calc_resolution = "20"
        else:
            calc_resolution = resolution
    elif index_name in ["arvi", "gci", "ndvi", "ndwi", "savi", "sipi"]:
        if resolution == "":
            calc_resolution = "10"
        else:
            calc_resolution = resolution
    return calc_resolution


def plottype_handler(index_name, result):
    """Choose parameters for the plot depending on the calculated index"""
    if index_name in ["arvi"]:
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-0.2, 0.8)  # range -1 to 1
    elif index_name in ["gci"]:
        plt.imshow(result, cmap="Greens")
        plt.clim(0, 1.1)  # range 0 to 2
    elif index_name in ["nbr", "nbr2"]:
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-1, 1)  # range -1 to 1
    elif index_name in ["ndbi", "ndwi"]:
        plt.imshow(result, cmap="BrBG")
        plt.clim(-0.1, 0.1)  # range -1 to 1
    elif index_name in ["ndmi"]:
        plt.imshow(result, cmap="jet_r")
        plt.clim(-0.2, 0.4)  # range -1 to 1
    elif index_name in ["gndvi", "ndre", "ndvi", "savi"]:
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-0.15, 0.45)  # range -1 to 1
    elif index_name in ["ndsi"]:
        plt.imshow(result, cmap="Blues")
        plt.clim(0.2, 0.42)  # range -1 to 1
    elif index_name in ["reip"]:
        plt.imshow(result, cmap="Greens")
        plt.clim(700, 740)  # range 700 to 740
    elif index_name in ["sipi"]:
        plt.imshow(result, cmap="Greens")
        plt.clim(0.7, 1.8)  # range 0 to 2
    else:
        plt.imshow(result)  # viridis is the default cmap


def plot_result(index_name, result, calc_resolution, want_plot, want_plot_saved):
    """Depending on the index, this plots the calculated results differently"""
    while want_plot not in ["true", "false"]:
        want_plot = input("Do you want to generate a plot? Use y/n: ")
        if want_plot in ["y", "yes"] or want_plot in ["n", "no"]:
            break
        print("ERROR: Please provide a valid input.")
    if want_plot in ["y", "yes", "true"]:
        plt.figure()
        plt.title(
            "Calculated {} for region of interest with spatial resolution of {} m".format(
                index_name.upper(), calc_resolution
            )
        )
        plt.xlabel("X-Axis")
        plt.ylabel("Y-Axis")
        # use different cmaps and limits depending on the calculated index
        plottype_handler(index_name, result)
        # plot a colorbar with the same height as the plot
        im_ratio = result.shape[0] / result.shape[1]
        plt.colorbar(fraction=0.04625 * im_ratio)
        # check if user wants to save the plot
        writing.save_plot(want_plot_saved, index_name, calc_resolution)
        plt.tight_layout()
        print("Awaiting user interaction to continue (close plot window)...")
        plt.show()
        print("...thanks!")
    else:
        pass


def cleanup_temp():
    """Loop through ./data/ and delete files no longer needed"""
    retain = ["raster", "shapes"]

    for item in os.listdir("./data/"):
        if item not in retain:
            os.remove("./data/" + item)
