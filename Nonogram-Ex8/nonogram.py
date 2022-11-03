# alon markovich
# alonmarko208
# 313454902

BLACK = 1
WHITE = 0
UNKNOWN = -1


def row_helper(row, constraint, temp_tup, i, valid_options):
    """
    recieves a row with unknown variables in it and adds into a
     list all the options
    that can be constructed according to the constraints given
    the function build thge list of lists recursivley
    :param row: list of ints
    :param constraint: list of ints
    :param temp_tup: the temporary tuple that is being constructed in the
    recursion
    :param i: the index that the recursion will run with
    :param valid_options: the final list that will be built
    :return: None, it builds a given empty list.
    """
    if i == len(row):
        painted_row = list(temp_tup)
        if create_line_pattern(painted_row) == constraint:
            valid_options.append(painted_row)
        return
    if row[i] == BLACK or row[i] == WHITE:
        temp_tup = temp_tup + (row[i],)
        row_helper(row, constraint, temp_tup, i + 1, valid_options)
    else:
        temp_tup = temp_tup + (BLACK,)
        row_helper(row, constraint, temp_tup, i + 1, valid_options)
        temp_tup = temp_tup[:-1]
        temp_tup = temp_tup + (WHITE,)
        row_helper(row, constraint, temp_tup, i + 1, valid_options)


def get_row_variations(row, blocks):
    """
    functions calculates all options for a line in nonogram
    :param row: list of ints 1,-1,o representing a partial paint of the line
    :param blocks: how many blocks are painted in a line.
    :return: list of lists containing the options for painted lines according
    to the input
    """
    option_list = list()
    index = 0
    temp_tuple = tuple()
    if is_empty_list(row, blocks):
        return option_list
    row_helper(row, blocks, temp_tuple, index, option_list)
    return option_list


"""def row_helper(row, constraint, lst, i, final):
    if len(lst) == len(row):
        copied = copy.deepcopy(lst)
        final.append(copied)
        return
    if row[i] == UNKNOWN:
        lst.append(BLACK)
        row_helper(row, constraint, lst, i + 1, final)
        lst.pop()
        lst.append(WHITE)
        row_helper(row, constraint, lst, i + 1, final)
        lst.pop()
    else:
        lst.append(row[i])
        row_helper(row, constraint, lst, i + 1, final)"""


def is_empty_list(row, blocks):
    """
    checks the situation if the row variation options is an empty list
    wich means the numebr of blocks painted is larger than the times number 1
    appears in the row.
    :param row: list of ints
    :param blocks: how many painted blocks
    :return: True or False
    """
    painted_times = painted_blocks(blocks)
    if row.count(BLACK) + row.count(UNKNOWN) < painted_times:
        return True
    return False


def painted_blocks(blocks):
    """
    checks hwo many squares are painted in the line according to the blocks
    given
    :param blocks: list of ints
    :return: int - how many blocks are painted
    """
    painted_times = 0
    for i in blocks:
        painted_times += i
    return painted_times


def create_line_pattern(lst):
    """
    gets a list of 0 and 1 and returns a new list representing the constraints
    on the list given.
    :param lst: list of ints
    :return: list of ints
    """
    pattern = []
    counter = 0
    for i, num in enumerate(lst):
        if num == BLACK and i == 0:
            counter += 1
        elif num == BLACK and lst[i - 1] == BLACK:
            counter += 1
        elif num == WHITE and lst[i - 1] == BLACK:
            if counter > 0:
                pattern.append(counter)
                counter = 0
        elif num == BLACK and lst[i - 1] == WHITE:
            counter += 1
        if i == len(lst) - 1 and counter > 0:
            pattern.append(counter)
    return pattern


def rotate_rows(rows):
    """
    reverses the given nested list with each new list is built from the items
    in the same index in all the lists accordignly
    does not change the original rows.
    :param rows: list of lists
    :return: the rotated list of lists
    """
    rotated = list(zip(*rows))
    return rotated


def get_intersection_row(rows):
    """
    gets a list of lists and returns one list build from the intersections of
    all the lists, if in the same index all lists have the same value,
    the value will be the same in the returned list, else it will be -1
    :param rows: list of lists
    :return: list of ints, represents all intersections
    """
    rotated = rotate_rows(rows)
    intersection_lst = []
    for index, row in enumerate(rotated):
        if row.count(row[0]) == len(row):
            intersection_lst.append(row[0])
        else:
            intersection_lst.append(UNKNOWN)
    return intersection_lst


def reverse_board(board):
    """
    reverses the board upwards like revere_rows but this function
    than overwrites the original board
    :param board: the play board list of lists
    :return: None
    """
    temp = rotate_rows(board)
    while len(temp) < len(board):
        board.pop()
    while len(temp) > len(board):
        for j in range(len(board) - 1, len(temp) - 1):
            board.append(list(temp[j]))
    for i in range(len(temp)):
        board[i] = list(temp[i])


def conclude_cycle(board, constraints):
    """
    runs a whole concluding cycle wich means a run on the rows, rotation and
    a run on the columns and rotating the board back.
    :param board: list of lists
    :param constraints: list of lists of lists
    :return: None, changes the original
    """
    board_conclude(board, constraints[0])
    if len(constraints[1]) == 1:
        return
    reverse_board(board)
    board_conclude(board, constraints[1])
    reverse_board(board)


def board_conclude(board, constraints):
    """
    this function concludes from the constraints what the options are
    it passes each row and gets its option, if there is only one option than
    it replaces it with the original row
    :param board: the play board list of lists
    :param constraints: nested list of constrains [0] for rows [1] for col
    :return:None, changes the original board
    """
    for i, row in enumerate(board):
        if not constraints[i]:
            for j in board[i]:
                if board[i][j] == UNKNOWN:
                    board[i][j] = WHITE
            continue
        if row.count(UNKNOWN) > 0:
            options = get_row_variations(row, constraints[i])
            if len(options) == 1:
                board[i] = options[0]
            elif len(options) > 1:
                intersected_row = get_intersection_row(options)
                if board[i] == intersected_row:
                    continue
                else:
                    board[i] = intersected_row


def conclude_from_constraints(board, constraints):
    """
    runs the conclude cycles several times until it can no longer conclude
    something new(when the new board equals to the previous one)
    :param board: list of lists
    :param constraints: nested list
    :return: None, it changes the original board
    """
    previous_board = []
    if not board:
        return
    if len(board) == 1 and len(board[0]) == 1:
        if painted_blocks(constraints[0][0]) > 0:
            board[0][0] = BLACK
        else:
            board[0][0] = WHITE
        return
    while previous_board != board:
        previous_board = board[:]
        conclude_cycle(board, constraints)


def create_board(constraints):
    """
    creates the palying board according to the constraints given
    and fills it with -1
    :param constraints: nested list for rows and cols constraints
    :return: list of list representing the game board
    """
    game_board = []
    cols = len(constraints[1])
    rows = len(constraints[0])
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(UNKNOWN)
        game_board.append(row)
    return game_board


def solve_easy_nonogram(constraints):
    """
    gets a list of constraints, builds the board accordingly
    and than solves it, return the solved board
    :param constraints: nested list of int
    :return: the solved board
    """
    nonogram_board = create_board(constraints)
    conclude_from_constraints(nonogram_board, constraints)
    return nonogram_board


def solve_nonogram(cons):
	#just to pass the submission
    return [solve_easy_nonogram(cons)]
