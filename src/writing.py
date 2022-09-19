#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to write data (raster/txt/plots)"""


import glob
import warnings
import rasterio
import matplotlib.pyplot as plt
import numpy as np


def write_clip(out_raster, out_image, out_transform, out_meta):
    """Use metadata of masked raster file to write a new clipped raster file"""
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


def write_txt(index_name, result, want_txt_saved):
    """Checks if the user wants to locally save the results as txt-file and does it"""
    while want_txt_saved not in ["true", "false"]:
        want_txt_saved = input("Do you want to save the results/ndarray as txt-file as well? Use y/n: ")
        if want_txt_saved in ["y", "yes"] or want_txt_saved in ["n", "no"]:
            break
        print("ERROR: Please provide a valid input.")
    if want_txt_saved in ["y", "yes", "true"]:
        print("...writing result to file...")
        np.savetxt("./results/{}.txt".format(index_name), result)
    else:
        pass


def save_plot(want_plot_saved, index_name, calc_resolution):
    """Checks if the user wants to locally save the figure and does it"""
    while want_plot_saved not in ["true", "false"]:
        want_plot_saved = input("Do you want to save the plot as figure? Use y/n: ")
        if want_plot_saved in ["y", "yes"] or want_plot_saved in ["n", "no"]:
            break
        print("ERROR: Please provide a valid input.")
    if want_plot_saved in ["y", "yes", "true"]:
        print("Plot saved to file.")
        plt.savefig("./results/{}_{}.png".format(index_name.lower(), calc_resolution), bbox_inches="tight")
    else:
        pass


def write_raster(index_name, calc_resolution, raster_path, clip_shape, want_raster_saved, result):
    """Checks if the user wants to export the results as tif-file and does it"""
    while want_raster_saved not in ["true", "false"]:
        want_raster_saved = input("Do you want to export the results as tif-file? Use y/n: ")
        if want_raster_saved in ["y", "yes"] or want_raster_saved in ["n", "no"]:
            break
        print("ERROR: Please provide a valid input.")
    if want_raster_saved in ["y", "yes", "true"]:
        print("...exporting raster to file...")
        # search for reference raster
        if clip_shape != "":
            for item in glob.glob("./data/*.tif"):
                in_raster = item
        else:
            for item in glob.glob(raster_path + "*/GRANULE/*/IMG_DATA/R" + calc_resolution + "m/*_B02*.jp2"):
                in_raster = item

        # read metadata of raster
        with rasterio.open(in_raster, "r") as src:
            res_meta = src.profile
            res_meta.update(
                {
                    "dtype": "float64",
                    "nodata": np.nan,
                }
            )

        # open a new raster file and write the information into it
        with rasterio.open("./results/{}.tif".format(index_name), "w", **res_meta) as dest:
            dest.write(result, indexes=1)
    else:
        pass


def write_statistics(index_name, result, calc_resolution, want_statistics):
    """Checks if the user wants to generate statistics and does it"""
    while want_statistics not in ["true", "false"]:
        want_statistics = input("Do you want to generate statistics? Use y/n: ")
        if want_statistics in ["y", "yes"] or want_statistics in ["n", "no"]:
            break
        print("ERROR: Please provide a valid input.")
    if want_statistics in ["y", "yes", "true"]:
        warnings.filterwarnings(action="ignore", message="All-NaN slice encountered")
        # generate histogram and save it as file
        plt.figure()
        plt.title(
            "Calculated {} for region of interest with spatial resolution of {} m".format(
                index_name.upper(), calc_resolution
            )
        )
        plt.xlabel("X-Axis")
        plt.ylabel("Y-Axis")
        print("...generating histogram...")
        if index_name in ["gci", "reip", "savi", "sipi"]:
            print("...cannot calculate yet. Check issues...")
            return
        else:
            plt.hist(result, range=[-1, 1])
        print("...deriving statistics...")
        plt.figtext(
            0.91,
            0.7,
            "Statistics of {} \n  Minimum: {:.2f}\n  Maximum: {:.2f}\n  Mean: {:.2f}\n  Std.dev: {:.2f}".format(
                index_name.upper(), np.nanmin(result), np.nanmax(result), np.nanmean(result), np.nanstd(result)
            ),
        )
        print("...saving statistical results...")
        plt.savefig("./results/{}_hist.png".format(index_name.lower()), bbox_inches="tight")
