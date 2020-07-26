from math import sqrt, sin, cos

from PIL import Image as PillowImage
from basics import Vector
from numpy import array, uint8

from class_lib.color import BLACK
from class_lib.coordinate_system import CoordinateSystem
from class_lib.light import Ray
from class_lib.useful_functions import reflected_vector
from globals import MAX_RECURSION_COUNTER


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

    def as_pillow_image(self):
        new_pixel_map = [[self.get_pixel(i, j).as_int_tuple() for j in range(self.__width)] for i in
                         range(self.__height)]
        pixel_array = array(new_pixel_map, dtype=uint8)
        return PillowImage.fromarray(pixel_array)

    def save_as_png(self, file_name):
        """Save image as png file"""
        new_image = self.as_pillow_image()
        new_image.save(file_name)

    def save_as_ppm(self, file_name):
        """Save image as PPM file"""
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

        i_prime, j_prime, k_prime = CoordinateSystem.unit_base_axis(self.__direction, self.__tilt_angle)

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
    """Collection of objects, light sources, and a camera"""

    def __init__(self, camera, objects, illumination):
        self.__camera = camera
        self.__objects = objects
        self.__background_color = BLACK
        self.__illumination = illumination

    def ray_is_obstructed(self, ray, light_source_distance):
        """
        Returns true if there is an object obstructing the light source and causing a shadow
        """
        for obj in self.__objects:
            distance = obj.intersection_distance(ray)
            if distance and distance <= light_source_distance:
                return True
        return False

    def __nearest_object_hit_by_ray(self, ray):
        """
        Find closest object which intersects ray
        Returns object itself, and its distance to ray origin
        """
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
            return self.__objects[save_object_index], minimum_distance
        return None, None

    def render_image(self):
        """Produce image"""
        image = Image(self.__camera.image_height, self.__camera.image_width)

        # Loop through all pixels
        for row in range(self.__camera.image_height):
            if self.__camera.image_height > 200 and (row + 1) % 50 == 0:
                print(f"Rendering row {row + 1}/{self.__camera.image_height}")  # To give an idea of the time left
            for col in range(self.__camera.image_width):
                ray = self.__camera.get_ray(row, col)
                pix_color = self.ray_trace(ray)
                image.set_pixel(row, col, pix_color)
        print("Done rendering.")
        return image

    def __get_ambient_light(self, chip):
        return chip.material.ambient_light_reflectivity ** self.__illumination.ambient_light.intensity

    @staticmethod
    def __get_diffuse_light(chip, ray_to_light_source, light_source):
        diffuse_multiplier = abs(ray_to_light_source.direction * chip.normal)
        diffuse_multiplier *= light_source.attenuator_by_distance_sq(chip.position)
        return diffuse_multiplier * chip.material.diffuse_light_reflectivity ** light_source.intensity

    @staticmethod
    def __get_phong_blinn_light(chip, incoming_ray, ray_to_light_source, light_source):
        h = (- incoming_ray.direction + ray_to_light_source.direction).unit
        r = reflected_vector(ray_to_light_source.direction, chip.normal)
        specular_multiplier = max(h * r, 0)

        specular_multiplier = chip.material.specular_multiplier * (
                specular_multiplier ** chip.material.specular_coefficient)

        specular_multiplier *= light_source.attenuator_by_distance_sq(chip.position)
        return specular_multiplier * light_source.intensity

    @staticmethod
    def __get_refracted_ray(chip, incoming_ray, ray_is_coming_from_outside):
        alpha = 1 / chip.material.refractive_index if ray_is_coming_from_outside else chip.material.refractive_index
        aux = alpha * incoming_ray.direction * chip.normal
        discriminant = aux * aux + 1 - alpha * alpha
        if discriminant < 0:
            return None
        beta = -aux - sqrt(discriminant) if ray_is_coming_from_outside else -aux + sqrt(discriminant)
        new_direction = alpha * incoming_ray.direction + beta * chip.normal
        return Ray(chip.position, new_direction)

    def color_at(self, chip, incoming_ray, recursion_depth):
        """Find color at given point of the scene"""
        color = BLACK
        if recursion_depth >= MAX_RECURSION_COUNTER:
            return color
        # Ambient light:
        color += self.__get_ambient_light(chip)

        # Light sources:
        for light_source in self.__illumination.light_sources:
            new_ray = light_source.ray_to_light_source(chip.position)
            # Check if light source is shining on the right side of the surface.
            cos_incoming = incoming_ray.direction * chip.normal
            cos_new_ray = new_ray.direction * chip.normal
            if cos_incoming * cos_new_ray > 0:
                # No good. They should have opposite signs, to indicate that the light is hitting the same side
                # of the surface that the camera sees. Otherwise, an opaque tube would be lit inside from a light
                # source outside, for example.
                continue
            # Check if light is obstructed, causing a shadow
            if not self.ray_is_obstructed(new_ray, light_source.distance_to_point(
                    chip.position)):  # Light source distance is infinity
                # Diffuse reflection
                color += Scene.__get_diffuse_light(chip, new_ray, light_source)
                # Specular reflection (Phong-Blinn)
                color += Scene.__get_phong_blinn_light(chip, incoming_ray, new_ray, light_source)
        # Recursive bits: Reflection and refraction
        # Reflection
        if chip.material.reflective_index > 0:
            new_direction = -reflected_vector(incoming_ray.direction, chip.normal)
            refracted_ray = Ray(chip.position, new_direction)

            # Find nearest object
            nearest_object, object_distance = self.__nearest_object_hit_by_ray(refracted_ray)
            if nearest_object is not None:
                intersection_position = refracted_ray.position_at_time(object_distance)
                new_chip = nearest_object.chip_at(intersection_position)
                attenuation = chip.material.reflective_index
                color += attenuation * self.color_at(new_chip, refracted_ray, recursion_depth + 1)
        # Refraction
        if chip.material.is_refractive:
            ray_is_coming_from_outside = chip.normal * incoming_ray.direction < 0
            refracted_ray = Scene.__get_refracted_ray(chip, incoming_ray, ray_is_coming_from_outside)
            if refracted_ray:
                # Find nearest object
                nearest_object, object_distance = self.__nearest_object_hit_by_ray(refracted_ray)
                if nearest_object is not None:
                    intersection_position = refracted_ray.position_at_time(object_distance)
                    new_chip = nearest_object.chip_at(intersection_position)
                    new_color = self.color_at(new_chip, refracted_ray, recursion_depth + 1)
                    vector_travelled = incoming_ray.initial_point - chip.position if ray_is_coming_from_outside else chip.position - new_chip.position
                    distance_travelled = vector_travelled.length
                    attenuated_color = chip.material.attenuate_by_refraction(new_color, distance_travelled)
                    color += attenuated_color

        return color

    def ray_trace(self, ray):
        """Traces ray through the scene and return a color"""
        color = BLACK

        # Find closest object which intersects ray
        nearest_object, object_distance = self.__nearest_object_hit_by_ray(ray)

        # Draw
        if nearest_object is not None:
            intersection_position = ray.position_at_time(object_distance)
            chip = nearest_object.chip_at(intersection_position)
            color += self.color_at(chip, ray, recursion_depth=0)
        else:
            # Draw background color
            return self.__background_color

        return color
