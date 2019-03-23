# BrickBrain
Project I did with my son to learn machine learning for his science fair project.  Identifies various LEGO-type bricks.

This project consists of 3 scripts:

* takepic.py: takes images to use for classification; intended to be used with a USB web cam
* train.py: trains a resnet-50 model using turicreate and saves the model for use by predict.py
* predict.py: takes an image using webcam then infers image classification using the model created by train.py


Dependencies:

* pyqt [https://www.riverbankcomputing.com/software/pyqt/download5]

* turicreate [https://github.com/apple/turicreate]

* imagensnap (needed to take picture using web cam) [https://github.com/rharder/imagesnap]

* This only works on OS X

* You'll need a USB web cam.  I used this one: [https://smile.amazon.com/gp/product/B012CH5F58/ref=oh_aui_search_asin_title?ie=UTF8&psc=1]

License:

GPL v3 because that's what PyQt uses.  turicreate itself is licensed under a BSD-3 variant.

