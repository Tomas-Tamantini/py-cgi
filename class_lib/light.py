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
