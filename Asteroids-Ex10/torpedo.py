import math

TORPEDO_RADIUS = 4


def init_speed_x(ship_speed, ship_heading):
    """This function receives
    :param ship_speed: the ship's speed on x axis
    :param ship_heading: the ship's heading
    :return: the torpedo's speed on x axis"""
    return ship_speed + 2 * math.cos(math.radians(ship_heading))


def init_speed_y(ship_speed, ship_heading):
    """This function receives
    :param ship_speed: the ship's speed on y axis
    :param ship_heading: the ship's heading
    :return: the torpedo's speed on y axis"""
    return ship_speed + 2 * math.sin(math.radians(ship_heading))


class Torpedo:
    """
    This class receives the object ship and create a torpedo fired from him.
    The description for each method can be found at it's docstring.
    """

    def __init__(self, ship):
        """This function receives
        :param ship: a Ship type object
        and initiate a new torpedo with the same location and heading as the
        given ship. The torpedo's speed is defined by a formula in init_speed.
        Furthermore, the function initiate the torpedo's radius and life by
        the default parameters"""
        self.__heading = ship.get_heading()
        self.__x_loc = ship.get_x_loc()
        self.__x_speed = init_speed_x(ship.get_x_speed(), self.__heading)
        self.__y_loc = ship.get_y_loc()
        self.__y_speed = init_speed_y(ship.get_y_speed(), self.__heading)
        self.__radius = TORPEDO_RADIUS
        self.__life = 0

    def get_x_speed(self):
        """This function
        :return: the torpedo's speed on X axis"""
        return self.__x_speed

    def get_x_loc(self):
        """This function
        :return: the torpedo's location on X axis"""
        return self.__x_loc

    def get_y_speed(self):
        """This function
        :return: the torpedo's speed on Y axis"""
        return self.__y_speed

    def get_y_loc(self):
        """This function
        :return: the torpedo's location on Y axis"""
        return self.__y_loc

    def get_heading(self):
        """This function
        :return: the torpedo's heading"""
        return self.__heading

    def get_radius(self):
        """This function
        :return: the torpedo's radius"""
        return self.__radius

    def set_location(self, new_loc):
        """This function receives
        :param new_loc: the coordination of the torpedo's new location
        :change: the torpedo's location in both axis"""
        self.__x_loc = new_loc[0]
        self.__y_loc = new_loc[1]
        self.__life += 1

    def get_cycles(self):
        """This function
        :return: the number of cycles the torpedo took part in"""
        return self.__life
