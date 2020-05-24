class Color:
    """Class for RGB colors"""

    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.__red = r
        self.__green = g
        self.__blue = b

    @staticmethod
    def __map_to_0_255(value):
        """Maps a float between 0 and 1 to an int between 0 and 255"""
        scaled_up_value = int(255 * value)
        if scaled_up_value > 255:
            return 255
        if scaled_up_value < 0:
            return 0
        return scaled_up_value

    def write_as_ppm(self):
        """Returns RGB value separated by spaces"""
        mapped_values = tuple(map(self.__map_to_0_255, (self.__red, self.__green, self.__blue)))
        return f'{mapped_values[0]} {mapped_values[1]} {mapped_values[2]}'

    def __add__(self, other):
        """Adds two colors together, component-wise"""
        return Color(self.__red + other.__red, self.__green + other.__green, self.__blue + other.__blue)

    def __mul__(self, other):
        """Multiplies color by given scalar component-wise"""
        return Color(self.__red * other, self.__green * other, self.__blue * other)

    def __rmul__(self, other):
        """Multiplies color by given scalar component-wise"""
        return self*other
    def __str__(self):
        return f'{{{self.__red}, {self.__green}, {self.__blue}}}'


class Ray:
    """Class for a light ray, starting from a given point, and going in given direction"""

    def __init__(self, initial_point, direction):
        """
        Initialize new light ray
        :param initial_point: Initial point
        :param direction: Direction
        """
        self.__initial_point = initial_point
        self.__direction = direction

    @property
    def initial_point(self):
        return self.__initial_point

    @property
    def direction(self):
        return self.__direction

    def __str__(self):
        return f'Ray starting at {self.initial_point} with direction {self.direction}'
