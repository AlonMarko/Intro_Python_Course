"""def get_even_func():
    def bigger(n):
        if n % 2 == 0:
            return True
        else:
            return False

    return bigger


def minus_one_func():
    def minus_one(num):
        num -= 1
        return num

    return minus_one


def my_pow(x):
    def my_pow_(*args):
        return x(*args)

    return my_pow_


my_pow = my_pow(lambda x: lambda y: x ** y)

from functools import reduce


def count_appearances1(letter, word):
    fun = lambda x, y: word.count(letter)
    return reduce(fun, word, 0)


def count_appearances2(letter, word):
    fun = lambda x: x == letter
    return sum(map(fun, word))


def count_appearances3(letter, word):
    fun = lambda x: x == letter
    return len(list(filter(fun, word)))


global last
last = []


def last_in(x):
    def wrapper(*args):
        if not last:
            last.append(*args)
            return
        else:
            lastin = last[-1]
            last.append(*args)
            return lastin

    return wrapper(x)


def dont_run_twice(f):
    list_fun = [None]

    def wrapper(*args):
        if args == list_fun[-1]:
            return
        else:
            list_fun.append(args)
            return f(*args)

    return wrapper
"""
"""
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.face = Face(self, width = 125, height = 175, bg = "#76F015")
        self.face.pack()

        btn = tk.Button(self, text="Smile", command=self.face.smile)
        btn.pack()

        btn = tk.Button(self, text="Normal", command=self.face.normal_mouth)
        btn.pack()

        btn = tk.Button(self, text="Quick smile", command=self.quick_smile)
        btn.pack()

    def quick_smile(self):
        self.face.smile()
        self.after(500, self.face.normal_mouth) # return to normal after .5 seconds

class Face(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)

        # make outside circle
        self.create_oval(25, 40, 105, 120)

        # make eyes
        self.create_oval(40, 55, 60, 75)
        self.create_oval(70, 55, 90, 75)

        # make initial mouth
        self.mouth = [] #list of things in the mouth
        self.normal_mouth()

    def smile(self):
        self.clear(self.mouth) # clear off the previous mouth
        self.mouth = [
            self.create_arc(45, 80, 85, 100, start=180, extent=180)
            ]

    def normal_mouth(self):
        self.clear(self.mouth) # clear off the previous mouth
        self.mouth = [
            self.create_line(45, 100, 85, 100),
            self.create_arc(25, 95, 45, 105, extent=90, start=-45, style='arc'), # dimple
            self.create_arc(85, 95, 105, 105, extent=90, start=135, style='arc') # dimple
            ]

    def clear(self, items):
        '''delete all the items'''
        for item in items:
            self.delete(item)

def main():
    root = tk.Tk()
    win = App(root)
    win.pack()
    root.mainloop()

"""

from tkinter import *

root = Tk()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(root)
listbox.pack()

for i in range(100):
    listbox.insert(END, i)

# attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

mainloop()