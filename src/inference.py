#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Modify by Kevin Yu. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

import jetson.inference
import jetson.utils

import requests
import argparse
import os

# parse the command line
# parser = argparse.ArgumentParser()
# parser.add_argument("filename", type=str,
#                     help="filename of the image to process")
# parser.add_argument("--network", type=str, default="googlenet",
#                     help="model to use, can be:  googlenet, resnet-18, ect.")
# opt = parser.parse_args()


def run_inference(url):

    # load an image (into shared CPU/GPU memory)
    response = requests.get(url)
    img_path = "./cache.jpg"
    file = open(img_path, "wb")
    file.write(response.content)
    file.close()
    img = jetson.utils.loadImage('./cache.jpg')

    # load the recognition network
    net = jetson.inference.imageNet('resnet-18')
    # net = jetson.inference.imageNet(opt.network)

    # classify the image
    class_idx, confidence = net.Classify(img)

    # find the object description
    class_desc = net.GetClassDesc(class_idx)

    # remove cache image file
    os.remove(img_path)

    # return the result as outputs
    return ("image is recognized as '{:s}' (class #{:d}) with {:f}% confidence".format(
        class_desc, class_idx, confidence * 100))
