from abc import ABC, abstractmethod
from math import floor
from basics import Vector
from class_lib.color import *
from class_lib.solid_objects import AbstractObject, Material
from globals import MIN_DIST


class AbstractPlane(AbstractObject, ABC):
    def __init__(self, coordinate_system, width, length):
        super().__init__(coordinate_system)
        self.width = width
        self.length = length

    def normal_at(self, rel_position):
        return Vector(0, 0, 1)

    def easier_intersection(self, ray_p0, ray_dir):
        if ray_dir.z == 0:
            return None
        t = - ray_p0.z / ray_dir.z
        if t <= MIN_DIST:
            return None
        if self.width:
            x = ray_p0.x + ray_dir.x * t
            if x < -self.width / 2 or x > self.width / 2:
                return None
        if self.length:
            y = ray_p0.y + ray_dir.y * t
            if y < -self.length / 2 or y > self.length / 2:
                return None
        return t

    @abstractmethod
    def material_at(self, rel_position):
        return NotImplementedError("Must be overridden")


class SmoothPlane(AbstractPlane):

    def __init__(self, coordinate_system, material, width=None, length=None):
        AbstractPlane.__init__(self, coordinate_system, width, length)
        self.material = material

    def material_at(self, rel_position):
        return self.material


class CheckeredPlane(AbstractPlane):
    def __init__(self, coordinate_system, cell_size=1, width=None, length=None):
        super().__init__(coordinate_system, width, length)
        self.cell_size = cell_size

    def material_at(self, rel_position):
        aux_x = floor(rel_position.x / self.cell_size)
        aux_y = floor(rel_position.y / self.cell_size)
        if (aux_x + aux_y) % 2 == 0:
            return Material(diffuse_light_reflectivity=Color(.8, .8, .8))
        return Material(diffuse_light_reflectivity=Color(.1, .1, .1))
