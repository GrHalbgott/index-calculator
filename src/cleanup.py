#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PCleans the project folder (empties results and deletes temp data)"""


import os


retain = ["raster", "shapes", "placeholder.md"]

print("Cleaning up...")

# deletes temp data
for item in os.listdir("./data/"):
    if item not in retain:
        os.remove("./data/" + item)

# empties results folder
for item in os.listdir("./results/"):
    if item not in retain:
        os.remove("./results/" + item)

print("...finished.")
