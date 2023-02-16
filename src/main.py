#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program to calculate different indices"""


from modules.chk_args import _check_input_arguments
from modules.utils import index_calculator_l8, index_calculator_s2, plot_result, cleanup_temp
from modules.writing import write_txt, write_raster, write_statistics
import time


if __name__ == "__main__":
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
    ) = _check_input_arguments()

    starttime1 = time.time()

    raster_path = "./data/raster/"

    print("Calculating {}...".format(index_name.upper()))
    if satellite in ["s2", "sentinel2", "sentinel"]:
        result, calc_resolution = index_calculator_s2(
            index_name, resolution, raster_path, clip_shape, optional_val
        )
    elif satellite in ["l8", "landsat8", "landsat"]:
        result = index_calculator_l8(index_name, raster_path, clip_shape, optional_val)
        calc_resolution = 30
    else:
        print(
            "ERROR: Your specified satellite dataset cannot be used yet or doesn't exist.\n Please provide a valid request, check the README for a list of possible datasets."
        )

    stoptime1 = time.time()

    # print out the information to user
    print(
        f"...finished calculating the {index_name.upper()} with a spatial resolution of {calc_resolution} m. \nCalculating took {stoptime1 - starttime1:.2f} seconds."
    )

    # plot the result/ndarray
    plot_result(index_name, result, calc_resolution, want_plot, want_plot_saved)

    starttime2 = time.time()

    if any([want_txt_saved == "true", want_raster_saved == "true", want_statistics == "true"]):
        print("\nAdditional outputs are generated...")

        # write txt file with results/ndarray
        write_txt(index_name, result, want_txt_saved)

        # export as raster tif-file
        write_raster(index_name, calc_resolution, raster_path, clip_shape, want_raster_saved, result)

        # generate statistics (histogram & descriptives)
        write_statistics(index_name, result, calc_resolution, want_statistics)

        print("...cleaning up...")
    else:
        print("\nCleaning up...")

    # delete any temporary files, works only if the program finished entirely
    cleanup_temp()

    stoptime2 = time.time()

    print(f"...finished. \nThis took another {stoptime2 - starttime2:.2f} seconds.")
