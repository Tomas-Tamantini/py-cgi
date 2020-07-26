from math import cos, sin

from basics import Vector


class CoordinateSystem:
    def __init__(self, origin=Vector(0, 0, 0), orientation=Vector(0, 0, 1), angle=0):
        self.origin = origin
        self.k_prime, self.i_prime, self.j_prime = CoordinateSystem.unit_base_axis(orientation, angle)

    @staticmethod
    def unit_base_axis(i_prime, tilt):
        """Returns a coordinate system (i', j' and k') given i'"""
        new_i = i_prime.unit
        if new_i == Vector(0, 0, 1) or new_i == Vector(0, 0, -1):
            aux_j = Vector(1, 0, 0)
        else:
            aux_j = Vector(-new_i.y, new_i.x, 0).unit
        aux_k = new_i ** aux_j  # Vector product
        aux_cos = cos(tilt)
        aux_sin = sin(tilt)
        new_j = aux_j * aux_cos + aux_k * aux_sin
        new_k = aux_k * aux_cos - aux_j * aux_sin
        return new_i, new_j, new_k

    def convert_position(self, position):
        dif = position - self.origin
        return self.convert_direction(dif)

    def deconvert_position(self, position):
        return self.origin + self.deconvert_direction(position)

    def convert_direction(self, direction):
        px = direction * self.i_prime
        py = direction * self.j_prime
        pz = direction * self.k_prime
        return Vector(px, py, pz)

    def deconvert_direction(self, direction):
        return self.i_prime * direction.x + self.j_prime * direction.y + self.k_prime * direction.z
