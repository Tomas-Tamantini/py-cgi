from abc import ABC, abstractmethod
from class_lib.color import *
from class_lib.coordinate_system import CoordinateSystem
from class_lib.solid_objects import AbstractObject, Material
from class_lib.useful_functions import min_pos_root
from math import atan2, degrees, pi, floor


class Sphere(AbstractObject, ABC):
    def __init__(self, coordinate_system, radius):
        super().__init__(coordinate_system)
        self.radius = radius

    def normal_at(self, rel_position):
        return rel_position.unit

    def easier_intersection(self, ray_p0, ray_dir):
        a = 1  # Because ray direction is unit. Otherwise, should be ray.direction.length_sq
        b = 2 * ray_dir * ray_p0
        c = ray_p0.length_sq - self.radius * self.radius
        return min_pos_root(a, b, c)

    @abstractmethod
    def material_at(self, rel_position):
        return NotImplementedError("Must be overridden")


class SmoothSphere(Sphere):
    """Sphere with the same material in its entire surface"""

    def __init__(self, position, radius, material):
        coordinate_system = CoordinateSystem(position)
        super().__init__(coordinate_system, radius)
        self.material = material

    def material_at(self, rel_position):
        return self.material


class BeachBall(Sphere):
    """Sphere with beach ball pattern"""

    def __init__(self, coordinate_system, radius):
        super().__init__(coordinate_system, radius)

    @staticmethod
    def __stripe(angle):
        colors = [Color(.8, 0, 0), Color(0, .8, 0), Color(0, 0, .8), Color(.8, .8, .8), Color(.8, 0, .8),
                  Color(0, .8, .8)]
        materials = []
        for i in range(6):
            materials.append(
                Material(diffuse_light_reflectivity=colors[i], specular_multiplier=.5, specular_coefficient=20))
        offset_angle = angle + pi / 2
        angle_degrees = degrees(offset_angle)
        angle_index = floor(angle_degrees / 60)
        return materials[angle_index]

    def material_at(self, rel_position):
        top_cap = Material(diffuse_light_reflectivity=Color(.8, .2, 0))
        bottom_cap = Material(diffuse_light_reflectivity=Color(0, .8, .2))
        if rel_position.z > 0.9 * self.radius:
            return top_cap
        elif rel_position.z < -0.9 * self.radius:
            return bottom_cap
        angle = atan2(rel_position.x, rel_position.y)
        return BeachBall.__stripe(angle)
