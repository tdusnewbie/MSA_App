#!/usr/bin/env python3

import sqlite3

from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

from Model import Database

class UserInfoDialog(Toplevel):
    def __init__(self, parent, username, **kw):
        Toplevel.__init__(self, parent, **kw)
        self.parent = parent
        self.data = Database()
        self.user = self.data.getUserInfo(username)
        self.drawDialog()
    
    def drawDialog(self):
        layoutUserInfo = Frame(self)

        lblNameTitle = Label(layoutUserInfo, text = "Tên người dùng: ")
        self.lblName = Label(layoutUserInfo, text = self.user.name)
        btnChangeName = Button(layoutUserInfo,text = "Đổi", command = self.onChangeName)
        
        lblUsernameTitle = Label(layoutUserInfo, text = "Username: ")
        self.lblUsername = Label(layoutUserInfo, text = self.user.username)

        hiddenPass = len(self.user.passWord) * "*"        
        lblPassTitle = Label(layoutUserInfo, text = "Password")
        self.lblPass = Label(layoutUserInfo, text = hiddenPass)
        btnChangePass = Button(layoutUserInfo,text = "Đổi", command = self.onChangePass)

        lblNameTitle.grid(row = 0, column = 0)
        self.lblName.grid(row = 0, column = 1, columnspan = 2)
        btnChangeName.grid(row = 0, column = 3)
        
        lblUsernameTitle.grid(row = 1, column = 0)
        self.lblUsername.grid(row = 1, column = 1, columnspan = 2)
        
        lblPassTitle.grid(row = 2, column = 0)
        self.lblPass.grid(row = 2, column = 1, columnspan = 2)
        btnChangePass.grid(row = 2, column = 3)

        layoutUserInfo.pack(side = TOP, fill = BOTH, expand = True, padx = 10, pady = 10)

    def onChangeName(self):
        newName = simpledialog.askstring("Đổi tên","Nhập tên mới", parent = self)
        if newName != None:
            if len(newName) > 0:
                self.lblName["text"] = newName
                self.data.updateNameOfuser(self.user.username,newName)
            else:
                messagebox.showerror("Empty!!!","Tên không thể để trống")
                return
        else:
            return

    def onChangePass(self):
        def onChange():
            if len(entryNewPass.get()) <= 0 or len(entryRetype.get()) <=0:
                messagebox.showerror("Empty","Bạn không thể để trống! Xin hãy nhập đầy đủ", parent = newPassDialog)
                return

            if entryNewPass.get() == entryRetype.get():
                temp = len(entryNewPass.get()) * "*"
                self.lblPass["text"] = temp
                self.data.updatePassOfUser(self.user.username, entryNewPass.get())
            else:
                messagebox.showwarning("Not Fix!!!","Bạn nhập lại pass không đúng", parent = newPassDialog)
                return
            
            newPassDialog.destroy()

        def onCancel():
            newPassDialog.destroy()

        newPassDialog = Toplevel(self)
        
        lblNewPass = Label(newPassDialog,text = "Nhập pass mới: ")
        entryNewPass = Entry(newPassDialog, show = "*")

        lblRetype = Label(newPassDialog, text = "Nhập lại: ")
        entryRetype = Entry(newPassDialog, show = "*")

        btnChange = Button(newPassDialog, text ="Đổi", command = onChange)
        btnCancel = Button(newPassDialog, text = "Hủy", command = onCancel)

        lblNewPass.grid(row = 0, column = 0)
        entryNewPass.grid(row = 0, column = 1, columnspan = 2)
        entryNewPass.focus_set()
        lblRetype.grid(row = 1, column = 0)
        entryRetype.grid(row = 1, column = 1, columnspan = 2)
        btnChange.grid(row = 2, column = 0)
        btnCancel.grid(row = 2, column = 2)
