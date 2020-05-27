"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""

from basics import Vector, Point
from class_lib.light import *
from class_lib.color import *
from class_lib.imaging import Image, Camera, Scene
from class_lib.solid_objects import *

HEIGHT = 500
WIDTH = 600

s1 = Sphere(Vector(0, 0, 1), 2,
            Material(diffuse_light_reflectivity=METAL,
                     specular_multiplier=0.5, specular_coefficient=20, reflective_index=.3
                     ))
s2 = Sphere(Vector(1, 1, -1), .5, Material(diffuse_light_reflectivity=TEAL,
                                           specular_multiplier=.5, specular_coefficient=20))

s3 = Sphere(Vector(0, 0, -2), .8, Material(diffuse_light_reflectivity=GRAPE,
                                           specular_multiplier=.5, specular_coefficient=20, reflective_index=.5))
s4 = Sphere(Vector(3.5, .5, -1), .4,
            Material(diffuse_light_reflectivity=WHITE * 0.01,
                     specular_multiplier=.5, specular_coefficient=20, reflective_index=0, refractive_index=1.05,
                     refractive_attenuation=Color(0.01, 0.01, 0.01)
                     ))

objects = [s1, s2, s3, s4]

l1 = LightSourceAtInfinity(intensity=Color('#ffffff'), direction=Vector(2, 1, 3))
l2 = LightSourceAtInfinity(intensity=Color('#002255'), direction=Vector(0, -1, 0))
l3 = PointLightSource(intensity=Color('#ffff00'), intensity_booster=4, position=Vector(2, 2, -2))
illumination = Illumination(ambient_light=AmbientLight(intensity=WHITE * 0.3), light_sources=[l1, l2, l3])

c = Camera(resolution=(HEIGHT, WIDTH), position=Vector(10, 0, 0), direction=Vector(-1, 0, 0), zoom=1, tilt_angle=0)
s = Scene(c, objects, illumination)
im = s.render_image()

im.save_as_ppm('output/test.ppm')
print("Image saved.")
