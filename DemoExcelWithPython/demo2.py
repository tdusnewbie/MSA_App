#!/usr/bin/env python3

from tkinter import *

def addToList():
    listItem.insert("end",entryAdd.get())

root = Tk()



entryAdd = Entry(root)
btnAdd = Button(root, text = "Add", command = addToList)
listItem = Listbox(root)

entryAdd.grid(row = 0, column = 0)
btnAdd.grid(row = 0, column = 1)
listItem.grid(row = 1, column = 0, columnspan = 2, pady = 10)



root.mainloop()
