# alon markovich, idan orgad
# alonmarko208
# idanorg
from os import path
import wave_helper as helper
import math

CHANGE_VALID_INPUT = ["1", "2", "3", "4", "5", "6", "7"]
MAIN_MENU_VALID_INPUT = ["1", "2", "3"]
MAX_VAL = 32767
MIN_VAL = -32768
MULTIPLY = "*"
DIVIDE = "/"
FRAME_RATE = 2000
NOTE_DICT = {"A": 440, "B": 494, "C": 523, "D": 587, "E": 659, "F": 698,
             "G": 784, "Q": 0}


def print_main_menu():
    """
    prints the main menu
    :return: None
    """
    print("********MAIN MENU*********")
    print("Please Choose One of The Following Options:")
    print("1.Change Wav File")
    print("2.Compose a Melody in a Wav File format")
    print("3.Exit the Program.")


def print_change_menu():
    """
    prints the change menu
    :return: None
    """
    print("~~~~~~~~FILE CHANGE MENU~~~~~~~~~~")
    print("Please Choose one of the following:")
    print("1.reverse audio")
    print("2.speed up audio")
    print("3.speed down audio")
    print("4.volume up")
    print("5.volume down")
    print("6.low pass filter")
    print("7.save the file and go back to the main menu")


def entry_menu():
    """
    this function presents the user with a main menu
    wich he can choose options from
    :return: the users choice (int)
    """
    print_main_menu()
    user_choice = input("enter your choice here - 1,2 or 3: ")
    while not main_menu_input_validation(user_choice):
        print("invalid choice - try again")
        user_choice = input("enter your choice here - 1,2 or 3: ")
    return int(user_choice)


def main_menu_input_validation(user_choice):
    """
    function checks if the main menu input is valid
    :param user_choice: the choice made by the user
    :return: True or False accordingly
    """
    if len(user_choice) == 1:
        if user_choice in MAIN_MENU_VALID_INPUT:
            return True
    return False


def wav_change_menu_input():
    """
     presents the user with the wav change menu if he chose to
    change it it reads from a wav_change file to print the menu
    :return: the value as integer from 1 to 7 according to his choice
    """
    print_change_menu()
    user_choice = input("enter your choice of 1 to 7: ")
    while not change_menu_validation(user_choice):
        print("invalid choice - try again")
        user_choice = input("enter your choice of 1 to 7: ")
    return int(user_choice)


def load_input_validation():
    """
    loads the wav file and validates it is loaded correctly
    :return: returns a list of frame rate and audio data as wav
    """
    filename = input("please enter the name of the file to edit: ")
    wav = helper.load_wave(filename)
    while wav == -1:
        print("there was a problem loading the file or it does not exist, "
              "try a different name")
        filename = input("please enter the name of the file to edit: ")
        wav = helper.load_wave(filename)
    return wav


def check_file_exist(filename):
    """
    function checks if the given file exists
    boolean return accordingly
    :param filename: the name of the file we check if exists
    :return: True or False accordingly
    """
    if path.exists(filename):
        return path.isfile(filename)
    return False


def change_menu_validation(user_choice):
    """
    validates the input made by the user to be correct
    :param user_choice: the users choice (str)
    :return:  True of False accordingly
    """
    if len(user_choice) == 1:
        if user_choice in CHANGE_VALID_INPUT:
            return True
    return False


def read_compose_instructions(filename):
    """
    reads the composed file and inserts each note and number into a tuple pair
    wich is part of a list
    :param filename: the name of the file we read from
    :return: list of tuple pairs str and int
    """
    with open(filename, "r") as compose:
        compose_list = create_compose_list(compose)
    compose_tuple_list = []
    for i in range(0, len(compose_list) - 1, 2):
        note_pair = (compose_list[i], int(compose_list[i + 1]))
        compose_tuple_list.append(note_pair)
    return compose_tuple_list


def create_compose_list(compose):
    """
    creates a list of strings from the compose files
    :param compose: the file we opened to read from
    :return: list of strings - each index a note and than its number of 1/16
    of a second
    """
    compose_list = []
    for line in compose:
        if line == "\n":
            continue
        line = line.strip()
        line = line.split(" ")
        compose_list.append(' '.join(line))
    compose_str = ' '.join(compose_list)
    compose_list = list(compose_str.split(" "))
    return compose_list


def save_validation(frame_rate, audio_data):
    """
    asks the user for a name to save the file and if the file is successfully
    saved it prints a message and finished its running
    :param frame_rate: for the wav file
    :param audio_data: for the wav file
    :return: None
    """
    filename = input("choose a name for the wav file: ")
    while helper.save_wave(frame_rate, audio_data, filename) == -1:
        print("there was a problem saving the file try a different name")
        filename = input("choose a name for the wav file: ")
    print("the file was saved successfully")


