# alon markovich and guy truzman
# alonmarko208, guy.truzman
# 313454902 , 312517303
import sys
from ship import Ship
from torpedo import Torpedo
from asteroid import Asteroid
import random
import math
from screen import Screen

DEFAULT_ASTEROIDS_NUM = 5
MSG_OVER = "Game Over"
MSG_WIN = "All The Asteroids have been destroyed!! \n you saved the EARTH"
MSG_LOSE = "THE EARTH IS DOOMED - APOCALYPSE"
MSG_QUIT = "you decided to run away - pathetic"
MSG_HIT = "Warning"
MSG_HIT_CONTENT = "You Are A Loser"


def create_smaller_asteroids(missile, rock, size):
    """This function receives
    :param missile: a torpedo type object
    :param rock: an asteroid type object
    :param size: the rock's size
    :create: two smaller asteroids that derive from rock
    :return: the new asteroids"""
    new_rock_speed_x = (missile.get_x_speed() + rock.get_x_speed()) / \
                       math.sqrt(
                           rock.get_x_speed() ** 2 + rock.get_y_speed() ** 2)
    new_rock_speed_y = (missile.get_y_speed() + rock.get_y_speed()) / \
                       math.sqrt(
                           rock.get_x_speed() ** 2 + rock.get_y_speed() ** 2)
    first_rock = Asteroid(rock.get_x_loc(),
                          rock.get_y_loc(), size - 1)
    first_rock.set_speed(new_rock_speed_x,
                         new_rock_speed_y)
    second_rock = Asteroid(rock.get_x_loc(),
                           rock.get_y_loc(), size - 1)
    second_rock.set_speed(-1 * new_rock_speed_x,
                          -1 * new_rock_speed_y)
    return first_rock, second_rock


