from car import Car
# alon markovich
# alonmarko208
# 313454902


class Board:
    """
   creates a board in a certain size and has functions to change it, add it and etc
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__board = [["_" for x in range(7)] for k in range(7)]
        self.__board[3].append("X")
        self.__car_array = []

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        board = ""
        for x in self.__board:
            row = " ".join(x)
            board = board + row + "\n"
        return str(board)

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        cor_list = []
        for i in range(len(self.__board)):
            for y in range(len(self.__board[i])):
                if i == 3 and y == 7:
                    continue
                cor_tup = i, y
                cor_list.append(cor_tup)
        cor_list.append((3, 7))
        return cor_list

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        if not self.__car_array:
            return []
        possible_moves = []
        for auto in self.__car_array:
            current_moves = auto.possible_moves()
            name = auto.get_name()
            for direction, description in current_moves.items():
                target_cell = auto.movement_requirements(direction)
                if target_cell[0] not in self.cell_list():
                    continue
                if self.cell_content(target_cell[0]) is not None:
                    continue
                possible_moves.append((name, direction, description))
        return possible_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name of the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        col = coordinate[1]
        row = coordinate[0]
        if self.__board[row][col] == "_" or self.__board[row][col] == "X":
            return
        return self.__board[row][col]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        car_span = car.car_coordinates()
        car_name = car.get_name()
        cells = self.cell_list()
        for i in self.__car_array:
            if car_name == i.get_name():
                return False
        for x in car_span:
            if x not in cells:
                return False
            if self.cell_content(x) is not None:
                return False
        counter = 0
        for x in car_span:
            row = x[0]
            col = x[1]
            self.__board[row][col] = car_name
            counter += 1
        if counter == len(car_span):
            self.__car_array.append(car)
            return True

    def move_car(self, name, movekey):
        """
            moves car one step in given direction.
            :param name: name of the car to move
            :param movekey: Key of move in car to activate
            :return: True upon success, False otherwise
            """
        # implement your code and erase the "pass"
        flag_moving = False
        flag_updating = False
        for i in range(len(self.__car_array)):
            car_name = self.__car_array[i].get_name()
            moves = self.specific_moves(car_name)
            if movekey in moves:
                if car_name == name and self.__car_array[i].move(movekey):
                    flag_moving = True
                    car_loc = self.__car_array[i].car_coordinates()
                    for j in range(len(self.__board)):
                        if car_name in self.__board[j]:
                            for k in range(len(self.__board[j])):
                                if self.__board[j][k] == car_name:
                                    self.__board[j][k] = "_"
                    for location in car_loc:
                        self.__board[location[0]][location[1]] = car_name
                    flag_updating = True
        if flag_moving and flag_updating:
            return True
        else:
            return False

    def specific_moves(self, name):
        """
        returns list of possible directions for a specific car in the board
        :param name: car name
        :return: list of strings
        """
        final_moves = []
        possible_moves = self.possible_moves()
        for car in self.__car_array:
            car_name = car.get_name()
            if car_name == name:
                for move in possible_moves:
                    if move[0] == car_name:
                        final_moves.append(move[1])
        return final_moves



