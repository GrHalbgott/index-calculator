#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check arguments given with argparse"""


import sys
import argparse


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
        "-sat",
        metavar="Satellite",
        dest="satellite",
        help="String | You can use different satellite datasets (s2/sentinel2 or l8/landsat8). Default value: s2",
        default="s2",
    )
    optional_args.add_argument(
        "-r",
        metavar="Resolution",
        dest="resolution",
        help="Integer | When using Sentinel 2 datasets, the indices can be calculated with different resolutions (10, 20, 60 m). Default value: highest resolution possible",
        default="",
    )
    optional_args.add_argument(
        "-ov",
        metavar="Optional value",
        dest="optional_val",
        help="Float | Some indices need additional values like the L-value in SAVI. Default value: as in literature",
        default="",
    )
    optional_args.add_argument(
        "-tif",
        metavar="Save raster",
        dest="want_raster_saved",
        help="Boolean | Do you want to export the results/ndarray as tif-file locally to ./results/? Use true/false. Default: false",
        default="false",
    )
    optional_args.add_argument(
        "-gp",
        metavar="Generate plot",
        dest="want_plot",
        help="Boolean | Do you want to generate a plot? Use true/false. Default: true",
        default="true",
    )
    optional_args.add_argument(
        "-sp",
        metavar="Save plot",
        dest="want_plot_saved",
        help="Boolean | Do you want to save the plot locally to ./results/? Use true/false. Default: false",
        default="false",
    )
    optional_args.add_argument(
        "-txt",
        metavar="Save as txt",
        dest="want_txt_saved",
        help="Boolean | Do you want to save the results/ndarray as txt-file locally to ./results/? Use true/false. Default: false",
        default="false",
    )
    optional_args.add_argument(
        "-stat",
        metavar="Statistics",
        dest="want_statistics",
        help="Boolean | Do you want to generate statistics (histogram & descriptive) for the results and save them locally to ./results/? Use true/false. Default: false",
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
    satellite = args.satellite.lower()
    resolution = args.resolution
    optional_val = args.optional_val
    want_raster_saved = args.want_raster_saved.lower()
    want_plot = args.want_plot.lower()
    want_plot_saved = args.want_plot_saved.lower()
    want_txt_saved = args.want_txt_saved.lower()
    want_statistics = args.want_statistics.lower()

    if clip_shape != "":
        while clip_shape[-4] != "." and clip_shape[-3] != ".":
            clip_shape = input("ERROR: Cannot read shapefile, please input a valid shapefile (like roi.shp): ")

    while resolution not in ["", "10", "20", "60"]:
        print(
            "ERROR: Your specified resolution cannot be used. Please provide a valid request (10, 20, 60; Sentinel 2 only)."
        )
        resolution = input("Enter the desired spatial resolution: ")

    if satellite in ["l8", "landsat8", "landsat"]:
        resolution = 30

    if optional_val != "":
        optional_val = float(args.optional_val)

    if want_plot == "false" and want_plot_saved == "true":
        print("ERROR: Changed -gp to true. You need to generate a plot to be able to save it.")
        want_plot = "true"

    return (
        index_name,
        clip_shape,
        satellite,
        resolution,
        optional_val,
        want_raster_saved,
        want_plot,
        want_plot_saved,
        want_txt_saved,
        want_statistics,
    )
