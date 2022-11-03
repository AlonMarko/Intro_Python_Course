import math

INIT_PARAMS = 0
SHIP_RADIUS = 1
INIT_HEALTH = 3
FULL_CYCLE = 360
TURNING_UNIT = 7


class Ship:
    """
    This class receives the location on X and Y axis and creates a ship.
    The description for each method can be found at it's docstring.
    """
    def __init__(self, x_loc, y_loc):
        """This function receives
        :param x_loc: the location on X axis
        :param y_loc: the location on Y axis
        and creates a new ship with default parameters"""
        self.__x_loc = x_loc
        self.__x_speed = INIT_PARAMS
        self.__y_loc = y_loc
        self.__y_speed = INIT_PARAMS
        self.__heading = INIT_PARAMS
        self.__radius = SHIP_RADIUS
        self.__health = INIT_HEALTH

    def get_x_speed(self):
        """This function
        :return: the speed on X axis"""
        return self.__x_speed

    def get_x_loc(self):
        """This function
        :return: the location on X axis"""
        return self.__x_loc

    def get_y_speed(self):
        """This function
        :return: the speed on Y axis"""
        return self.__y_speed

    def get_y_loc(self):
        """This function
        :return: the location on Y axis"""
        return self.__y_loc

    def get_heading(self):
        """This function
        :return: the ship's heading"""
        return self.__heading

    def set_location(self, new_loc):
        """This function receives
        :param new_loc: the coordination of the new location
        :change: the location on X and Y axis"""
        self.__x_loc = new_loc[0]
        self.__y_loc = new_loc[1]

    def set_heading(self, movekey):
        """This function receives
        :param movekey: a string (either "l" or "r")
        :change: the angle of the ship, according to the given movekey"""
        if movekey == "l":
            self.__heading -= TURNING_UNIT
            if self.__heading < 0:
                self.__heading += FULL_CYCLE
        elif movekey == "r":
            self.__heading += TURNING_UNIT
            if self.__heading > FULL_CYCLE:
                self.__heading -= FULL_CYCLE

    def ship_acceleration(self):
        """This function is being called if up bottom was pressed and
        :change: the ship's speed"""
        self.__x_speed = self.__x_speed + math.cos(
            math.radians(self.__heading))
        self.__y_speed = self.__y_speed + math.sin(
            math.radians(self.__heading))

    def get_radius(self):
        """This function
        :return: the ship's radius"""
        return self.__radius

    def get_health(self):
        """This function
        :return: the ship's health (how many lives remind)"""
        return self.__health

    def remove_health(self):
        """This function
        :change: the ship's health (decrease the number of lives by 1)"""
        self.__health -= 1
