#!/usr/bin/env python3

import sqlite3

from tkinter import *
from tkinter import messagebox
from Model import Item, Database

class NewItemDialog:
    def __init__(self, master):
        self.dialog = Toplevel(master)
        self.dialog.resizable(0,0)
        self.master = master
        self.data = Database()
        self.drawDialog(self.dialog)
        self.linkAccelerator()

        self.dialog.protocol("WM_DELETE_WINDOW",self.onCancel)
    
    def linkAccelerator(self):
        self.dialog.bind_all("<Escape>", self.onCancel)
            
    def drawDialog(self, dialog):
        layoutDialog = Frame(dialog)
        
        # Name Of Item
        lblNameTitle = Label(layoutDialog, text = "Tên mặt hàng")
        self.entryName = Entry(layoutDialog)
        
        # ID of Item
        lblIDTitle = Label(layoutDialog, text = "Tạo ID")
        self.entryID = Entry(layoutDialog)
        

        # Button Create Account and Cancel
        btnAdd = Button(layoutDialog, text = "Thêm", command = self.onAddNewItem)
        btnCancel = Button(layoutDialog, text = "Hủy", command = self.onCancel)

        # Add Widget to Dialog
        lblNameTitle.grid(row = 0, column = 0, sticky = "w", pady = 5)
        self.entryName.grid(row = 0, column = 1, columnspan = 2, pady = 5)
        self.entryName.focus_set()

        lblIDTitle.grid(row = 1, column = 0, sticky = "w", pady = 5)
        self.entryID.grid(row = 1, column = 1, columnspan = 2, pady = 5)
        

        btnAdd.grid(row = 3, column = 0, columnspan = 1, pady = 10)
        btnCancel.grid(row = 3, column = 1, columnspan = 2, pady = 10)

        layoutDialog.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

    def onAddNewItem(self):
        # sqlite3.IntegrityError
        if not self.entryName.get():
            messagebox.showwarning("Empty !!!!",message="Tên mặt hàng không thể để trống")
            return
        if not self.entryID.get():
            messagebox.showwarning("Empty !!!!",message="ID không thể để trống")
            return

        self.item = Item(name = self.entryName.get(), idItem=self.entryID.get())
        try:
            self.data.insertItem(self.item)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Opps !!!!",message="ID bạn nhập đã tồn tại !!!!")
            return

        # listItem = self.data.getItemList()
        # listName = []
        # for item in listItem:
        #     listName.append(item.name)
        # self.master.comboObject.config(values = listName)
        # self.master.listItem = listItem

        self.dialog.destroy()


    def onCancel(self, event = None):
        self.dialog.unbind_all("<Escape>")
        self.dialog.destroy()
