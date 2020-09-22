from basics import Vector
from class_lib.solid_objects import AbstractObject
from class_lib.useful_functions import min_pos_root, all_pos_roots


class Paraboloid(AbstractObject):

    def __init__(self, coordinate_system, material, a=1, b=1, z_max=None):
        super().__init__(coordinate_system)
        self.material = material
        self.a = a
        self.b = b
        self.z_max = z_max

    def material_at(self, rel_position):
        return self.material

    def easier_intersection(self, ray_p0, ray_dir):
        aux_a = self.a * ray_dir.x ** 2 + self.b * ray_dir.y ** 2
        aux_b = 2 * (self.a * (ray_p0.x * ray_dir.x) +
                     self.b * (ray_p0.y * ray_dir.y)) - ray_dir.z
        aux_c = self.a * ray_p0.x ** 2 + self.b * ray_p0.y ** 2 - ray_p0.z
        intersections = all_pos_roots(aux_a, aux_b, aux_c)
        if not intersections or len(intersections) == 0:
            return None
        if not self.z_max:
            return min(intersections)
        for time in intersections:
            z = ray_p0.z + time * ray_dir.z
            if self.z_max >= z >= -self.z_max:
                return time
        return None

    def normal_at(self, rel_position):
        return Vector(self.a * rel_position.x,
                      self.b * rel_position.y,
                      -.5).unit
