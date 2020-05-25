class Color:
    """Class for RGB colors"""

    def __init__(self, *args, **kwargs):
        """
        Initialize new color
        Acceptable args:
            String with hex representation (ex. hex = #1234ab)
            Named parameters (ex. r = 0.2, green = 0.44, blue = 0.12)
        Acceptable keywords:
            r, g, b, red, green, blue
        """
        if len(kwargs) > 0:
            if len(args) > 0:
                raise Exception("Cannot have kwargs and args at the same time, choose one or the other")

            if 'r' in kwargs:
                self.__red = kwargs.get('r')
            elif 'red' in kwargs:
                self.__red = kwargs.get('red')

            if 'g' in kwargs:
                self.__green = kwargs.get('g')
            elif 'green' in kwargs:
                self.__green = kwargs.get('green')

            if 'b' in kwargs:
                self.__blue = kwargs.get('b')
            elif 'blue' in kwargs:
                self.__blue = kwargs.get('blue')
        elif len(args) > 0:
            if len(args) == 1:
                hex_value = args[0]

                if isinstance(hex_value, str):
                    # Color like '#12a5bf'
                    self.__red = int(hex_value[1:3], 16) / 255.0
                    self.__green = int(hex_value[3:5], 16) / 255.0
                    self.__blue = int(hex_value[5:7], 16) / 255.0
                else:
                    raise Exception('Color must be given by string, or r,g,b separately')
            else:
                self.__red, self.__green, self.__blue = tuple(args)
        else:
            self.__red, self.__green, self.__blue = 0, 0, 0

    @staticmethod
    def __map_to_0_255(value):
        """Maps a float between 0 and 1 to an int between 0 and 255"""
        scaled_up_value = round(255 * value)
        return max(min(scaled_up_value, 255), 0)

    def ppm_string(self):
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
        return self * other

    def __pow__(self, power, modulo=None):
        """Multiplies colors component-wise"""
        return Color(self.__red * power.__red, self.__green * power.__green, self.__blue * power.__blue)

    def __str__(self):
        return f'{{{self.__red}, {self.__green}, {self.__blue}}}'


# Constant colors
BLACK = Color(0, 0, 0)
