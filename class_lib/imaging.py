from class_lib.color import BLACK
from class_lib.light import Ray
from basics import Vector


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

    def __pixel_pos(self, row, column):
        """Pixel position given its row and column"""
        pass

    def get_ray(self, row, column):
        """Ray from camera through given pixel"""
        p0 = self.position
        direction = self.__pixel_pos(row, column) - self.position
        return Ray(p0, direction)
