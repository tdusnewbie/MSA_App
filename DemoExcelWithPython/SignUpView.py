#!/usr/bin/env python3

import sqlite3

from tkinter import *
from tkinter import messagebox
from Model import User, Database

class SignUpDialog:
    def __init__(self, master):
        self.dialog = Toplevel(master)
        self.dialog.resizable(0,0)
        self.master = master
        self.data = Database()
        self.user = None
        self.drawDialog(self.dialog)
        self.dialog.bind_all("<Escape>",self.onCancel)
        self.dialog.bind_all("<Return>", self.onCreateAccount)
    
    def drawDialog(self, dialog):
        layoutDialog = Frame(dialog)
        
        # Name Of User
        lblNameUserTitle = Label(layoutDialog, text = "Họ tên: ")
        self.entryNameUser = Entry(layoutDialog)
        
        # Account of User
        lblAccountTitle = Label(layoutDialog, text = "Tạo Username")
        self.entryAccount = Entry(layoutDialog)
        
        # Password of User
        lblPasswordTitle = Label(layoutDialog, text = "Tạo Password")
        self.entryPassWord = Entry(layoutDialog)
        self.entryPassWord.config(show = "*")

        # Button Create Account and Cancel
        btnCreate = Button(layoutDialog, text = "Tạo", command = self.onCreateAccount)
        btnCancel = Button(layoutDialog, text = "Hủy", command = self.onCancel)

        # Add Widget to Dialog
        lblNameUserTitle.grid(row = 0, column = 0, sticky = "w", pady = 5)
        self.entryNameUser.grid(row = 0, column = 1, columnspan = 2, pady = 5)
        self.entryNameUser.focus_set()

        lblAccountTitle.grid(row = 1, column = 0, sticky = "w", pady = 5)
        self.entryAccount.grid(row = 1, column = 1, columnspan = 2, pady = 5)
        
        lblPasswordTitle.grid(row = 2, column = 0, sticky= "w", pady = 5)
        self.entryPassWord.grid(row = 2, column = 1, columnspan = 2, pady = 5)

        btnCreate.grid(row = 3, column = 0, columnspan = 1, pady = 10)
        btnCancel.grid(row = 3, column = 1, columnspan = 2, pady = 10)

        layoutDialog.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

    def onCreateAccount(self):
        # sqlite3.IntegrityError
        if not self.entryNameUser.get():
            messagebox.showwarning("Empty !!!!",message="Họ tên không thể để trống")
            return

        if not self.entryAccount.get():
            messagebox.showwarning("Empty !!!!",message="Username không thể để trống")
            return

        if " " in self.entryAccount.get():
            messagebox.showwarning("Error !!!!",message="Username không được có khoảng cách")
            return

        if not self.entryPassWord.get():
            messagebox.showwarning("Empty !!!!",message="Password không thể để trống")
            return        

        user = User(name = self.entryNameUser.get(), username = self.entryAccount.get(), passWord = self.entryPassWord.get())
        try:
            self.data.insertUser(user)
        except sqlite3.IntegrityError:
            messagebox.showwarning("Opps !!!!",message="Username bạn chọn đã tồn tại !!!!")

        self.master.entryUserName.insert(0,user.username)
        self.master.entryPass.insert(0,user.passWord)
        self.master.listUser = self.data.getUserList()
        self.dialog.destroy()


    def onCancel(self, event = None):
        self.dialog.destroy()
