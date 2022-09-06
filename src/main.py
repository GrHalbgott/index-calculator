#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculate indices"""


import utils
import sys
import matplotlib.pyplot as plt
from rasterio.plot import show as rshow
import time


def main():
    """
    Reads raster files as NumPy-arrays and calculate the desired index
    :return: raster image
    """

    starttime = time.time()

    raster_path = r"./data/raster/"
    if len(sys.argv) < 2:
        print(
            "Please use the required system arguments. Call the program with:\n $ python src/main.py [shape_input_file_name] [index_name {ndvi, ndmi, ndwi, reip}]"
        )
        sys.exit()
    elif len(sys.argv) < 3:
        index_name = sys.argv[1].lower()
    else:
        index_name = sys.argv[2].lower()

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
    if index_name == "ndvi":
        plt.imshow(result, cmap="RdYlGn")
        plt.clim(-0.2, 0.6)
    elif index_name == "ndmi":
        plt.imshow(result, cmap="jet_r")
        plt.clim(-0.2, 0.4)
    elif index_name == "ndwi":
        plt.imshow(result, cmap="seismic_r")
        plt.clim(-0.8, 0.8)
    else:
        plt.imshow(result)
    # Plot a colorbar with the same height as the plot
    im_ratio = result.shape[0] / result.shape[1]
    plt.colorbar(fraction=0.04625 * im_ratio)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
