#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculate indices"""


# Call with:
# $ python src/main.py [raster_input_file] [shape_input_file] [index_name {ndmi, ndvi, reip, rgb}]


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

    in_raster = "./data/" + sys.argv[1]
    if len(sys.argv) < 4:
        index_name = sys.argv[2]
    else:
        in_shape = "./data/shapes/" + sys.argv[2]
        index_name = sys.argv[3]

    if len(sys.argv) == 4:
        print("Cutting raster...")
        try:
            cut_raster = utils.cut(in_raster, in_shape)
        except Exception as err:
            print("...error occured when cutting the raster file: {}".format(str(err)))
            sys.exit()
    else:
        cut_raster = in_raster

    print("Calculating {}...".format(index_name))
    try:
        result = utils.calc_index(index_name, cut_raster)
    except Exception as err:
        print(
            "...error occured when calculating the {}: {}".format(index_name, str(err))
        )
        sys.exit()

    stoptime = time.time()

    # Print out the information to user
    print(
        "Finished calculating the {} of the raster {}. \n The script took {:.2f} seconds to run.".format(
            index_name, in_raster, stoptime - starttime
        )
    )

    plt.figure(figsize=(20, 20))
    plt.title("{} of chosen input raster file".format(index_name))
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    if index_name in {"RGB", "rgb", 4}:
        plt.imshow(result)
    else:
        plt.imshow(result, cmap="viridis")
        # Plot a colorbar with the same height as the plot
        im_ratio = result.shape[0] / result.shape[1]
        plt.colorbar(fraction=0.04625 * im_ratio)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
