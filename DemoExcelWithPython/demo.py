# from tkinter import *
# from tkinter.ttk import Treeview

# root = Tk()

# root.geometry("400x400")
# screen = Frame(root)

# listCol = [ "Name", "Type", "Amount", "Price"]



# treeview = Treeview(screen,column = listCol)
# treeview.heading("#0",text = "Created Date")
# for nameCol in listCol:
#     treeview.heading(column = nameCol, text = nameCol)

# treeview.insert("","0","item1",text = "First Item")
# treeview.insert("","1","item2",text = "Second Item")
# treeview.insert("","2","item3",text = "Third Item")
# treeview.pack()

# screen.pack(fill = BOTH, expand = True)
# root.mainloop()

# listDemo = [1,2,3,4,5,6]
# listDemo.pop()
# listDemo.append(10)
# print(listDemo)

# from tkinter import *

# def showDialog():
#     dialog = Toplevel(root)
#     dialog.geometry("200x200")
#     button = Button(dialog, text = "Click", command = exit)
#     button.pack()


# root = Tk()

# root.geometry("600x600")

# buttonRoot = Button(root, text = "Show Dialog", command = showDialog)
# buttonRoot.pack()

# root.mainloop()

import tkinter as tk

# --- functions ---

def method(event):
    print('-----')
    print('[DEBUG] event.char  :', event.char)
    print('[DEBUG] event.keysym:', event.keysym)
    print('[DEBUG] event.state :', event.state, '=', bin(event.state))

    if event.char: # skip Control_L, etc.

        # if you need `& 5` then it has to be before `& 4` 

        if event.state & 5 == 5: # it needs `== 5` because `& 5` can give results `5`, `4` or `1` which give `True` or `0` which gives `False`
            print('method: Control+Shift +', event.keysym)

        elif event.state & 4: # it doesn't need `== 4` because `& 4` can give only results `4` or `0`
            print('method: Control +', event.keysym)

        elif event.state & 1: # it doesn't need `== 1` because `& 1` can give only results `1` or `0`
            print('method: Shift +', event.keysym)

        else:
            print('method:', event.keysym)

# --- main ---

root = tk.Tk()

root.bind("<Key>", method)

root.mainloop()