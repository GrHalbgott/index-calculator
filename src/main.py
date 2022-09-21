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
        satellite,
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
    if satellite in ["s2", "sentinel2", "sentinel"]:
        result, calc_resolution = utils.index_calculator_s2(
            index_name, resolution, raster_path, clip_shape, optional_val
        )
    elif satellite in ["l8", "landsat8", "landsat"]:
        result = utils.index_calculator_l8(index_name, raster_path, clip_shape, optional_val)
        calc_resolution = 30
    else:
        print(
            "ERROR: Your specified satellite dataset cannot be used yet or doesn't exist.\n Please provide a valid request, check the README for a list of possible datasets."
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

    starttime2 = time.time()

    if any([want_txt_saved == "true", want_raster_saved == "true", want_statistics == "true"]):
        print("\nAdditional outputs are generated...")

        # write txt file with results/ndarray
        writing.write_txt(index_name, result, want_txt_saved)

        # export as raster tif-file
        writing.write_raster(index_name, calc_resolution, raster_path, clip_shape, want_raster_saved, result)

        # generate statistics (histogram & descriptives)
        writing.write_statistics(index_name, result, calc_resolution, want_statistics)

        print("...cleaning up...")
    else:
        print("\nCleaning up...")

    # delete any temporary files, works only if the program finished entirely
    utils.cleanup_temp()

    stoptime2 = time.time()

    print("...finished. \nThis took another {:.2f} seconds.".format(stoptime2 - starttime2))


if __name__ == "__main__":
    main()
