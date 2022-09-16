#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities (check inputs, choose index function, plot)"""


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
