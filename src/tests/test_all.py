#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Integration tests"""


import utils
import indices_s2
import reading
import writing


def test_resolution_handler():
    """Tests if the resolution handler works fine"""

    calc_resolution_ndmi = utils.resolution_handler("ndmi", "")
    calc_resolution_ndvi = utils.resolution_handler("ndvi", "")    
    test_resolution_ndmi = 20
    test_resolution_ndvi = 10

    assert int(calc_resolution_ndmi) == test_resolution_ndmi
    assert int(calc_resolution_ndvi) == test_resolution_ndvi