def wav_menu_router(user_choice, wav):
    """
    if teh user chose to change a wav file it gets his input choice and
    redirects the proper function and prints a messange that the change has
    been done
    :param wav:
    :param user_choice: number between 1 to 6
    :return:
    """
    if user_choice == 1:
        wav = reverse_audio(wav)
        print("the audio has been reversed")
        return wav
    if user_choice == 2:
        wav = speed_up(wav)
        print("the audio has been sped up")
        return wav
    if user_choice == 3:
        wav = speed_down(wav)
        print("the audio has been slowed down")
        return wav
    if user_choice == 4:
        wav = volume_up(wav)
        print("the audio volume was increased")
        return wav
    if user_choice == 5:
        wav = volume_down(wav)
        print("the audio volume has been decreased")
        return wav
    if user_choice == 6:
        wav = low_pass_filter(wav)
        print("the audio was dimmed")
        return wav


def change_menu():
    """
    goes through the proccess of editing a wav file from start to end
    and saves the file, redirects back to the main menu
    :return: None
    """
    choice = 0
    wav = load_input_validation()
    while choice != 7:
        choice = wav_change_menu_input()
        if choice == 7:
            frame_rate, audio_data = divide_wav(wav)
            save_validation(frame_rate, audio_data)
            break
        wav = wav_menu_router(choice, wav)


def divide_wav(wav):
    """
    take wav and divide it to 2 values
    :param wav: list of list of list
    :return: frame_rate(int type) , data_list (list of list type)
    """
    return wav[0], wav[1]


def make_music_input():
    """
    asks the user for a name to the instructions list
    checks if exists and returns that name
    :return: filename - string
    """
    filename = input("enter the instructions file name: ")
    while not check_file_exist(filename):
        print("file not found - enter a different name")
        filename = input("enter the instructions file name: ")
    return filename


def check_only_one_item(data_lst):
    """
    check if data lst has only 1 item
    :param data_lst: from wav
    :return: True if yes
    """
    if len(data_lst) == 1:
        return True
    else:
        return False


def reverse_audio(wav):
    """
    take wav value and reverse the date_list
    :param wav:
    :return: wav with reversed data list
    """
    lst_of_reversed_audio = wav[1][::-1]
    reversed_wav = [wav[0], lst_of_reversed_audio]
    return reversed_wav


def speed_up(wav):
    """
    take from data list only the even items
    :param wav:
    :return: new wav after that change
    """
    data_lst = wav[1]
    if check_only_one_item(data_lst):
        return wav
    wav_speed_up = [wav[0], data_lst[::2]]
    return wav_speed_up


def calculate_average(*values):
    """
    calculate avg like calculator ;)
    :param values: take unknown number of arguments ("*")
    :return: int of the average number
    """
    count = len(values)
    sum_values = sum(values)
    avg = float(sum_values / count)  # for complex numbers like -111.139
    return int(avg)


def insert_average_item(data_lst, index):
    """
    put average item between the 2 items its calculate
    :param data_lst: from wav
    :param index: incdex for for loop
    :return: list of 2 values
    """
    average_value = []
    first_original_item = data_lst[index]
    second_original_item = data_lst[index + 1]
    average_value.append(
        calculate_average(first_original_item[0], second_original_item[0]))
    average_value.append(
        calculate_average(first_original_item[1], second_original_item[1]))
    return average_value


def speed_down(wav):
    """
    take data list and insert item of average between 2 items in the
     original list
    :param wav: data list
    :return: new data list with average values
    """
    data_lst = wav[1]
    if check_only_one_item(data_lst):
        return wav
    new_data_lst = []
    last_item_index = len(data_lst) - 1
    for i in range(len(data_lst)):
        if i == last_item_index:
            new_data_lst.append(data_lst[i])
            break
        new_data_lst.append(data_lst[i])
        new_data_lst.append(insert_average_item(data_lst, i))
    wav_with_average = [wav[0], new_data_lst]
    return wav_with_average


def put_num_in_range(number, sign):
    """
    change the number between min val to max val after multiply or division
    :param number: number from data_lst
    :param sign: * or /
    :return: new number (int type)
    """
    new_number = number
    if sign == MULTIPLY:
        new_number = number * 1.2
    if sign == DIVIDE:
        new_number = number / 1.2
    if new_number > MAX_VAL:
        return MAX_VAL
    elif new_number < MIN_VAL:
        return MIN_VAL
    return int(new_number)


def volume_up(wav):
    """
    multiply the 2 values of data list item
    :param wav:
    :return: new wav after the change
    """
    data_lst = wav[1]
    for item in data_lst:
        item[0] = put_num_in_range(item[0], MULTIPLY)
        item[1] = put_num_in_range(item[1], MULTIPLY)
    return wav


def volume_down(wav):
    """
        divide the 2 values of data list item
        :param wav:
        :return: new wav after the change
    """
    data_lst = wav[1]
    for item in data_lst:
        item[0] = put_num_in_range(item[0], DIVIDE)
        item[1] = put_num_in_range(item[1], DIVIDE)
    return wav


def append_first_average(average_lst, data_lst, average_item):
    """
    only in first loop
    :param average_lst: the list I want to insert in
    :param data_lst: from wav
    :param average_item: empty list []
    :return:
    """
    average_item.append(calculate_average(data_lst[0][0], data_lst[1][0]))
    average_item.append(calculate_average(data_lst[0][1], data_lst[1][1]))
    average_lst.append(average_item)
    return average_lst


