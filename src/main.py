#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculate indices"""


import utils
import sys
import matplotlib.pyplot as plt
import time


def main():
    """
    Reads raster files as NumPy-arrays and calculate the desired index
    :return: raster image
    """

    starttime = time.time()

    raster_path = r"./data/raster/"
    if len(sys.argv) < 3:
        index_name = sys.argv[1]
    else:
        index_name = sys.argv[2]

    print("Calculating {}...".format(index_name))
    try:
        result = utils.calc_index(index_name, raster_path)
    except Exception as err:
        print(
            "...error occured when calculating the {}: {}.\n Please check your input files.".format(
                index_name, str(err)
            )
        )
        sys.exit()

    stoptime = time.time()

    # Print out the information to user
    print(
        "Finished calculating the {}. \n The script took {:.2f} seconds to run.".format(
            index_name.upper(), stoptime - starttime
        )
    )

    plt.figure()
    plt.title("Calculated {} of region of interest".format(index_name.upper()))
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    plt.imshow(result)
    # Plot a colorbar with the same height as the plot
    im_ratio = result.shape[0] / result.shape[1]
    plt.colorbar(fraction=0.04625 * im_ratio)
    plt.show()


if __name__ == "__main__":
    main()
