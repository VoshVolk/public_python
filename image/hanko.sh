#!/bin/zsh
time python transparent.py
cp -fv ./transparent_images/* ./images/
time python resize.py