from class_lib.color import *
from class_lib.coordinate_system import CoordinateSystem
from class_lib.imaging import Camera, Scene
from class_lib.light import *
from class_lib.solid_objects import *
from class_lib.solids.plane import SmoothPlane, CheckeredPlane
from class_lib.solids.ellipsoid import Ellipsoid
from class_lib.solids.sphere import SmoothSphere

HEIGHT = 500
WIDTH = 600

floor = CheckeredPlane(CoordinateSystem(), cell_size=1)
e1 = Ellipsoid(CoordinateSystem(origin=Vector(0, 0, 1), orientation=Vector(0, 1, 1), angle=-0.5),
               Material(diffuse_light_reflectivity=Color('#ed8e4a'), specular_multiplier=0.85), width=.3,
               length=1, height=2)

e2 = Ellipsoid(CoordinateSystem(origin=Vector(1, -1, 0.25)), Material(specular_multiplier=0.95), height=.5)
lens_material = Material(diffuse_light_reflectivity=WHITE * 0.01,
                         specular_multiplier=.85, specular_coefficient=20, reflective_index=0, refractive_index=1.1,
                         refractive_attenuation=Color(0.03, 0.01, 0.01)
                         )
lens1 = Ellipsoid(CoordinateSystem(origin=Vector(1, 0, .5)), lens_material, width=0.2)
lens2 = Ellipsoid(CoordinateSystem(origin=Vector(0, 1, 1), angle=0.5), lens_material, height=2, width=0.2)

objects = [floor, e1, e2, lens1, lens2]

l1 = LightSourceAtInfinity(intensity=Color('#ffffff'), direction=Vector(2, -1, 3))
l2 = PointLightSource(intensity=Color('#ffff00'), intensity_booster=1, position=Vector(0, -1, 1.1))
illumination = Illumination(ambient_light=AmbientLight(intensity=WHITE * 0.2), light_sources=[l1, l2])

camera_pos = Vector(5, 0, 1)

c = Camera(resolution=(HEIGHT, WIDTH), position=camera_pos, direction=-camera_pos + Vector(0, 0, 1), zoom=1,
           tilt_angle=0)

scene = Scene(c, objects, illumination)
