from basics import Vector
from class_lib.solid_objects import AbstractObject
from class_lib.useful_functions import min_pos_root


class Ellipsoid(AbstractObject):

    def __init__(self, coordinate_system, material, width=1, length=1, height=1):
        super().__init__(coordinate_system)
        self.material = material
        self.width = width
        self.length = length
        self.height = height

    def material_at(self, rel_position):
        return self.material

    def easier_intersection(self, ray_p0, ray_dir):
        a = (ray_dir.x / self.width) ** 2 + (ray_dir.y / self.length) ** 2 + (ray_dir.z / self.height) ** 2
        b = 2 * ((ray_p0.x * ray_dir.x) / self.width ** 2 +
                 (ray_p0.y * ray_dir.y) / self.length ** 2 +
                 (ray_p0.z * ray_dir.z) / self.height ** 2)
        c = (ray_p0.x / self.width) ** 2 + (ray_p0.y / self.length) ** 2 + (ray_p0.z / self.height) ** 2 - 0.25
        return min_pos_root(a, b, c)

    def normal_at(self, rel_position):
        return Vector(rel_position.x / self.width ** 2,
                      rel_position.y / self.length ** 2,
                      rel_position.z / self.height ** 2).unit
