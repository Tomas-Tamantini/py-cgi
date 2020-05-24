from class_lib.color import BLACK
from class_lib.light import Ray
from class_lib.useful_functions import coordinate_system
from basics import Vector
from math import sqrt, sin, cos


class Image:
    """2D-Array of color pixels"""

    def __init__(self, height=320, width=200):
        self.__width = width
        self.__height = height
        self.__pixels = [[None for _ in range(width)] for _ in range(height)]

    def get_pixel(self, row, column):
        """Gets pixel color from given row and column"""
        pix = self.__pixels[row][column]
        if pix:
            return pix
        return BLACK  # Default color returned if pixel has not been set

    def set_pixel(self, color, row, column):
        """Sets pixel to given color"""
        self.__pixels[row][column] = color

    def save_as_ppm(self, file_name):
        with open(file_name, 'w') as img_file:
            # Write header
            # Indicate that it is a ppm file, and give width and height
            img_file.write(f'P3 {self.__width} {self.__height}\n')
            # Maximum value
            img_file.write('255\n')
            # Write values
            for i in range(self.__height):
                for j in range(self.__width):
                    img_file.write(self.get_pixel(i, j).ppm_string() + '\t')
                img_file.write('\n')


class Camera:
    """Camera positioned in 3d space"""

    def __init__(self, resolution=(20, 30), position=Vector(10, 0, 0), direction=Vector(-1, 0, 0), zoom=1,
                 tilt_angle=0):
        """Initialize new camera. Attention: Resolution is given like a matrix = height, width"""
        self.__resolution = resolution
        self.position = position
        self.direction = direction.unit
        self.zoom = zoom
        self.tilt_angle = tilt_angle

        # Auxiliary variables
        r_ver = self.__resolution[0] - 1
        r_hor = self.__resolution[1] - 1
        discriminant = r_ver * r_ver + r_hor * r_hor

        delta = 1 / (self.zoom * sqrt(discriminant)) if discriminant > 0 else 1
        i_prime, j_aux, k_aux = coordinate_system(self.direction)
        j_prime = j_aux * cos(self.tilt_angle) + k_aux * sin(self.tilt_angle)
        k_prime = k_aux * cos(self.tilt_angle) - j_aux * sin(self.tilt_angle)

        self.v_vertical = -delta * k_prime
        self.v_horizontal = -delta * j_prime
        self.offset_vertical = r_ver / 2
        self.offset_horizontal = r_hor / 2

    def __pixel_pos(self, row, column) -> Vector:
        """Pixel position given its row and column"""
        return self.position + self.direction + (row - self.offset_vertical) * self.v_vertical + (
                column - self.offset_horizontal) * self.v_horizontal

    def get_ray(self, row, column):
        """Ray from camera through given pixel"""
        p0 = self.position
        direction = self.__pixel_pos(row, column) - self.position
        return Ray(p0, direction)
