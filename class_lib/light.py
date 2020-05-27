from math import inf

from basics import Vector

from class_lib.color import WHITE
from class_lib.useful_functions import attenuate_by_distance_sq


class Ray:
    """Class for a light ray, starting from a given point, and going in given direction"""

    def __init__(self, initial_point, direction):
        """
        Initialize new light ray
        :param initial_point: Initial point
        :param direction: Direction (is always converted to unit vector)
        """
        self.__initial_point = initial_point
        self.__direction = direction.unit

    def position_at_time(self, time):
        """Ray position at given time"""
        return self.initial_point + time * self.direction

    @property
    def initial_point(self):
        return self.__initial_point

    @property
    def direction(self):
        return self.__direction

    def __str__(self):
        return f'Ray starting at {self.initial_point} with direction {self.direction}'


class LightSource:
    """A source which emits light with given intensity"""

    def __init__(self, intensity=WHITE):
        """
        Initialize light source with given intensity
        :param intensity: Color indicating how intense the light is in the RGB colors
        """
        self.__intensity = intensity

    @property
    def intensity(self):
        return self.__intensity

    def attenuator_by_distance_sq(self, chip_position):
        return 1


class AmbientLight(LightSource):
    """Class for ambient light (doesn't produce shades and is constant everywhere. An alias for its superclass"""
    pass


class PointLightSource(LightSource):
    """Light source at a specific point in space, emitting light in all directions"""

    def __init__(self, intensity=WHITE, intensity_booster=5, position=Vector(0, 0, 10)):
        """
        Initialize new point light source
        :param intensity: Color indicating how intense the light is in the RGB colors
        :param intensity_booster: Light decays with the square of the distance, booster helps it not be so faint
        :param position: Light source position
        """
        super().__init__(intensity)
        self.__position = position
        self.__intensity_booster = intensity_booster

    @property
    def position(self):
        return self.__position

    def ray_to_light_source(self, chip_position):
        direction = self.position - chip_position
        return Ray(chip_position, direction)

    def distance_to_point(self, point_position):
        return (self.position - point_position).length

    def attenuator_by_distance_sq(self, chip_position):
        distance_sq = (self.position - chip_position).length_sq
        return self.__intensity_booster * attenuate_by_distance_sq(distance_sq)


class LightSourceAtInfinity(LightSource):
    """Light coming from infinity in parallel rays (for example, the sun)"""

    def __init__(self, intensity=WHITE, direction=Vector(0, 0, 1)):
        """
        Initialize new light source at infinity
        :param intensity: Color indicating how intense the light is in the RGB colors
        :param direction: Direction from which the light rays come
        """
        super().__init__(intensity)
        self.__direction = direction

    @property
    def direction(self):
        return self.__direction

    def ray_to_light_source(self, chip_position):
        return Ray(chip_position, self.direction)

    def distance_to_point(self, point_position):
        return inf


class Illumination:
    """Class for storing light sources"""

    def __init__(self, ambient_light=WHITE * 0.25, light_sources=None):
        """
        Initializes new illumination
        :param ambient_light: Ambient light of the scene
        :param light_sources: Punctual light sources and light sources at infinity
        """
        self.ambient_light = ambient_light
        self.light_sources = light_sources if light_sources else []
