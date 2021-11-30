#!/bin/zsh
time python transparent.py images transparent_images -v
#cp -fv ./transparent_images/* ./images/
time python resize.py transparent_images resize_images -vf LANCZOS -s 300