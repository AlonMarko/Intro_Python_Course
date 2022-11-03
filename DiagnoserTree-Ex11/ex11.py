# 313454902
# alonmarko208
# alon markovich
import copy
import itertools


class Node:
    """
    node class - has data and next children
    """

    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def get_positive(self):
        """
        :return: positive node
        """
        return self.positive_child

    def get_negative(self):
        """
        :return: negative node
        """
        return self.negative_child

    def get_value(self):
        """
        :return: node data
        """
        return self.data


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms

    def get_illness(self):
        """
        :return: string
        """
        return self.illness

    def get_symptoms(self):
        """
        :return: list of strings
        """
        return self.symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose(self, symptoms):
        """
        goes over a tree in recursion to detect wich disease it is
        from the root
        :param symptoms: list of symptoms
        :return: the disease
        """
        return self.diagnose_helper(symptoms, self.root)

    def diagnose_helper(self, symptoms, node):
        """
        recursive function that gets a tree(node object) and uses recursion
        to return the desiease related to the sympomts
        :param node: node object
        :param symptoms: list of str
        :return: str - the name of the disease
        """
        if node.get_positive() is None and node.get_negative() is None:
            return node.get_value()
        if node.get_value() in symptoms:
            return self.diagnose_helper(symptoms, node.get_positive())
        else:
            return self.diagnose_helper(symptoms, node.get_negative())

    def calculate_success_rate(self, records):
        """
        checks how many good diagnoses have been done on a list of records
        (illness and sympomts)
        :param records: list of Record object
        :return: the rate of success - number from 0 -0% to 1 - 100%
        """
        successes = 0
        for record in records:
            illness = self.diagnose(record.get_symptoms())
            if illness == record.get_illness():
                successes += 1
        return successes / len(records)

    def all_illnesses(self):
        """
        runs over the tree and returns a list of all the diseases in it, in
        decreasing order - from most common to the rarest
        :return: a list of strings
        """
        pre_sort = []
        self.all_illnesses_helper(pre_sort, self.root)
        ill_dict = {i: pre_sort.count(i) for i in pre_sort}
        post_sort = sorted(ill_dict, key=ill_dict.get)
        post_sort = post_sort[::-1]
        return post_sort

    def all_illnesses_helper(self, illness_list, tree_root):
        """
        helper function for all_illnesses method
        :param tree_root: Node object
        :param illness_list: an empty list
        :return: None, changes the empty list to contain all the leaf values
        """
        if tree_root.get_positive() is None and tree_root.get_negative() is None:
            if tree_root.get_value() is not None:
                illness_list.append(tree_root.get_value())
            return
        self.all_illnesses_helper(illness_list, tree_root.get_positive())
        self.all_illnesses_helper(illness_list, tree_root.get_negative())

    def paths_to_illness(self, illness):
        """
        gets an illness and runs over the tree to get all the
        paths that lead to that illness
        :param illness: String
        :return: list of lists
        """
        paths = []
        self.paths_to_helper(self.root, paths, illness)
        return paths

    def paths_to_helper(self, tree_root, paths, illness, path=()):
        """
        helper function to paths_to_illness
        recursivly adds possible routes to a list
        :param tree_root: Node object
        :param paths: list of path lists
        :param illness: the illness we seek a path to (str)
        :param path: a changing list - representing a path
        :return: None
        """
        if tree_root.get_positive() is None and tree_root.get_negative() is None:
            if tree_root.get_value() == illness:
                path_lst = list(path)
                paths.append(path_lst)
            return
        path = path + (True,)
        self.paths_to_helper(tree_root.get_positive(), paths, illness, path)
        path = path[:-1]
        path = path + (False,)
        self.paths_to_helper(tree_root.get_negative(), paths, illness, path)


def insert(temp, key):
    """
    inserts a node with no children as a leaf in the first
    available spot
    :param temp: node
    :param key: value
    :return:
    """
    node_iterator = list()
    node_iterator.append(temp)
    while len(node_iterator):
        temp = node_iterator[0]
        node_iterator.pop(0)
        if not temp.get_positive():
            temp.positive_child = Node(key)
            break
        else:
            node_iterator.append(temp.get_positive())
        if not temp.get_negative():
            temp.negative_child = Node(key)
            break
        else:
            node_iterator.append(temp.get_negative())


