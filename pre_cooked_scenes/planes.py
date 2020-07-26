from class_lib.color import *
from class_lib.coordinate_system import CoordinateSystem
from class_lib.imaging import Camera, Scene
from class_lib.light import *
from class_lib.solid_objects import *
from class_lib.solids.plane import SmoothPlane, CheckeredPlane
from class_lib.solids.sphere import SmoothSphere

HEIGHT = 500
WIDTH = 600

p1 = SmoothPlane(CoordinateSystem(origin=Vector(0, 0, 0), orientation=Vector(0, 1, 1)), Material(), width=9, length=10)
p2 = SmoothPlane(CoordinateSystem(origin=Vector(0, 0, 0), orientation=Vector(0, -1, 5)), Material())
p3 = CheckeredPlane(CoordinateSystem(origin=Vector(3, 0, 0.2), orientation=Vector(0, -1, 5)), cell_size=.5, width=2,
                    length=3)

lens = SmoothSphere(Vector(3 + .2 + .2, .2 + 1 - .2, 0.2 + .5 - .2 + .1), .3,
                    Material(diffuse_light_reflectivity=WHITE * 0.01,
                             specular_multiplier=.5, specular_coefficient=20, reflective_index=0, refractive_index=1.05,
                             refractive_attenuation=Color(0.01, 0.01, 0.01)
                             ))

objects = [p1, p2, p3, lens]

l1 = LightSourceAtInfinity(intensity=Color('#ffffff'), direction=Vector(2, 1, 3))
l2 = PointLightSource(intensity=Color('#ffff00'), intensity_booster=1, position=Vector(0, 0, 1))
l3 = PointLightSource(intensity=Color('#00ff00'), intensity_booster=2, position=Vector(4, -.5, 2))
illumination = Illumination(ambient_light=AmbientLight(intensity=WHITE * 0.3), light_sources=[l1, l2, l3])

camera_pos = Vector(8, 0, 1)

c = Camera(resolution=(HEIGHT, WIDTH), position=camera_pos, direction=-camera_pos, zoom=1, tilt_angle=0)

scene = Scene(c, objects, illumination)
