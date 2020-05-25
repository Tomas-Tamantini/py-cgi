from class_lib.color import Color


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

    def __init__(self, intensity):
        """
        Initialize light source with given intensity
        :param intensity: Color indicating how intense the light is in the RGB colors
        """
        self.__intensity = intensity

    @property
    def intensity(self):
        return self.__intensity


class AmbientLight(LightSource):
    """Class for ambient light (doesn't produce shades and is constant everywhere. An alias for its superclass"""
    pass


class PointLightSource(LightSource):
    """Light source at a specific point in space, emitting light in all directions"""

    def __init__(self, intensity, position):
        """
        Initialize new point light source
        :param intensity: Color indicating how intense the light is in the RGB colors
        :param position: Light source position
        """
        super().__init__(intensity)
        self.__position = position

    @property
    def position(self):
        return self.__position


class LightSourceAtInfinity(LightSource):
    """Light coming from infinity in parallel rays (for example, the sun)"""

    def __init__(self, intensity, direction):
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


class Illumination:
    """Class for storing light sources"""
    def __init__(self, ambient_light=Color('#555555'), point_light_sources=None, light_sources_at_infinity=None):
        self.ambient_light = ambient_light
        self.point_light_sources = point_light_sources if point_light_sources else []
        self.light_sources_at_infinity = light_sources_at_infinity if light_sources_at_infinity else []
