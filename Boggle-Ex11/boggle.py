import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import boggle_board_randomizer as br
import sys

INFO = """
             ***Please Initialize game!***
    The game is played with a 4X4 board of letters.
    The objective is to form as many words as possible by
    concatenating adjacent letters.
    you have 3 minutes(180 seconds) after that the game will end
    your current score appears on the bottom - the longer the word more points 
    you get!
    in order to key in words - press with your mouse on the letter.
    after you finish press submit to key-in the word, if the word you entered 
    is legit it will appear on the right, if you hit the same word twice - 
    nothing will happen - GOOD LUCK
"""
FILE_NAME = "boggle_dict.txt"
ALL_WORDS = set()
TIME_COUNT = 180
ROWS = 4
COLS = 4
SCORE_TITLE = "Score Board"
TIME_OUT_T = "Time's Out"
NO_SCORES = "No Available Scores"
ERROR_T = "Error"
ERROR_M = "word cache not found - game cannot run"
STATUS_B = "Get you daily Dose of Boggle"
SHOW_SCORE_B = "Show Scores"
HIDE_SCORES_B = "Hide Scores"
START_GAME_B = "Start Game"
QUIT_GAME_B = "Quit Game"
MAIN_MENU = "Main Menu"
SUBMIT_B = "Submit Word"
GAME_TITLE = "The Best Boggle No One Ever Asked For"
LEADER_B_T = "Score Board Registry"
LEADER_B_TEXT = "Enter Your Name Here:"


def boggle_words_reader(file_name):
    """
    opens the fiel and creates a set of all the words in it
    :param file_name: word file name
    """
    try:
        global ALL_WORDS
        words_file = open(file_name)
        ALL_WORDS = set([line.strip() for line in words_file])
    except FileNotFoundError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(ERROR_T, ERROR_M)
        sys.exit()


class Board:
    """
    this Class represents the Board part of the game and includes all the methods
    related to key presses and answer submitting.
    score tracking.
    this class represents one score cycle.
    """

    def __init__(self, root, good_words):
        self.words = good_words
        self.parent = root
        self.buttons_dict = dict()
        self.board = br.randomize_board()
        self.possible_clicks_set = set()
        self.clicked_set = set()
        self.word = ""
        self.guessed = []
        self.score = 0

    def make_letters(self):
        """
        this method creates the buttons on the board and places them
        """
        index = 0
        board = self.board
        for i in range(len(board)):
            for j, letter in enumerate(board[i]):
                button = tk.Button(self.parent, text=letter,
                                   font=("David", 49), bg="grey",
                                   fg="black",
                                   command=lambda i=i,
                                                  j=j: self.add_letter(
                                       (i, j)))
                button.grid(row=index // ROWS, column=index % COLS,
                            sticky='EW')
                self.buttons_dict[(i, j)] = button
                index += 1

    def set_all_color(self, color):
        """
        this method changed the color of all buttons to the recieved color
        :param color: string
        """
        for button in self.buttons_dict.values():
            button.configure(bg=color)

    def possible_clicks(self, coord):
        """
        gets the coordinate and adds to a set all the possible clicks for the
        next move from that button
        :param coord: tuple (x,y) of ints
        """
        i, j = coord[0], coord[1]
        for row in range(-1, 2):
            for col in range(-1, 2):
                if row == 0 and col == 0:
                    continue
                if (i + row, j + col) in self.buttons_dict.keys() and (
                        i + row, j + col) not in self.clicked_set:
                    self.possible_clicks_set.add((i + row, j + col))

    def score_calculate(self):
        """
        adds to the current score to the total score
        """
        self.score += len(self.word) ** 2

    def add_letter(self, coord):
        """
        after a letter is clicked this method checks if the click is legit
        if so it adds the letter to the word being written
        :param coord: tuple (x,y) of ints
        """
        if coord in self.possible_clicks_set or not self.possible_clicks_set:
            if coord not in self.clicked_set:
                self.possible_clicks_set = set()
                self.possible_clicks(coord)
                letter = self.board[coord[0]][coord[1]]
                self.word += letter
                self.buttons_dict.get(coord).configure(bg="green")
                self.clicked_set.add(coord)

    def submited(self):
        """
        this method upon submitting the word if it is legit and if so
        adds it to the guessed words window.
        also does a reset for the possible clicks and clicked buttons for the
        next guess
        """
        if self.word in ALL_WORDS and self.word not in self.guessed:
            self.guessed.append(self.word)
            self.words.insert(tk.END, self.word)
            self.score_calculate()
        self.set_all_color("grey")
        self.word = ""
        self.possible_clicks_set = set()
        self.clicked_set = set()


