from class_lib.color import GRAPE, Color
from class_lib.useful_functions import min_pos_root
from math import log, exp


class Material:
    """Material optical specifications"""

    def __init__(self, ambient_light_reflectivity=None, diffuse_light_reflectivity=GRAPE, specular_multiplier=0,
                 specular_coefficient=20, reflective_index=0, refractive_index=1,
                 refractive_attenuation=Color(1, 1, 1)):
        """
        Initialize new material
        :param ambient_light_reflectivity: Color indicating the percentage of light the material reflects from ambient light in RGB
        :param diffuse_light_reflectivity: Color indicating the percentage of light the material reflects by diffusion in RGB
        :param specular_multiplier: Percentage of light received which is reflected by specular reflection
        :param specular_coefficient: Power to which the cosine between R and H is raised in the Blinn-Phong reflection model
        :param reflective_index: Percentage of light which is reflected by surface like a mirror
        :param refractive_index: Refractive index of material
        :param refractive_attenuation: How much light is attenuated per meter traveled inside the material in RGB
        """
        self.ambient_light_reflectivity = ambient_light_reflectivity if ambient_light_reflectivity else diffuse_light_reflectivity
        self.diffuse_light_reflectivity = diffuse_light_reflectivity
        self.specular_multiplier = specular_multiplier
        self.specular_coefficient = specular_coefficient
        self.reflective_index = reflective_index
        self.refractive_index = refractive_index
        self.__refractive_attenuation = refractive_attenuation
        self.__refractive_attenuation_consts = Color(Material.__exp_constant(self.__refractive_attenuation.red),
                                                     Material.__exp_constant(self.__refractive_attenuation.green),
                                                     Material.__exp_constant(self.__refractive_attenuation.blue))

    @property
    def is_refractive(self):
        """True if material lets light through it"""
        return self.__refractive_attenuation.red < 1 or \
               self.__refractive_attenuation.green < 1 or \
               self.__refractive_attenuation.blue < 1

    def attenuate_by_refraction(self, original_color, distance_travelled):
        new_red = original_color.red * exp(self.__refractive_attenuation_consts.red * distance_travelled)
        new_green = original_color.green * exp(self.__refractive_attenuation_consts.green * distance_travelled)
        new_blue = original_color.blue * exp(self.__refractive_attenuation_consts.blue * distance_travelled)
        return Color(new_red, new_green, new_blue)

    @staticmethod
    def __exp_constant(p):
        """Exponent decay constant"""
        if p < 1:
            return log(1 - p)
        return -1000


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
