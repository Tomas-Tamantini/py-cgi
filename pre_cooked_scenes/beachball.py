from class_lib.coordinate_system import CoordinateSystem
from class_lib.imaging import Camera, Scene
from class_lib.light import *
from class_lib.solid_objects import *
from class_lib.solids.sphere import SmoothSphere, BeachBall

HEIGHT = 500
WIDTH = 600

ball_radius = 2
s1 = SmoothSphere(Vector(0, 0, 0), ball_radius,
                  Material(diffuse_light_reflectivity=METAL,
                           specular_multiplier=0.5, specular_coefficient=20, reflective_index=.3
                           ))
s1 = BeachBall(coordinate_system=CoordinateSystem(orientation=Vector(80, -35, 18), angle=-0.6), radius=2)

lens_pos = Vector(25, -21, 13)
lens_radius = .4
lens_pos = (ball_radius + lens_radius) * lens_pos.unit

s4 = SmoothSphere(lens_pos, lens_radius,
                  Material(diffuse_light_reflectivity=WHITE * 0.01,
                           specular_multiplier=.5, specular_coefficient=20, reflective_index=0, refractive_index=1.05,
                           refractive_attenuation=Color(0.01, 0.01, 0.01)
                           ))
objects = [s1, s4]

l1 = LightSourceAtInfinity(intensity=Color('#ffffff'), direction=Vector(2, 1, 3))
l2 = LightSourceAtInfinity(intensity=Color('#002255'), direction=Vector(0, -1, 0))
# l3 = PointLightSource(intensity=Color('#ffff00'), intensity_booster=4, position=Vector(2, 2, -2))
illumination = Illumination(ambient_light=AmbientLight(intensity=WHITE * 0.3), light_sources=[l1, l2])

c = Camera(resolution=(HEIGHT, WIDTH), position=Vector(8, 0, 0), direction=Vector(-1, 0, 0), zoom=1, tilt_angle=0)

scene = Scene(c, objects, illumination)