def build_tree(records, symptoms):
    """
    build a tree
    :param records: list of record objects
    :param symptoms: list of strings
    :return: tree root
    """
    if len(symptoms) == 0 and len(records) >= 0:
        root = special_cases(records)
        return root
    root = Node(symptoms[0])
    symptoms_list = symptoms[1:]
    build_tree_helper(root, symptoms_list)
    diagnoser = Diagnoser(root)
    paths = diagnoser.paths_to_illness(symptoms[len(symptoms) - 1])
    paths_copy = copy.deepcopy(paths)
    new_paths = []
    make_double_paths(new_paths, paths, paths_copy)
    add_illnesses(new_paths, records, root, symptoms)
    return root


def add_illnesses(new_paths, records, root, symptoms):
    """
    checks which illness needs to be added and adds it
    """
    for path in new_paths:
        if len(records) == 0:
            insert(root, None)
            continue
        current_list = []
        forbidden_list = []
        create_related_lists(current_list, forbidden_list, path, symptoms)
        illness_list = []
        record_iteration(current_list, forbidden_list, illness_list, records)
        post_sort = sorter(illness_list)
        if not post_sort:
            value = None
        else:
            value = post_sort[0]
        insert(root, value)


def record_iteration(current_list, forbidden_list, illness_list, records):
    """
    adds diseases to a list that are compatible with the path
    """
    for record in records:
        flag_forbidden = 0
        for symptom in forbidden_list:
            if symptom in record.get_symptoms():
                flag_forbidden = 1
                break
        if flag_forbidden == 1:
            continue
        result = set(x in record.get_symptoms() for x in current_list)
        flag = 0
        for answer in result:
            if not answer:
                flag = 1
        if flag == 0:
            illness_list.append(record.get_illness())
        else:
            continue


def create_related_lists(current_list, forbidden_list, path, symptoms):
    """
    creates forbbiden lists and illness lists
    """
    for index, value in enumerate(path):
        if value is True:
            current_list.append(symptoms[index])
            continue
        if value is False:
            forbidden_list.append(symptoms[index])


def sorter(illness_list):
    ill_dict = {i: illness_list.count(i) for i in illness_list}
    post_sort = sorted(ill_dict, key=ill_dict.get)
    post_sort = post_sort[::-1]
    return post_sort


def make_double_paths(new_paths, paths, paths_copy):
    """
    doubles the paths and adds true or false accordingly
    """
    for current_index, current_path in enumerate(paths):
        new_paths.append(current_path)
        new_paths.append(paths_copy[current_index])
    for i in range(0, len(new_paths) - 1, 2):
        new_paths[i].append(True)
        new_paths[i + 1].append(False)


def special_cases(records):
    """
    checks special cases in the build tree function
    """
    illnessess = []
    for record in records:
        if not record.get_symptoms():
            illnessess.append(record.get_illness())
    ill_dict = {i: illnessess.count(i) for i in illnessess}
    post_sort = sorted(ill_dict, key=ill_dict.get)
    post_sort = post_sort[::-1]
    if not post_sort:
        value = None
    else:
        value = post_sort[0]
    root = Node(value)
    return root


def build_tree_helper(root, symptoms, i=0):
    """
    build a tree recursivly
    :param root:
    :param symptoms:
    :param i:
    :return:
    """
    if root is None:
        return
    if i == len(symptoms):
        return
    if root.get_positive() is None and root.get_negative() is None:
        root.positive_child = Node(symptoms[i])
        root.negative_child = Node(symptoms[i])
    build_tree_helper(root.get_positive(), symptoms, i + 1)
    build_tree_helper(root.get_negative(), symptoms, i + 1)


def optimal_tree(records, symptoms, depth):
    """
    checks for the highest success rate tree and returns it
    """
    options_temp = itertools.combinations(symptoms, depth)
    options_normal = list(options_temp)
    options_final = []
    for i in range(len(options_normal)):
        options_final.append(list(options_normal[i]))
    best_tree = None
    current_rate = -1
    for option in options_normal:
        tree = build_tree(records, option)
        diagnoser = Diagnoser(tree)
        rate = diagnoser.calculate_success_rate(records)
        if rate > current_rate:
            if rate == 1:
                return tree
            current_rate = rate
            best_tree = tree
    return best_tree
