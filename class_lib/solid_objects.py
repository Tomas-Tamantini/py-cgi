from class_lib.color import GRAPE
from class_lib.useful_functions import min_pos_root


class Material:
    """Material optical specifications"""

    def __init__(self, ambient_light_reflectivity=None, diffuse_light_reflectivity=GRAPE, specular_multiplier=.5,
                 specular_coefficient=20):
        """
        Initialize new material
        :param ambient_light_reflectivity: Color indicating the percentage of light the material reflects from ambient light in RGB
        :param diffuse_light_reflectivity: Color indicating the percentage of light the material reflects by diffusion in RGB
        :param specular_multiplier: Percentage of light received which is reflected by specular reflection
        :param specular_coefficient: Power to which the cosine between R and H is raised in the Blinn-Phong reflection model
        """
        self.ambient_light_reflectivity = ambient_light_reflectivity if ambient_light_reflectivity else diffuse_light_reflectivity
        self.diffuse_light_reflectivity = diffuse_light_reflectivity
        self.specular_multiplier = specular_multiplier
        self.specular_coefficient = specular_coefficient


class Chip:
    """A small chip of material, with a position and a normal vector"""

    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal
        self.material = material


class Sphere:
    def __init__(self, position, radius, material):
        """Initialize new sphere"""
        self.__position = position
        self.__radius = radius
        self.__material = material

    def chip_at(self, position):
        return Chip(position, self.__normal(position), self.__material)

    def __normal(self, position):
        return (position - self.__position).unit

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
