from board import *
from board import Car
import helper as h
from os import path
import sys

CAR_NAMES = ["O", "R", "W", "B", "G", "Y"]
VALID_MOVES = ["l", "r", "u", "d"]


def valid_input(user_input):
    """
    checks if the input from the command line is good
    """
    if len(user_input) == 3:
        if user_input[0].isupper() and user_input[1] == "," and \
                user_input[2].islower():
            if user_input[0] in CAR_NAMES and user_input[2] in VALID_MOVES:
                return True
    return False


def check_file(filename):
    #checks if the file exists
    if len(filename) != 1:
        return "to many arguments given"
    if not path.exists(filename[0]):
        return "the file needed does not exist"
    return


class Game:
    """
    this class represents a rush hour game,
    gets a board with cars and plays the game until victory or
    the user quits
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code here (and then delete the next line - 'pass')
        self.__game_board = board
        self.__victory = board.target_location()

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        returns - None if the turn ended succfully and car moves
        False if the user decided to terminate the game
        True if the car landed at the victory coordinates
        """
        # implement your code here (and then delete the next line - 'pass')
        while True:
            user_input = input("enter a car name and direction - eg: 'R,l' ")
            if user_input == "!":
                return False
            if valid_input(user_input):
                if self.__game_board.move_car(user_input[0], user_input[2]):
                    print(self.__game_board)
                    return
            print("invalid input")

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code here (and then delete the next line - 'pass')
        print(self.__game_board)
        while True:
            if self.__game_board.cell_content(self.__victory) is not None:
                print("a Car has Landed at the exit! the game has ended")
                return
            if self.__single_turn() is False:
                print("the game has been terminated according to user input")
                return
            else:
                continue


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    filename = sys.argv[1:]
    if check_file(filename) is None:
        game_board = Board()
        car_dictionary = h.load_json(filename[0])
        car_list = []
        for name, details in car_dictionary.items():
            if 2 <= details[0] <= 4 and name in CAR_NAMES and name not in \
                    car_list:
                car = Car(name, details[0], tuple(details[1]), details[2])
                if game_board.add_car(car):
                    car_list.append(name)
        game = Game(game_board)
        game.play()
    else:
        print(check_file(filename))
