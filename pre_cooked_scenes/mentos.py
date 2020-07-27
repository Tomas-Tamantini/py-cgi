from random import choice

from class_lib.coordinate_system import CoordinateSystem
from class_lib.imaging import Camera, Scene
from class_lib.light import *
from class_lib.solid_objects import *
from class_lib.solids.ellipsoid import Ellipsoid
from class_lib.solids.plane import SmoothPlane

HEIGHT = 600
WIDTH = 600

lens_material = Material(diffuse_light_reflectivity=WHITE * 0.01,
                         specular_multiplier=.85, specular_coefficient=20, reflective_index=0, refractive_index=1.1,
                         refractive_attenuation=Color(0.03, 0.01, 0.01)
                         )

floor = SmoothPlane(CoordinateSystem(), Material(diffuse_light_reflectivity=WHITE * 0.3, reflective_index=.15))
candy_width = 0.5
num_candies = 6
candies = []
colors = [Color('#01aa4f'), Color('#9e1b3b'), Color('#f27024'), Color('#ee4131'), Color('#73328f'), Color('#fccc20'),
          Color('#ee4d90')]
previous_color = None
for i in range(num_candies):
    position = Vector((2 * i - num_candies + 1) * candy_width / 2, 0, .5)
    color = choice(colors)
    while color == previous_color:
        color = choice(colors)
    previous_color = color

    if i == num_candies - 3:
        material = lens_material
    else:
        material = Material(diffuse_light_reflectivity=color, specular_multiplier=0.5)

    new_candy = Ellipsoid(CoordinateSystem(origin=position), material, width=candy_width)
    candies.append(new_candy)

position = Vector((num_candies + 2) * candy_width / 2, 0, candy_width / 2)
color = choice(colors)
while color == previous_color:
    color = choice(colors)
material = Material(diffuse_light_reflectivity=color, specular_multiplier=0.5)
last_candy = Ellipsoid(CoordinateSystem(origin=position), material, height=candy_width)
candies.append(last_candy)

objects = [floor] + candies

l1 = LightSourceAtInfinity(intensity=Color('#ffffff'), direction=Vector(2, 3, 3))
l2 = PointLightSource(intensity=Color('#00ff00'), intensity_booster=2, position=Vector(0, 1, 2))
illumination = Illumination(ambient_light=AmbientLight(intensity=WHITE * 0.2), light_sources=[l1, l2])

camera_pos = Vector(5, 7, 2) * 0.85

c = Camera(resolution=(HEIGHT, WIDTH), position=camera_pos, direction=-camera_pos + Vector(0, 0, 1), zoom=1,
           tilt_angle=0)

scene = Scene(c, objects, illumination)
