class Car:
    """
    this class creates a car object wich has direction,length, name and a
    location. it has basic functions like move,get name and get the full
    location of the car, and which cell has to be free for the car to move
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
        location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"
        self.__name = name
        self.__length = length
        self.__coordinate = location
        self.__direction = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        # implement your code and erase the "pass"
        location_list = [self.__coordinate]
        col = self.__coordinate[1]
        row = self.__coordinate[0]
        if self.__direction == 1:
            for i in range(1, self.__length):
                location_list.append((row, col + 1))
                col += 1
        else:
            for i in range(1, self.__length):
                location_list.append((row + 1, col))
                row += 1
        return location_list

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        vertical_dict = {"u": "this makes the car go up by 1 block",
                         "d": "this makes the car go down by 1 block"}
        horizontal_dict = {"l": "this makes the car go left by 1 block",
                           "r": "this makes the car go right by 1 block"}
        car_direction = self.__direction
        if car_direction == 1:
            return horizontal_dict
        return vertical_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
         move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        required = []
        car_coor_lst = self.car_coordinates()
        car_len = self.__length
        if movekey == "d":
            row = car_coor_lst[car_len - 1][0]
            col = car_coor_lst[car_len - 1][1]
            required.append((row + 1, col))
        if movekey == "u":
            row = self.__coordinate[0]
            col = self.__coordinate[1]
            required.append((row - 1, col))
        if movekey == "l":
            row = self.__coordinate[0]
            col = self.__coordinate[1]
            required.append((row, col - 1))
        if movekey == "r":
            row = car_coor_lst[car_len - 1][0]
            col = car_coor_lst[car_len - 1][1]
            required.append((row, col + 1))
        return required

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        possible = self.possible_moves()
        if movekey in possible:
            target_cell = self.movement_requirements(movekey)
            car_span = self.car_coordinates()
            if movekey == "u":
                self.__coordinate = target_cell[0]
                return True
            elif movekey == "l":
                self.__coordinate = target_cell[0]
                return True
            elif movekey == "r":
                self.__coordinate = car_span[1]
                return True
            elif movekey == "d":
                self.__coordinate = car_span[1]
                return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        # implement your code and erase the "pass"
        return self.__name
