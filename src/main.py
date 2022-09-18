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

    starttime = time.time()

    raster_path = r"./data/raster/"

    print("Calculating {}...".format(index_name))
    result, calc_resolution = utils.index_calculator(
        index_name, resolution, raster_path, clip_shape, optional_val, want_raster_saved
    )

    stoptime = time.time()

    # print out the information to user
    print(
        "...finished calculating the {} with a spatial resolution of {} m. \n The script took {:.2f} seconds to run.".format(
            index_name.upper(), calc_resolution, stoptime - starttime
        )
    )

    # write txt file with results/ndarray
    writing.write_txt(index_name, result, want_txt_saved)

    # export as raster tif-file
    writing.write_raster(index_name, calc_resolution, raster_path, clip_shape, want_raster_saved, result)

    # plot the result/ndarray
    utils.plot_result(index_name, result, calc_resolution, want_plot, want_plot_saved)

    # generate statistics (histogram & descriptives)
    writing.write_statistics(index_name, result, calc_resolution, want_statistics)

    # delete any temporary files
    utils.cleanup_temp()


if __name__ == "__main__":
    main()
