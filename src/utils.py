#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities (check inputs, choose index function, plot)"""


import indices
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np


def _check_input_arguments():
    """Some error-handling and interaction for the optional input values: clip raster to shapefile, index name, resolution, optional value (e.g. L in SAVI) and whether user wants to save the plot locally"""
    # Initialize argparse and specify the optional arguments
    help_msg = "Calculate an index with Sentinel-2 satellite imagery. You can use the following options to adapt the calculation to your needs. Have fun!"
    parser = argparse.ArgumentParser(description=help_msg, prefix_chars="-")
    parser._action_groups.pop()
    # use two groups of inputs (required and optional)
    required_args = parser.add_argument_group("required arguments")
    optional_args = parser.add_argument_group("optional arguments")
    required_args.add_argument(
        "-i",
        metavar="Index name",
        dest="index_name",
        help="String | Choose which index gets calculated. Check the README for a list of possible indices.",
        required=True,
    )
    optional_args.add_argument(
        "-c",
        metavar="Clip",
        dest="clip_shape",
        help="String | Clip raster to shapefile with shapefile. Use the name and file-type only (like roi.shp). Default value: None",
        default="",
    )
    optional_args.add_argument(
        "-r",
        metavar="Resolution",
        dest="resolution",
        help="Integer | The indices can be calculated with different resolutions (10, 20, 60 (meters)). Default value: highest resolution possible",
        default="",
    )
    optional_args.add_argument(
        "-ov",
        metavar="Optional value",
        dest="optional_val",
        help="Integer | Some indices need additional values like the L-value in SAVI. Default value: as in literature",
        default="",
    )
    optional_args.add_argument(
        "-sp",
        metavar="Save plot",
        dest="want_plot_saved",
        help="Boolean | Do you want to automatically save the plot locally to ./data/? Use true/false. Default: false",
        default="false",
    )
    optional_args.add_argument(
        "-txt",
        metavar="Save as txt",
        dest="want_txt_saved",
        help="Boolean | Do you want to automatically save the results/ndarray as txt-file locally to ./data/? Use true/false. Default: false",
        default="false",
    )
    # show help dialog if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        print(" \nExiting program, call again to run. Use -h or --help to show the help dialog.")
        sys.exit(1)
    else:
        # initialize arguments of parser
        args = parser.parse_args()
    # Assign arguments to variables and do some checks for error-handling
    index_name = args.index_name.lower()
    clip_shape = args.clip_shape
    resolution = args.resolution
    optional_val = args.optional_val
    want_plot_saved = args.want_plot_saved.lower()
    want_txt_saved = args.want_txt_saved.lower()

    if clip_shape != "":
        while clip_shape[-4] != "." and clip_shape[-3] != ".":
            clip_shape = input("Cannot read shapefile, please input a valid shapefile (like roi.shp): ")

    while resolution not in ["10", "20", "60", ""]:
        print("Your specified resolution cannot be used. Please provide a valid request (10, 20, 60).")
        resolution = input("Enter the desired spatial resolution: ")

    if optional_val != "":
        optional_val = int(args.optional_val)

    return (
        index_name,
        clip_shape,
        resolution,
        optional_val,
        want_plot_saved,
        want_txt_saved,
    )


def index_calculator(index_name, resolution, raster_path, clip_shape, optional_val, want_txt_saved):
    """Calculates the desired index and returns a ndarray (raster)"""
    # only specific indices can be calculated with a spatial resolution of 10 m
    if index_name in ["ndbi", "ndmi", "ndre", "ndsi", "reip"]:
        if resolution == "":
            resolution = "20"
        elif resolution == "10":
            print("{} cannot be calculated with a spatial resolution of 10 m.".format(index_name.upper()))
            resolution = "20"
    else:
        pass
    np.seterr(divide="ignore", invalid="ignore")
    if index_name == "ndbi":
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
    elif index_name == "vari":
        result, calc_resolution = indices.vari_calc(resolution, raster_path, clip_shape)
    else:
        print(
            "Your specified index cannot be calculated yet or doesn't exist.\n Please provide a valid request, check the README for a list of possible indices."
        )
        sys.exit()
    # checks if the user wants to locally save the results as txt-file as well
    while want_txt_saved not in ["true", "false"]:
        want_txt_saved = input("Do you want to save the results/ndarray as txt-file as well? Use y/n: ")
        if want_txt_saved in ["y", "yes"] or want_txt_saved in ["n", "no"]:
            break
        print("Please provide a valid input.")
    if want_txt_saved in ["y", "yes", "true"]:
        np.savetxt("./data/{}.txt".format(index_name), result)
    else:
        pass
    return result, calc_resolution


def index_plot(index_name, result):
    """Choose parameters for the plot depending on the calculated index"""
    if index_name in ["ndbi"]:
        plt.imshow(result, cmap="BrBG")
        plt.clim(-0.1, 0.1)
    elif index_name in ["ndmi"]:
        plt.imshow(result, cmap="jet_r")
        plt.clim(-0.2, 0.4)
    elif index_name in ["ndwi"]:
        plt.imshow(result, cmap="seismic_r")
        plt.clim(-0.8, 0.8)
    elif index_name in ["ndre", "ndvi", "savi", "vari"]:
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-0.15, 0.45)
    elif index_name in ["ndsi"]:
        plt.imshow(result, cmap="Blues")
        plt.clim(0.2, 0.42)
    elif index_name in ["reip"]:
        plt.imshow(result, cmap="Greens")
        plt.clim(705, 740)
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
    # checks if the user wants to locally save the figure as well
    while want_plot_saved not in ["true", "false"]:
        want_plot_saved = input("Do you want to save the plot as figure? Use y/n: ")
        if want_plot_saved in ["y", "yes"] or want_plot_saved in ["n", "no"]:
            break
        print("Please provide a valid input.")
    if want_plot_saved in ["y", "yes", "true"]:
        plt.savefig("./{}_{}.png".format(index_name.lower(), calc_resolution))
    else:
        pass
    plt.tight_layout()
    plt.show()
