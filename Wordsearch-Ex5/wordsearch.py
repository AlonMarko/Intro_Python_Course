# alon markovich
# alonmarko208
# 313454902
from os import path
import sys

# direction list is global and does not change
DIRECTION_LIST = ["x", "y", "z", "w", "r", "l", "u", "d"]


def check_input_args(parameters):
    """
    checks if the arguments we get for the function are correct
    :param parameters: list of 4 strings that represent the parameters for
     the function
    :return: a message that represents the error or None otherwise
    """
    if len(parameters) == 4:  # checks if given enough parameters
        if parameters[2] == "":
            return "the written file name is empty"
        for i in range(len(parameters) - 2):  # if the files exist
            if not path.exists(parameters[i]):
                return "one of the files needed does not exist"
            else:
                if path.isdir(parameters[i]):  # if its not a file but a folder
                    return "one of the files needed does not exist"
        for j in parameters[3]:  # checks if the directions are legal
            if j not in DIRECTION_LIST:
                return "incorrect direction inserted"
    else:
        return "expected 4 parameters, got a different number"


def read_wordlist_file(filename):
    """
    recieves a file of words
    :param filename: a file that can or cannot contain words
    :return: a list of words that appear in the file
    """
    words_list = []
    with open(filename, 'r') as words:
        for line in words:  # passes each line in the file
            line = line.strip()  # gets rid of the /n in end of each line
            words_list.append(line)
    return words_list


def read_matrix_file(filename):
    """
    function opens a file representing the matrix
    :param filename: the matrix text file
    :return: a list of lists that represents the matrix - each inner list is
    a row, all rows are to be in the same length
    """
    matrix_list = []
    with open(filename, 'r') as matrix:
        for line in matrix:
            current_lst = []
            line = line.strip()  # gets rid of the /n
            line = line.split(',')  # gets rid of the ","
            for letter in line:  # creates the inner list
                current_lst.append(letter)
            matrix_list.append(current_lst)
        return matrix_list


def matrix_convert(matrix):
    """
    converts the list of letter lists into list of strings
    :param matrix: the matrix to convert - a two dimensional list
    :return: a list of strings representing the matrix
    """
    string_list = []
    for i in range(len(matrix)):
        matrix_line = ""
        for letter in matrix[i]:
            matrix_line += letter
        string_list.append(matrix_line)
    return string_list


def reverse_matrix(matrix):
    """
    :param matrix: two dimensional list
    :return: matrix reversed as list of lists
    """
    reversed_matrix = []
    for i in range(len(matrix)):
        line = []
        for j in range(len(matrix[i]) - 1, -1, -1):
            line.append(matrix[i][j])  # goes through the word in reverse
        reversed_matrix.append(line)
    return reversed_matrix


def upwards_matrix(matrix):
    """
    turns the matrix into a new one where it is built upwards - each column
    becomes the new line from the bottom
    :param matrix: a regular matrix made of list of lists
    :return: list of lists upwards
    """
    up_matrix = list(zip(*matrix[::-1]))  # turning it into columns with zip
    return up_matrix


def downwards_matrix(matrix):
    """
    turns the matrix into a new one where it is build downwards - each column
    becomes a row
    :param matrix: the matrix as a list of lists
    :return: a two dimensional list that is reversed
    """
    down_matrix = list(zip(*matrix))  # turning it into columns with zip
    return down_matrix


def matrix_search(word_list, matrix):
    """
    searches the matrix horizontaly and verticaly or diagonaliy
    (according to the matrix given it does the same search from
    left to right but the matrix type fits the direction
    :param word_list: the list to search words from
    :param matrix: the matrix itself as a list of strings
    :return: a dictionary containing the word and number of times it appears
    if it is  1 or more
    """
    found_words = {}
    for word in word_list:
        word_count = 0
        len_word = len(word)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j:j + len_word] == word:
                    word_count += 1
        if word_count > 0:
            found_words[word] = word_count
    return found_words


