from random import choice

from class_lib.color import *
from class_lib.coordinate_system import CoordinateSystem
from class_lib.imaging import Camera, Scene
from class_lib.light import *
from class_lib.solid_objects import *
from class_lib.solids.plane import SmoothPlane, CheckeredPlane
from class_lib.solids.ellipsoid import Ellipsoid
from class_lib.solids.paraboloid import Paraboloid
from class_lib.solids.sphere import SmoothSphere

# res = 30 for 1080 x 1920
res = 30
p_aux = .4

HEIGHT = round(64 * res)
WIDTH = round(36 * res)

colors = [Color('#01aa4f'), Color('#9e1b3b'), Color('#f27024'), Color('#ee4131'), Color('#73328f'), Color('#fccc20'),
          Color('#ee4d90')]

lens_material = Material(diffuse_light_reflectivity=WHITE * 0.01,
                         specular_multiplier=.85, specular_coefficient=20, reflective_index=0, refractive_index=1.02,
                         refractive_attenuation=Color(0.03, 0.01, 0.01)
                         )

back_wall_1 = Paraboloid(CoordinateSystem(origin=Vector(-10, 0, 0), orientation=Vector(1, 0, 0)),
                         Material(diffuse_light_reflectivity=WHITE * 0.3), a=0.02, b=0.01, z_max=2)
back_wall_2 = SmoothPlane(CoordinateSystem(origin=Vector(-9.15, 0, -5), orientation=Vector(1, 0, 0), angle=0.6),
                          Material(diffuse_light_reflectivity=WHITE * 0.6), width=30,
                          length=5)
back_wall_3 = SmoothPlane(CoordinateSystem(origin=Vector(-9, 0, -6), orientation=Vector(1, 0, 0), angle=0.5),
                          Material(diffuse_light_reflectivity=WHITE * 0.4), width=30,
                          length=5)
background = [back_wall_1, back_wall_2, back_wall_3]
p1 = Paraboloid(CoordinateSystem(origin=Vector(0, 0, 2)),
                Material(diffuse_light_reflectivity=WHITE * 0.4, specular_multiplier=0.3), a=p_aux, b=p_aux)

p2 = Paraboloid(CoordinateSystem(origin=Vector(0, 0, -2), orientation=Vector(0, 0, -1)),
                Material(diffuse_light_reflectivity=WHITE * 0.4, specular_multiplier=0.3), a=p_aux, b=p_aux)

color1 = colors[0]
color2 = colors[2]
color3 = colors[6]

e1 = Ellipsoid(CoordinateSystem(), Material(diffuse_light_reflectivity=color1, specular_multiplier=0.5),
               width=2,
               length=2, height=1)

s1 = SmoothSphere(Vector(0, 0, 1.25), .35, Material(diffuse_light_reflectivity=color2, specular_multiplier=0.5))

s2 = SmoothSphere(Vector(0, 0, -1.25), .35, Material(diffuse_light_reflectivity=color3, specular_multiplier=0.5))

lens1 = Ellipsoid(CoordinateSystem(origin=Vector(-2, 1.4, -1.3)), lens_material, width=0.2)

lens2 = SmoothSphere(Vector(2, 0.8, -0.4), .4,
                     Material(diffuse_light_reflectivity=WHITE * 0.01,
                              specular_multiplier=.5, specular_coefficient=20, reflective_index=0,
                              refractive_index=1.15,
                              refractive_attenuation=Color(0.03, 0.01, 0.01)
                              ))

# objects = [back_wall_1, p1, p2, e1, s1, s2]
objects = background + [p1, p2, e1, s1, s2, lens2]

l1 = LightSourceAtInfinity(intensity=Color('#ffffff') * 0.6, direction=Vector(2, 4, 2))
l2 = PointLightSource(intensity=Color('#ffffff'), intensity_booster=8, position=Vector(-5, 4, -2))
l3 = PointLightSource(intensity=WHITE, intensity_booster=4, position=Vector(3, -1, 0))
illumination = Illumination(ambient_light=AmbientLight(intensity=WHITE * 0.2), light_sources=[l1, l2, l3])

camera_pos = Vector(10, 0, 0)

c = Camera(resolution=(HEIGHT, WIDTH), position=camera_pos, direction=-camera_pos, zoom=1,
           tilt_angle=0)

scene = Scene(c, objects, illumination)
