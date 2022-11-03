import random
import math

MIN_SPEED = 1
MAX_SPEED = 4
BIG = 3
MEDIUM = 2
SMALL = 1
POINTS_FOR_BIG = 20
POINTS_FOR_MEDIUM = 50
POINTS_FOR_SMALL = 100


class Asteroid:
    """
    This class receives the location on X and Y axis and the asteroid size
    (default 3 is given if nothing was inserted) and creates an asteroid.
    The description for each method can be found at it's docstring.
    """
    def __init__(self, x_loc, y_loc, size=3):
        """This function receives
        :param x_loc: the location on X axis
        :param y_loc: the location on Y axis
        :param size: the asteroid's size (3 by default)
        and creates a new ship with random speed rates"""
        self.__x_loc = x_loc
        self.__x_speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.__y_loc = y_loc
        self.__y_speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.__size = size
        self.__radius = size * 10 - 5

    def get_x_speed(self):
        """This function
        :return: the asteroid's speed on X axis"""
        return self.__x_speed

    def get_x_loc(self):
        """This function
        :return: the asteroid's location on X axis"""
        return self.__x_loc

    def get_y_speed(self):
        """This function
        :return: the asteroid's speed on Y axis"""
        return self.__y_speed

    def get_y_loc(self):
        """This function
        :return: the asteroid's location on Y axis"""
        return self.__y_loc

    def get_size(self):
        """This function
        :return: the asteroid's size"""
        return self.__size

    def set_speed(self, x, y):
        """This function receives
        :param x: new speed on X axis
        :param y: new speed on Y axis
        :change: the asteroid's speed in both axis"""
        self.__x_speed = x
        self.__y_speed = y

    def set_location(self, new_loc):
        """This function receives
        :param new_loc: the coordination of the asteroid's new location
        :change: the asteroid's location in both axis"""
        self.__x_loc = new_loc[0]
        self.__y_loc = new_loc[1]

    def has_intersection(self, obj):
        """This function receives
        :param obj: an object on the screen
        :return: True - if the asteroid touch the object, False - otherwise"""
        distance = math.sqrt(
            math.pow(obj.get_x_loc() - self.__x_loc, 2) + math.pow(
                obj.get_y_loc() - self.__y_loc, 2))
        if distance <= self.__radius + obj.get_radius():
            return True
        return False

    def get_score(self):
        """This function checks the size of the smashed asteroid
        :return: the points that the user should get"""
        if self.__size == BIG:
            return POINTS_FOR_BIG
        elif self.__size == MEDIUM:
            return POINTS_FOR_MEDIUM
        elif self.__size == SMALL:
            return POINTS_FOR_SMALL
