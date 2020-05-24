"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""

from basics import Vector, Point
from class_lib.light import Ray
from class_lib.color import Color
from class_lib.imaging import Image, Camera

c = Camera(resolution=(3, 3), position=Vector(10, 0, 0), direction=Vector(-1, 0, 0), zoom=0.3535, tilt_angle=0)
for i in range(3):
    for j in range(3):
        print(c.get_ray(i, j))
