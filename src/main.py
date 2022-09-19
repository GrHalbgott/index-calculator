#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program to calculate different indices"""


import chk_args
import utils
import writing
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
        want_raster_saved,
        want_plot,
        want_plot_saved,
        want_txt_saved,
        want_statistics,
    ) = chk_args._check_input_arguments()

    starttime1 = time.time()

    raster_path = "./data/raster/"

    print("Calculating {}...".format(index_name.upper()))
    result, calc_resolution = utils.index_calculator(
        index_name, resolution, raster_path, clip_shape, optional_val, want_raster_saved
    )

    stoptime1 = time.time()

    # print out the information to user
    print(
        "...finished calculating the {} with a spatial resolution of {} m. \nCalculating took {:.2f} seconds.".format(
            index_name.upper(), calc_resolution, stoptime1 - starttime1
        )
    )

    # plot the result/ndarray
    utils.plot_result(index_name, result, calc_resolution, want_plot, want_plot_saved)

    print("\nAdditional outputs are generated...")
    starttime2 = time.time()

    # write txt file with results/ndarray
    writing.write_txt(index_name, result, want_txt_saved)

    # export as raster tif-file
    writing.write_raster(index_name, calc_resolution, raster_path, clip_shape, want_raster_saved, result)

    # generate statistics (histogram & descriptives)
    writing.write_statistics(index_name, result, calc_resolution, want_statistics)

    # delete any temporary files
    print("Cleaning up...")
    utils.cleanup_temp()

    stoptime2 = time.time()

    print("...finished. \n   This took another {:.2f} seconds.".format(stoptime2 - starttime2))


if __name__ == "__main__":
    main()
