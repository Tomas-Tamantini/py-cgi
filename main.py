"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""

from basics import Vector, Point
from class_lib.light import *
from class_lib.color import Color
from class_lib.imaging import Image, Camera, Scene
from class_lib.solid_objects import *

HEIGHT = 250
WIDTH = 300

s1 = Sphere(Vector(0, 0, 1), 2,
            Material(ambient_light_reflectivity=Color('#008081'), diffuse_light_reflectivity=Color('#008081'),
                     specular_multiplier=0.5, specular_coefficient=20))  # Teal
s2 = Sphere(Vector(0, 0, -1), 1, Material(ambient_light_reflectivity=Color(r=0.5, green=0.8, b=0.2),
                                          diffuse_light_reflectivity=Color(r=0.5, green=0.8, b=0.2),
                                          specular_multiplier=-.2, specular_coefficient=2))

objects = [s1, s2]

illumination = Illumination(ambient_light=AmbientLight(intensity=Color('#444444')),
                            light_sources_at_infinity=[
                                LightSourceAtInfinity(intensity=Color('#ffffff'), direction=Vector(2, 1, 3))])

c = Camera(resolution=(HEIGHT, WIDTH), position=Vector(10, 0, 0), direction=Vector(-1, 0, 0), zoom=1, tilt_angle=0)
s = Scene(c, objects, illumination)
im = s.render_image()

im.save_as_ppm('output/test.ppm')
print("Image saved.")