class Game:
    """
    this class operates as the game managing all the screens and screen changes
    it accepts a board object for each new game.
    keeps the highest score. and creates most of the GUI.
    """

    def __init__(self, root):
        self.root = root
        self.update_root()
        self.header = tk.Label(self.root)
        self.main_frame = tk.Frame(self.root)
        self.right_frame = tk.Frame(self.root)
        self.scroll_bar = tk.Scrollbar(self.right_frame)
        self.words_success = tk.Listbox(self.right_frame)
        self.board_frame = tk.Frame(self.main_frame)
        self.initialize_frame = tk.Frame(self.main_frame)
        self.start_button = tk.Button(self.root)
        self.finish_button = tk.Button(self.root)
        self.status_bar = tk.Label(self.root)
        self.information = tk.Label(self.initialize_frame)
        self.leader_board = tk.Button(self.root)
        self.configure()
        self.pack_all()
        self.tick = False
        self.board = None
        self.high_score = []

    def update_root(self):
        """
        configures the root for specified requierments
        """
        self.root.title(GAME_TITLE)
        self.root.geometry("700x670")
        self.root.resizable(width=False, height=False)
        self.root.configure(background='black')

    def configure(self):
        """
        configures all the objects in the game.
        """
        self.header.configure(text="BOGGLE", font=("David", 55), fg="red",
                              bg="grey")
        self.main_frame.configure(bg="red")
        self.words_success.configure(bg='silver', relief=tk.SUNKEN, bd=3)
        self.initialize_frame.configure(height=470, width=470, bg="black")
        self.board_frame.configure(height=470, width=470, bd=8, bg="yellow")
        self.start_button.configure(text=START_GAME_B, font=("David", 23),
                                    bg="grey",
                                    fg="blue", command=self.raise_frame,
                                    width=9)
        self.finish_button.configure(text=QUIT_GAME_B, font=("David", 23),
                                     bg="grey", fg="yellow",
                                     command=self.root.quit,
                                     width=9)
        self.leader_board.configure(text=SHOW_SCORE_B, font=("David", 23),
                                    bg="grey", fg="red", command=
                                    self.leader_boards,
                                    width=9)
        self.status_bar.configure(text=STATUS_B, bd=5,
                                  relief=tk.SUNKEN,
                                  anchor=tk.W, font=("David", 15))
        self.information.configure(text=INFO, font=("David", 12))
        self.words_success.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.configure(command=self.words_success.yview)

    def pack_all(self):
        """
        places all objects on the GUI
        """
        self.header.pack(fill=tk.X)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.words_success.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame.pack(side=tk.TOP, anchor=tk.NW)
        for frame in (self.board_frame, self.initialize_frame):
            frame.grid(row=0, column=0, sticky='news')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.start_button.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y)
        self.finish_button.pack(side=tk.LEFT, anchor=tk.NE, fill=tk.Y)
        self.leader_board.pack(side=tk.LEFT, anchor=tk.NE, fill=tk.Y)
        self.information.pack(fill=tk.BOTH, expand=True)

    def raise_frame(self):
        """
        creates a board and raises the Frame to start a round
        starts the countdown
        """
        self.board = Board(self.board_frame, self.words_success)
        self.board.make_letters()
        self.tick = True
        self.board_frame.tkraise()
        self.leader_board.pack_forget()
        self.start_button.configure(text=SUBMIT_B,
                                    command=self.board.submited)
        self.finish_button.configure(text=MAIN_MENU,
                                     command=self.raise_info_screen)
        self.words_success.delete(0, tk.END)
        self.countdown(TIME_COUNT)

    def raise_info_screen(self):
        """
        raises the info screen and ends that game round.
        :return:
        """
        self.tick = False
        self.status_bar.configure(text=STATUS_B)
        self.initialize_frame.tkraise()
        self.start_button.configure(text=START_GAME_B,
                                    command=self.raise_frame)
        self.finish_button.configure(text=QUIT_GAME_B, command=self.root.quit)
        self.leader_board.pack(side=tk.LEFT, anchor=tk.NE, fill=tk.Y)
        self.leader_board.configure(text=SHOW_SCORE_B,
                                    command=self.leader_boards)
        self.words_success.delete(0, tk.END)

    def countdown(self, left):
        """
        responsible for counting the time and adding the score to the score
        board. than redirecting back to the main screen
        :param left:  how much time is left
        """
        if left > 0 and self.tick is True:
            self.status_bar.configure(
                text=f"{left} seconds left, your current score is:"
                     f" {self.board.score}")
            self.root.after(1000, self.countdown, left - 1)
        elif left <= 0:
            answer = messagebox.askquestion(title=TIME_OUT_T,
                                            message=f"Game Over - "
                                                    f"you got {self.board.score} "
                                                    f"points,do you wish to "
                                                    f"register in the "
                                                    f"leaderboard?")
            if answer == "yes":
                name = askstring(LEADER_B_T, LEADER_B_TEXT)
                self.add_too_score_board(name)
                self.raise_info_screen()
            else:
                self.raise_info_screen()

    def add_too_score_board(self, name):
        """
        adds the user score to the score board
        :param name: users name
        :return: None if the user canceled and than it does not add the score
        """
        if name == "":
            name = "generic user"
        if name is None:
            return
        self.high_score.append((f"{str(name)}: ", self.board.score))

    def delete_scores(self):
        """
        after the user choses to close the main window this method clears
        the Listbox and changes the button role
        """
        self.words_success.delete(0, tk.END)
        self.leader_board.configure(text=SHOW_SCORE_B,
                                    command=self.leader_boards)

    def leader_boards(self):
        """
        shows the user all the scores from the current game session
        sorted from highest to lowest
        """
        if not self.high_score:
            messagebox.showinfo(title=SCORE_TITLE,
                                message=NO_SCORES)
            return
        self.leader_board.configure(text=HIDE_SCORES_B,
                                    command=self.delete_scores)
        sort_by_score = sorted(self.high_score, key=lambda tup: tup[1],
                               reverse=True)
        for score in sort_by_score:
            cur = "".join(map(str, score))
            self.words_success.insert(tk.END, cur)

    def run_game(self):
        """
        runs the game
        """
        self.root.mainloop()


if __name__ == '__main__':
    boggle_words_reader(FILE_NAME)
    game = Game(tk.Tk())
    game.run_game()
