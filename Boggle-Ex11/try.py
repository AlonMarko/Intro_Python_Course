"""import functools
import time
import itertools


def cartesean_product(lst):
    if len(lst) == 0:
        return [""]
    return helper(lst, [], 0, "")


def helper(lst, sol, idx, word):
    if idx == len(lst):
        sol.append(word)
    else:
        for i in range(len(lst[idx])):
            helper(lst, sol, idx + 1, word + lst[idx][i])
    return sol


def diff_iter(some_iter):
    lst = []
    prev = next(some_iter)
    for num in some_iter:
        lst.append(num - prev)
        prev = num
    return iter(lst)


class TreeNode:
    def __init__(self, children, data):
        self.children = set(children)
        self.data = data


def find_duplicate(root):
    nodes_list = []
    return find_duplicate_helper(root, nodes_list)


def find_duplicate_helper(root, nodes_list):
    if not root.children:
        return
    for child in root.children:
        if child in nodes_list:
            return child
        else:
            nodes_list.append(child)
            find_duplicate_helper(child, nodes_list)


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def is_repetative(self, lst):
        cur = self.__head
        while cur != None:
            index = 0
            for i in lst:
                index += 1
                if cur.data == i:
                    cur = cur.next
                else:
                    return False
            if index != 0:
                return False
            return True


def find_discontinuity(lst):
    mid = len(lst) // 2
    mid2 = len(lst) // 2
    while True:
        if lst[mid] > lst[mid + 1]:
            return mid
        if lst[mid2] > lst[mid2 + 1]:
            return mid2
        mid2 = (mid + len(lst)) // 2
        mid = mid // 2


class Range2D:
    def __init__(self, x, y):
        self.max_x = x
        self.max_y = y
        self.local_x = 0
        self.local_y = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.local_x >= self.max_x and self.local_y >= self.local_y:
            raise StopIteration
        while True:
            cur = (self.local_x, self.local_y)
            self.local_y += 1
            if self.local_y == self.max_y:
                self.local_y = 0
                self.local_x += 1
            return cur

    def contains(self, item):
        if item.max_x > self.max_x or item.max_y > self.max_y:
            return False
        return True


def most_common(lst):
    common_d = dict()
    for i in lst:
        if i in common_d:
            common_d[i] = common_d.get(i) + 1
        else:
            common_d[i] = 1
    common = common_d.items()
    common = sorted(common, key=lambda tup: tup[1], reverse=True)
    return common[0][0]


def match(team1, team2):
    total = 0
    for player in team1:
        counter = 0
        for player2 in team2:
            if player > player2:
                counter += 1
                continue
            break
        total += counter
    return total


def contain_all_of(items, world):
    return contain_helper(items, world, True)


def contain_helper(items, world, flag, idx=0):
    if idx == len(items) and flag == True:
        return True
    if not flag:
        return False
    if items[idx] in world:
        return contain_helper(items, world, True, idx + 1)
    else:
        return False


def brute_search(word, text, num):
    found = 0
    starti = 0
    while starti < len(text):
        count = 0
        i = starti
        for letter in word:
            if letter == text[i]:
                i += 1
                count += 1
        if count == len(word):
            starti = i + 1
            found += 1
        else:
            starti += 1
        if found >= num:
            return True
    return False


def iterable_to_func(iterable):
    def inner(index):
        iterator = iter(iterable)
        for k in range(index - 1):
            next(iterator)
        return next(iterator)

    return inner


def foor(a, l=[]):
    for i in a:
        l.append(i)
    return l


def f(m):
    k = 1
    while True:
        if (pow(2, k + 1) - 2 < m):
            k += 1
        else:
            break
    n = m - (pow(2, k) - 2)
    while k > 0:
        num = pow(2, k - 1)
        if (num >= n):
            print("A", end="")
        else:
            print("b", end="")
            n -= num
        k -= 1


class Library:
    def __init__(self):
        self.stock = dict()
        self.borrowed = []

    def add_bood_copy(self, book_name):
        if book_name in self.stock:
            self.stock[book_name] += 1
        else:
            self.stock[book_name] = 1

    def borrow_one_book(self, book_name):
        try:
            self.stock[book_name] -= 1
            self.borrowed.append(book_name)
            if self.stock[book_name] == 0:
                del (self.stock[book_name])
        except:
            raise ValueError

    def return_one_book(self, book_name):
        if book_name in self.borrowed:
            self.add_bood_copy(book_name)
            self.borrowed.remove(book_name)
        else:
            raise ValueError

    def get_num_copis(self, book_name):
        if book_name in self.stock:
            return self.stock[book_name]
        else:
            return 0
"""


def merge(a, b):
    inda = 0
    indb = 0
    c = []
    while (inda < len(a) and indb < len(b)):
        if a[inda] <= b[indb]:
            c.append(a[inda])
            inda += 1
        else:
            c.append(b[indb])
            indb += 1
    if inda < len(a):
        c += a[inda:]
        return c
    else:
        c += b[indb:]
        return c


def merge_sort(a):
    if len(a) == 1:
        return a
    left = merge_sort(a[:len(a) // 2])
    right = merge_sort((a[len(a) // 2:]))
    return merge(left, right)


lst = []


listb = [11, 12, 13, 14, 3193094]
print(merge(lst, listb))
