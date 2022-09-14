#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculation of indeces"""


import utils
import sys
import time


def main():
    """
    Reads raster files as NumPy-arrays and calculate the desired index
    :return: raster image
    """
    (
        index_name,
        clip_shape,
        resolution,
        optional_val,
        want_plot_saved,
    ) = utils._check_input_arguments()

    starttime = time.time()

    raster_path = r"./data/raster/"

    print("Calculating {}...".format(index_name))
    try:
        result, calc_resolution = utils.index_calculator(
            index_name, resolution, raster_path, clip_shape, optional_val
        )
    except Exception as err:
        print(
            "...error occured when calculating the {}: {}.\n Please check your input arguments and files.".format(
                index_name, str(err)
            )
        )
        sys.exit()

    stoptime = time.time()

    # Print out the information to user
    print(
        "Finished calculating the {} with a spatial resolution of {} m. \n The script took {:.2f} seconds to run.".format(
            index_name.upper(), calc_resolution, stoptime - starttime
        )
    )

    # Plot the result (ndarray)
    utils.plot_result(index_name, result, calc_resolution, want_plot_saved)


if __name__ == "__main__":
    main()
