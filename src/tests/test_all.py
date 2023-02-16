#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing the functions"""


from modules.utils import resolution_handler


def test_resolution_handler():
    """Tests if the resolution handler works fine"""

    calc_resolution_ndmi = resolution_handler("ndmi", "")
    calc_resolution_ndvi = resolution_handler("ndvi", "")
    test_resolution_ndmi = 20
    test_resolution_ndvi = 10

    assert int(calc_resolution_ndmi) == test_resolution_ndmi
    assert int(calc_resolution_ndvi) == test_resolution_ndvi
