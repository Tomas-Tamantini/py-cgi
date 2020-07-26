"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""
from class_lib.color import *
from class_lib.imaging import Camera, Scene
from class_lib.light import *
from class_lib.solid_objects import *
from math import pi, sqrt, sin, cos

from pre_cooked_scenes.original_spheres import scene

im = scene.render_image()
im.save_as_png('output/test.png')
print("Image saved.")
