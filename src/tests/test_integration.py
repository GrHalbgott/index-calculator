#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Integration tests"""


import subprocess


def test_run_main():
    """Tests whether main runs correctly and catches errors"""
    subprocess.check_call(["python", "src/main.py", "-c rouse.shp", "-i ndxx"])
