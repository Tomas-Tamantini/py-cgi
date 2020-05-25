"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""

from basics import Vector, Point
from class_lib.light import *
from class_lib.color import Color
from class_lib.imaging import Image, Camera, Scene
from class_lib.solid_objects import *

HEIGHT = 64
WIDTH = 40

s1 = Sphere(Vector(0, 0, 0), 2, Material(ambient_light_reflectivity=Color('#008081')))  # Teal
s2 = Sphere(Vector(0, 1, -2), 1, Material(ambient_light_reflectivity=Color(r=0.5, green=0.8, b=0.2)))

objects = [s1, s2]

illumination = Illumination(ambient_light=Color('#ffffff'))

c = Camera(resolution=(HEIGHT, WIDTH), position=Vector(10, 0, 0), direction=Vector(-1, 0, 0), zoom=1, tilt_angle=0)
s = Scene(c, objects, illumination)
im = s.render_image()

im.save_as_ppm('output/test.ppm')
print("Image saved.")
