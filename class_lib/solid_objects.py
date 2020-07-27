from abc import ABC, abstractmethod

from class_lib.color import *
from math import log, exp


class Material:
    """Material optical specifications"""

    def __init__(self, ambient_light_reflectivity=None, diffuse_light_reflectivity=GRAPE, specular_multiplier=.0,
                 specular_coefficient=20, reflective_index=.0, refractive_index=1.0,
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


class AbstractObject(ABC):
    """Abstract object with position and orientation"""

    def __init__(self, coordinate_system):
        self.coordinate_system = coordinate_system

    def intersection_distance(self, ray):
        new_ray_init_point = self.coordinate_system.convert_position(ray.initial_point)
        new_ray_direction = self.coordinate_system.convert_direction(ray.direction)
        return self.easier_intersection(new_ray_init_point, new_ray_direction)

    def chip_at(self, position):
        relative_position = self.coordinate_system.convert_position(position)
        normal = self.normal_at(relative_position)
        fixed_normal = self.coordinate_system.deconvert_direction(normal)
        material = self.material_at(relative_position)
        return Chip(position, fixed_normal, material)

    @abstractmethod
    def normal_at(self, rel_position):
        raise NotImplementedError("Must be overridden")

    @abstractmethod
    def material_at(self, rel_position):
        raise NotImplementedError("Must be overridden")

    @abstractmethod
    def easier_intersection(self, ray_p0, ray_dir):
        raise NotImplementedError("Must be overridden")