def diagonal_matrix(matrix):
    """
    :param matrix: a matrix to return its diagonals
    :return: a new matrix build by its diagonals in the w direction
    """
    diag_matrix = []
    if len(matrix) == 0:
        return diag_matrix
    rows = len(matrix)
    columns = len(matrix[0])
    diagonal_number = rows + columns - 1

    for diag_index in range(diagonal_number):
        one_diagonal = []
        for i in range(diag_index + 1):
            if (diag_index - i) < rows and i < columns:
                one_diagonal.append(matrix[diag_index - i][i])
        diag_matrix.append(one_diagonal)
    return diag_matrix


def relevant_matrix(direction, matrix):
    """
    gets the matrix and a search direction and returns the relavent matrix
    for a search as a list of strings.
    :param direction: the current direction search
    :param matrix: the matrix
    :return: the relevant matrix as a list of strings ready to be searched
    """
    if direction == "r":
        return matrix_convert(matrix)
    elif direction == "l":
        return matrix_convert(reverse_matrix(matrix))
    elif direction == "u":
        return matrix_convert(upwards_matrix(matrix))
    elif direction == "d":
        return matrix_convert(downwards_matrix(matrix))
    elif direction == "w":
        return matrix_convert(diagonal_matrix(matrix))
    elif direction == "x":
        return matrix_convert(diagonal_matrix(reverse_matrix(matrix)))
    elif direction == "z":
        return matrix_convert(diagonal_matrix(downwards_matrix(matrix)))
    elif direction == "y":
        temp_matrix = diagonal_matrix(downwards_matrix(reverse_matrix(matrix)))
        return matrix_convert(temp_matrix)


def merge_dictionaries(dictionary_one, dictionary_two):
    """
    gets two dicts and merges them
    :param dictionary_one: the main one
    :param dictionary_two: the current one from the current search
    :return: a merged dictionary of both of them
    """
    merged_dictionary = {}
    for key in dictionary_one:
        if key in dictionary_two:
            new_value = dictionary_one[key] + dictionary_two[key]
        else:
            new_value = dictionary_one[key]
        merged_dictionary[key] = new_value
    for key in dictionary_two:
        if key not in merged_dictionary:
            merged_dictionary[key] = dictionary_two[key]
    return merged_dictionary


def find_words_in_matrix(word_list, matrix, directions):
    """
    the function searches the matrix for the gives words according to the
    search directions
    :param word_list: a list of words to search
    :param matrix: a list representing the matrix to be searched in
    :param directions: a string of letters that represent the search
    direction
    :return: a list of pair - a word and how many times it appears string and
    int
    """
    existing_dict = {}
    existing_list = []
    for direction in directions:
        ready_matrix = relevant_matrix(direction, matrix)
        found_words = matrix_search(word_list, ready_matrix)
        existing_dict = merge_dictionaries(existing_dict, found_words)
    for key in existing_dict:
        current_item = (key, existing_dict[key])
        existing_list.append(current_item)
    return existing_list


def write_output_file(results, output_filename):
    """
    function creates a file wich name is given as a string and will write in
    it the search results
    :param results: the list of pairs of search results
    :param output_filename: the given name according to the search parameter
    :return:
    """
    output = open(output_filename, "w")
    for result in results:
        word = result[0]
        count = str(result[1])
        line = word + "," + count
        output.write(line)
        output.write("\n")
    output.close()


def direction_convert(directions):
    """
    converts the direction string into a one time string
    if a letter is inside twice than it will appear once
    :param directions: direction string
    :return: signle show string
    """
    direction_list = list(directions)
    direction_set = set(direction_list)
    direction_string = ''.join(direction_set)
    return direction_string


def matrix_complete(arguments):
    """
    this function combines all - gets the file names, opens the new file
    and runs through the entire matrix in order to find the words accoring to
    the direction given
    :param arguments: list of 4 aruments - file names and directions - strings
    :return: None
    """
    if check_input_args(arguments) is None:
        word_list = read_wordlist_file(arguments[0])
        matrix = read_matrix_file(arguments[1])
        directions = direction_convert(arguments[3])
        results = find_words_in_matrix(word_list, matrix, directions)
        write_output_file(results, arguments[2])
    else:
        msg = check_input_args(arguments)
        print(msg)


if __name__ == '__main__':
    args = sys.argv
    matrix_complete(args[1:])
