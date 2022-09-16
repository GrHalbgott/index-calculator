#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions to write data (raster/txt/plots)"""


import matplotlib.pyplot as plt
import numpy as np


def write_txt(index_name, want_txt_saved, result):
    """Checks if the user wants to locally save the results as txt-file as well"""
    while want_txt_saved not in ["true", "false"]:
        want_txt_saved = input("Do you want to save the results/ndarray as txt-file as well? Use y/n: ")
        if want_txt_saved in ["y", "yes"] or want_txt_saved in ["n", "no"]:
            break
        print("Please provide a valid input.")
    if want_txt_saved in ["y", "yes", "true"]:
        np.savetxt("./data/{}.txt".format(index_name), result)
    else:
        pass


def save_plot(index_name, calc_resolution, want_plot_saved):
    """Checks if the user wants to locally save the figure as well"""
    while want_plot_saved not in ["true", "false"]:
        want_plot_saved = input("Do you want to save the plot as figure? Use y/n: ")
        if want_plot_saved in ["y", "yes"] or want_plot_saved in ["n", "no"]:
            break
        print("Please provide a valid input.")
    if want_plot_saved in ["y", "yes", "true"]:
        plt.savefig("./{}_{}.png".format(index_name.lower(), calc_resolution), bbox_inches="tight")
    else:
        pass
