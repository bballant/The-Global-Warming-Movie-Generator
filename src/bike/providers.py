# gwmg.bike.providers.py

from settings import *
from gwmg import base

RESOURCES_ROOT = APPLICATION_ROOT + "bike_sources/"

# pure masks
black_mask      = base.ColorProvider(SIZE, "Black", "L")
white_mask      = base.ColorProvider(SIZE, "White", "L")
# colors
yellow          = base.ColorProvider(SIZE, "Yellow")
black           = base.ColorProvider(SIZE, "Black")
white           = base.ColorProvider(SIZE, "White")
red             = base.ColorProvider(SIZE, "Red")
pink            = base.ColorProvider(SIZE, "Pink")
# frames
bike            = base.FrameProvider(SIZE, RESOURCES_ROOT + "bike_frames/bike1_%04d.png")
behbike         = base.FrameProvider(SIZE, RESOURCES_ROOT + "behbike_frames/behbike%04d.png")
tree            = base.FrameProvider(SIZE, RESOURCES_ROOT + "treemask/treemaskin %04d.jpg")
fountain        = base.FrameProvider(SIZE, RESOURCES_ROOT + "fountain_frames/fountain%04d.png")
#images
sun             = base.ImageProvider(SIZE, RESOURCES_ROOT + "images/sun.png")
scene           = base.ImageProvider(SIZE, RESOURCES_ROOT + "images/scene.JPG")
credits         = base.ImageProvider(SIZE, RESOURCES_ROOT + "images/credits.png")
# image masks
title           = base.MaskImageProvider(SIZE, RESOURCES_ROOT + "images/title.png", True)
# frame masks
tree_mask       = base.MaskProvider(SIZE, RESOURCES_ROOT + "treemask/treemaskin %04d.jpg", True)
behbike_mask    = base.MaskProvider(SIZE, RESOURCES_ROOT + "behbike_frames/behbike%04d.png", True, "L")
fountain_mask   = base.MaskProvider(SIZE, RESOURCES_ROOT + "fountain_frames/fountain%04d.png", True)
auto_mask       = base.MaskProvider(SIZE, RESOURCES_ROOT + "automotion/automotionin %04d.jpg", True, "1")
bike_mask_o     = base.MaskProvider(SIZE, RESOURCES_ROOT + "bike_frames/bike1_%04d.png", True, "L")