class GameRunner:
    """
    This class receives the amount of asteroids, initiate a new game and runs
    it. The description for each method can be found at it's docstring.
    """
    def __init__(self, asteroids_amount):
        """
        creates the screen and places the ship in its start position which
        is randomized.
        asteroid belt - list of asteroid objects to be saved in
        torpedo barrage - list of torpedo objects to save
        :param asteroids_amount: the initial amount of asteroids to place on
        screen
        """
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(
            random.randint(self.__screen_min_x, self.__screen_max_x),
            random.randint(self.__screen_min_y, self.__screen_max_y))
        self.__torpedo_barrage = []
        self.__asteroid_belt = []
        self.__score = 0
        self.add_asteroids_to_list(asteroids_amount)

    def add_asteroids_to_list(self, asteroids_amount):
        """
        creates asteroids and registers them according to the amount given
        :param asteroids_amount: the amount of asteroids to register
        :return: None
        """
        for i in range(asteroids_amount):
            x_loc = random.randint(self.__screen_min_x,
                                   self.__screen_max_x)
            y_loc = random.randint(self.__screen_min_y,
                                   self.__screen_max_y)
            while y_loc == self.__ship.get_y_loc() and x_loc == \
                    self.__ship.get_x_loc():
                x_loc = random.randint(self.__screen_min_x,
                                       self.__screen_max_x)
                y_loc = random.randint(self.__screen_min_y,
                                       self.__screen_max_y)
            rock = Asteroid(x_loc, y_loc)
            self.__screen.register_asteroid(rock, 3)
            self.__asteroid_belt.append(rock)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def collision_check(self):
        """
        checks for collisions -
        first, asteroid - ship collisions, if such happens it removes a life
        from the user and destroys the asteroid without awarding any points
        second, asteroid - torpedo collisions, if such happens the asteroid is
        deleted and if the size is bigger than 1 than 2 smaller ones are
        created. the torpedo is also removed
        :return:
        """
        for rock in self.__asteroid_belt[::-1]:
            if rock.has_intersection(self.__ship):
                if self.__ship.get_health() > 1:
                    self.__screen.show_message(MSG_HIT, MSG_HIT_CONTENT)
                self.__screen.remove_life()
                self.__ship.remove_health()
                self.__screen.unregister_asteroid(rock)
                self.__asteroid_belt.remove(rock)
            for missile in self.__torpedo_barrage[::-1]:
                if rock.has_intersection(missile):
                    self.__score += rock.get_score()
                    self.__screen.set_score(self.__score)
                    self.has_intersected(missile, rock)

    def user_input(self):
        """
        checks if the user clicked a certain key and if so - performs the
        needed action accordignly
        :return: None
        """
        if self.__screen.is_left_pressed():
            self.__ship.set_heading("r")
        elif self.__screen.is_right_pressed():
            self.__ship.set_heading("l")
        if self.__screen.is_up_pressed():
            self.__ship.ship_acceleration()
        if self.__screen.is_space_pressed():
            if len(self.__torpedo_barrage) < 10:
                new_torp = Torpedo(self.__ship)
                self.__torpedo_barrage.append(new_torp)
                self.__screen.register_torpedo(new_torp)

    def has_intersected(self, missile, rock):
        """
        if a collision occurs in asteroid - torpedo than it does as explained
        in collision_check
        :param missile: a torpedo object
        :param rock: a asteroid object
        :return: None
        """
        cur_size = rock.get_size()
        if cur_size == 1:
            self.__screen.unregister_torpedo(missile)
            self.__torpedo_barrage.remove(missile)
            self.__screen.unregister_asteroid(rock)
            self.__asteroid_belt.remove(rock)
        else:
            self.split_asteroid(missile, rock, cur_size)

    def split_asteroid(self, missile, rock, size):
        """
        splits the asteroid into smaller ones
        and registers it into the asteroid list
        :param missile: a torpedo object
        :param rock: a asteroid object
        :param size: asteroid size
        :return: None
        """
        first_rock, second_rock = create_smaller_asteroids(missile, rock,
                                                           size)
        self.__screen.unregister_torpedo(missile)
        self.__torpedo_barrage.remove(missile)
        self.__screen.unregister_asteroid(rock)
        self.__asteroid_belt.remove(rock)
        self.__screen.register_asteroid(first_rock, size - 1)
        self.__screen.register_asteroid(second_rock, size - 1)
        self.__asteroid_belt.append(first_rock)
        self.__asteroid_belt.append(second_rock)

    def end_scenario(self):
        """
        checks all the situations in which the game should end
        1- user input - quit key or q on keyboard
        2 - victory - all asteroids have been destroyed
        3 - ship health is zero
        quits the game after showing a relevant message
        :return: None
        """
        if self.__ship.get_health() == 0:
            self.__screen.show_message(MSG_OVER,
                                       MSG_LOSE)
            self.__screen.end_game()
            sys.exit()
        if len(self.__asteroid_belt) == 0:
            self.__screen.show_message(MSG_OVER,
                                       MSG_WIN)
            self.__screen.end_game()
            sys.exit()
        if self.__screen.should_end():
            self.__screen.show_message(MSG_OVER,
                                       MSG_QUIT)
            self.__screen.end_game()
            sys.exit()

    def movement(self, item):
        """
        receives an object and updates its location
        :param item: an object - asteroid, ship or torpedo
        :return: the new x,y locations (int)
        """
        new_x = self.__screen_min_x + (
                item.get_x_loc() + item.get_x_speed() - self.__screen_min_x) \
                % (self.__screen_max_x - self.__screen_min_x)
        new_y = self.__screen_min_y + (
                item.get_y_loc() + item.get_y_speed() - self.__screen_min_y) \
                % (self.__screen_max_y - self.__screen_min_y)
        return new_x, new_y

    def move_draw_everything(self):
        """
        this function moves every object type on the screen and draws them
        as well.
        if a torpedo exceeds 200 game cycles it is deleted
        :return: None
        """
        self.__screen.draw_ship(self.__ship.get_x_loc(),
                                self.__ship.get_y_loc(),
                                self.__ship.get_heading())
        self.__ship.set_location(self.movement(self.__ship))
        for rock in self.__asteroid_belt:
            self.__screen.draw_asteroid(rock, rock.get_x_loc(),
                                        rock.get_y_loc())
            rock.set_location(self.movement(rock))
        for missile in self.__torpedo_barrage[::-1]:
            if missile.get_cycles() > 200:
                self.__screen.unregister_torpedo(missile)
                self.__torpedo_barrage.remove(missile)
                continue
            missile.set_location(self.movement(missile))
            self.__screen.draw_torpedo(missile, missile.get_x_loc(),
                                       missile.get_y_loc(),
                                       missile.get_heading())

    def _game_loop(self):
        """
        the main game loop - checks if there is a reason to end the game
        and if not it gets the user input, moves the object and draws them on
        the screen.
        finally checks for collisions
        :return: none
        """
        # Your code goes here
        self.end_scenario()
        self.user_input()
        self.move_draw_everything()
        self.collision_check()



def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
