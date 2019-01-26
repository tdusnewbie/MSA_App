#!/usr/bin/env python3

import sqlite3

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from Model import TypeItem, Database

class NewTypeDialog:
    def __init__(self, master):
        self.dialog = Toplevel(master)
        self.dialog.resizable(0,0)
        self.master = master
        self.data = Database()
        self.itemList = self.data.getItemList()
        self.typeItem = TypeItem()
        self.drawDialog(self.dialog)
        self.linkAccelerator()
        self.dialog.protocol("WM_DELETE_WINDOW",self.onCancel)
    
    def linkAccelerator(self):
        self.dialog.bind_all("<Escape>",self.onCancel)
        
    def drawDialog(self, dialog):
        layoutDialog = Frame(dialog)
        listParent = []
        for item in self.itemList:
            listParent.append(item.name)
        # Parent of Type
        lblParentTitle = Label(layoutDialog, text = "Thuộc Mặt hàng")
        self.comboParent = Combobox(layoutDialog,values = listParent)
        self.comboParent.bind(sequence="<<ComboboxSelected>>",func= self.onParentSelect)

        # Name Of Type
        lblNameTitle = Label(layoutDialog, text = "Tên loại hàng")
        self.entryName = Entry(layoutDialog)
        
        # ID of Type
        lblIDTitle = Label(layoutDialog, text = "Tạo ID")
        self.entryID = Entry(layoutDialog)
        
        # Amount of Type
        lblAmountTitle = Label(layoutDialog, text = "Số lượng nhập")
        self.entryAmount = Entry(layoutDialog)

        # Unit Price of Type
        lblUnitTitle = Label(layoutDialog, text = "Đơn giá")
        self.entryUnit = Entry(layoutDialog)


        # Button Create Account and Cancel
        btnAdd = Button(layoutDialog, text = "Thêm", command = self.onAddNewType)
        btnCancel = Button(layoutDialog, text = "Hủy", command = self.onCancel)

        # Add Widget to Dialog
        lblParentTitle.grid(row = 0, column = 0, sticky = "w", pady = 5)
        self.comboParent.grid(row = 0, column = 1, columnspan = 2, pady = 5)
        self.comboParent.focus_set()

        lblNameTitle.grid(row = 1, column = 0, sticky = "w", pady = 5)
        self.entryName.grid(row = 1, column = 1, columnspan = 2, pady = 5)

        lblIDTitle.grid(row = 2, column = 0, sticky = "w", pady = 5)
        self.entryID.grid(row = 2, column = 1, columnspan = 2, pady = 5)
        
        lblAmountTitle.grid(row = 3, column = 0, sticky = "w", pady = 5)
        self.entryAmount.grid(row = 3, column = 1, columnspan = 2, pady = 5)

        lblUnitTitle.grid(row = 4, column = 0, sticky = "w", pady = 5)
        self.entryUnit.grid(row = 4, column = 1, columnspan = 2, pady = 5)

        btnAdd.grid(row = 5, column = 0, columnspan = 1, pady = 10)
        btnCancel.grid(row = 5, column = 1, columnspan = 2, pady = 10)

        layoutDialog.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

    def onAddNewType(self,event = None):
        # sqlite3.IntegrityError
        if not self.entryName.get():
            messagebox.showwarning("Empty !!!!",message="Tên loại hàng không thể để trống")
            return
        if not self.entryID.get():
            messagebox.showwarning("Empty !!!!",message="ID không thể để trống")
            return

        self.typeItem.idType = self.entryID.get()
        self.typeItem.unitPrice = self.entryUnit.get()
        self.typeItem.amount = self.entryAmount.get()
        self.typeItem.name = self.entryName.get()
        try:
            self.data.insertTypeItem(self.typeItem)
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


    def onCancel(self,event = None):
        self.dialog.unbind_all("<Escape>")
        self.dialog.destroy()

    def onParentSelect(self, event = None):
        pos = self.comboParent.current()
        self.typeItem.idParent = self.itemList[pos].id

