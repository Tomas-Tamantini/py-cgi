from class_lib.useful_functions import min_pos_root


class Sphere:
    def __init__(self, position, radius, material):
        """Initialize new sphere"""
        self.__position = position
        self.__radius = radius
        self.__material = material

    @property
    def material(self):
        return self.__material

    def intersection_distance(self, ray):
        """
        If ray doesn't intersect sphere, returns None.
        If it does, returns time when ray intersects sphere
        """
        dist = ray.initial_point - self.__position
        a = 1  # Because ray direction is unit. Otherwise, should be ray.direction.length_sq
        b = 2 * ray.direction * dist
        c = dist.length_sq - self.__radius * self.__radius
        return min_pos_root(a, b, c)