def append_last_average(average_lst, data_lst, average_item):
    """
    only in last loop
    :param average_lst: the list I want to insert in
    :param data_lst: from wav
    :param average_item: empty list []
    :return:
    """
    average_item.append(
        calculate_average(data_lst[-1][0], data_lst[-2][0]))
    average_item.append(
        calculate_average(data_lst[-1][1], data_lst[-2][1]))
    average_lst.append(average_item)
    return average_lst


def append_mid_average(average_lst, data_lst, average_item, i):
    """
    occours in most of the loops. append average item
    :param average_lst: the list I want to insert in
    :param data_lst: from wav
    :param average_item: empty list []
    :param i: the index in the loop i run
    :return:
    """
    average_item.append(
        calculate_average(data_lst[i - 1][0], data_lst[i][0],
                          data_lst[i + 1][0]))
    average_item.append(
        calculate_average(data_lst[i - 1][1], data_lst[i][1],
                          data_lst[i + 1][1]))
    average_lst.append(average_item)
    return average_lst


def change_to_average(wav):
    """
    take lst and make new list with average between all 2 values
    :param wav:  from wav
    :return: new average list
    """
    data_lst = wav[1]
    if check_only_one_item(data_lst):
        return wav
    last_item_index = len(data_lst) - 1
    average_lst = []
    average_wav = [wav[0], average_lst]
    average_item = []
    if len(data_lst) == 2:
        append_first_average(average_lst, data_lst, average_item)
        return average_wav
    for i in (range(len(data_lst))):
        average_item = []
        if i == 0:  # first item
            append_first_average(average_lst, data_lst, average_item)
        elif i == last_item_index:
            append_last_average(average_lst, data_lst, average_item)
        else:
            append_mid_average(average_lst, data_lst, average_item, i)
    return average_wav


def low_pass_filter(wav):
    """
    takes wav and changes the audio data to its
    averages
    :param wav: frame rate and audio data
    :return: the wav after the change of the audio data
    """
    return change_to_average(wav)


def find_frequency(letter):
    """
    take letter  and return value of frequency
    :param letter: A to G or Q
    :return: int value
    """
    for key in NOTE_DICT.keys():
        if key == letter:
            return NOTE_DICT[key]


def create_sample_lst_quiet(quantity_samples):
    """
    creates a list of [0,0] n times for a quiet note
    :param quantity_samples: int type - the duration on the note in frame
    rates
    :return: the new list of lists made of zeroes
    """
    val = 0
    lst_of_samples = []
    for i in range(quantity_samples):
        lst_of_samples.append([val] * 2)
    return lst_of_samples


def create_val(index, samples_per_cycle):
    val = MAX_VAL * math.sin(
        math.pi * 2 * (index / samples_per_cycle))  # calculation from ex
    val = int(val)  # round it to  int
    return val


def insert_samples(tuple_of_sound):
    """
    take one tuple and make list of samples.
    :param tuple_of_sound: (letter,int duration)
    :return: lst of list of samples for example [[1,1],[14,14] ...]
    """
    lst_of_sample = []
    letter = tuple_of_sound[0]  # define letter
    duration = tuple_of_sound[1]  # define duration
    quantity_of_samples = int(
        FRAME_RATE / (16 / duration))  # calculation from ex
    frequency = find_frequency(letter)  # call function
    if frequency == NOTE_DICT["Q"]:
        return create_sample_lst_quiet(quantity_of_samples)
    samples_per_cycle = FRAME_RATE / frequency  # calculation from ex
    for i in range(quantity_of_samples):
        val = create_val(i, samples_per_cycle)
        lst_of_sample.append(
            [
                val] * 2)  # make 2 same vals in lst. it add for example: [2,2]
    return lst_of_sample


def create_music_data(lst_of_tuples):
    """
    take lst of tuples and make "insert sample" function  i times like len of
     tuples lst.
    :param lst_of_tuples:  [(A,1),(c,16) ...]
    :return: lst of samples
    """
    sum_of_samples = []
    for item in lst_of_tuples:
        sum_of_samples += insert_samples(item)
    return sum_of_samples


def make_new_music():
    """
    gets the instructions file name - creates the music file and redirects the
    the user to teh change menu for that files specificly and after that saves
    it
    :return: None
    """
    filename = make_music_input()
    notes_list = read_compose_instructions(filename)
    audio_data = create_music_data(notes_list)
    wav = [FRAME_RATE, audio_data]
    choice = wav_change_menu_input()
    while choice != 7:
        wav = wav_menu_router(choice, wav)
        choice = wav_change_menu_input()
    save_validation(FRAME_RATE, audio_data)


def music_mixer():
    """
    the main function - calls all the other functions
    gets user input and creates or edits wav files accordingly
    :return: None
    """
    choice = entry_menu()
    while choice != 3:
        if choice == 1:
            change_menu()
        if choice == 2:
            make_new_music()
        choice = entry_menu()
    print("thank you so much for using our program")


if __name__ == '__main__':
    music_mixer()
