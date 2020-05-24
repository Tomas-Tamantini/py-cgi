from class_lib.color import BLACK
from class_lib.light import Ray
from class_lib.useful_functions import coordinate_system
from class_lib.color import Color
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

    def set_pixel(self, row, column, color):
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
        self.__position = position
        self.__direction = direction.unit
        self.__zoom = zoom
        self.__tilt_angle = tilt_angle

        # Auxiliary variables
        r_ver = self.__resolution[0] - 1
        r_hor = self.__resolution[1] - 1
        discriminant = r_ver * r_ver + r_hor * r_hor

        delta = 1 / (self.__zoom * sqrt(discriminant)) if discriminant > 0 else 1
        i_prime, j_aux, k_aux = coordinate_system(self.__direction)
        j_prime = j_aux * cos(self.__tilt_angle) + k_aux * sin(self.__tilt_angle)
        k_prime = k_aux * cos(self.__tilt_angle) - j_aux * sin(self.__tilt_angle)

        self.v_vertical = -delta * k_prime
        self.v_horizontal = -delta * j_prime
        self.offset_vertical = r_ver / 2
        self.offset_horizontal = r_hor / 2

    @property
    def image_height(self):
        return self.__resolution[0]

    @property
    def image_width(self):
        return self.__resolution[1]

    def __pixel_pos(self, row, column) -> Vector:
        """Pixel position given its row and column"""
        return self.__position + self.__direction + (row - self.offset_vertical) * self.v_vertical + (
                column - self.offset_horizontal) * self.v_horizontal

    def get_ray(self, row, column):
        """Ray from camera through given pixel"""
        p0 = self.__position
        direction = self.__pixel_pos(row, column) - self.__position
        return Ray(p0, direction)


class Scene:
    def __init__(self, camera, objects):
        self.__camera = camera
        self.__objects = objects
        self.background_color = Color('#87CEEB')

    def __nearest_object_hit_by_ray(self, ray):
        """Find closest object which intersects ray"""
        save_object_index = None
        minimum_distance = -1
        for obj_index, obj in enumerate(self.__objects):
            distance = obj.intersection_distance(ray)
            if not distance:
                continue
            if distance < minimum_distance or minimum_distance < 0:
                minimum_distance = distance
                save_object_index = obj_index
        if save_object_index is not None:
            return self.__objects[save_object_index]
        return None

    def render_image(self):
        image = Image(self.__camera.image_height, self.__camera.image_width)

        # Loop through all pixels
        for row in range(self.__camera.image_height):
            for col in range(self.__camera.image_width):
                ray = self.__camera.get_ray(row, col)
                pix_color = self.ray_trace(ray)
                image.set_pixel(row, col, pix_color)

        return image

    def ray_trace(self, ray):
        """Traces ray through the scene and return a color"""
        # Find closest object which intersects ray
        nearest_object = self.__nearest_object_hit_by_ray(ray)

        # Draw
        if nearest_object is not None:
            # TODO: Correct this
            return nearest_object.material
        else:
            # Draw background color
            return self.background_color
