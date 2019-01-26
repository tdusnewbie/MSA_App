#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from SignUpView import SignUpDialog
from HomeView import HomeScreen
from Model import User,Database

class LoginScreen(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.isKeepLogin = IntVar()
        self.listUser = self.parent.data.getUserList()

        self.drawScreen()

    def drawScreen(self):
        self.pack(fill = X , expand = 1)

        ######## Create User Input Layout #######
        layoutUserInput = Frame(self)

        # User name
        lblUserName = Label(layoutUserInput, text = "Username: ")
        lblUserName.grid(row = 0, column = 0, pady = 5, sticky = W)
        self.entryUserName = Entry(layoutUserInput)
        self.entryUserName.grid(row = 0, column = 1, pady = 5)
        self.entryUserName.focus_set()

        # Password
        lblPass = Label(layoutUserInput, text = "Pass: ")
        lblPass.grid(row = 1, column = 0, pady = 5, sticky = W)
        self.entryPass = Entry(layoutUserInput)
        self.entryPass.grid(row = 1, column = 1, pady = 5)
        self.entryPass.config(show="*")

        # Save Login State
        keepLoggedIn = Checkbutton(layoutUserInput, text = "Nhớ mật khẩu !!!", variable = self.isKeepLogin)
        keepLoggedIn.grid(row = 2,columnspan = 2, pady = 5)

        layoutUserInput.pack(side = TOP)

        ######## Create Button Login Layout #######
        layoutButton = Frame(self)

        btnLogIn = Button(layoutButton, text = "Đăng nhập", command = self.onClickLogIn)
        btnLogIn.pack(side=LEFT, padx = 5)

        btnSignUp = Button(layoutButton, text = "Đăng kí", command = self.onClickSignUp)
        btnSignUp.pack(side=LEFT, padx = 5)

        layoutButton.pack(side = TOP, pady = 30)

    def onClickLogIn(self):
        self.listUser = self.parent.data.getUserList()

        username = self.entryUserName.get()
        passWord = self.entryPass.get()

        if len(username) == 0:
            messagebox.showwarning("Empty !!!", "username không thể để trống !!!")
            self.entryUserName.focus_set()
            return 
        
        if " " in username:
            messagebox.showwarning("Error !!!!",message="Username không được có khoảng cách")
            return

        elif len(passWord) == 0:
            messagebox.showwarning("Empty !!!", "password không thể để trống !!!")
            self.entryPass.focus_set()
            return

        if not self.findUserInList(username,passWord):
            messagebox.showwarning("Username hoặc Password Sai", "Không thể tìm thấy username hoặc password trong database!!!")
            return

        # print(username, passWord, self.isKeepLogin.get())
        self.pack_forget()
        frame = HomeScreen(self.parent,username)
        self.parent.geometry("700x400")
        self.parent.showFrame(frame)

    def findUserInList(self, username, password):
        for user in self.listUser:
            if username == user.username and password == user.passWord:
                return True
            
        return False

    def onClickSignUp(self):
        SignUpDialog(self)
        # if self.user:
        #     print("Is Existed")
        # else:
        #     print("Is Not Existed")      


            

# root = Tk()

# root.geometry("400x400")

# # lg = LoginScreen(root)


# root.mainloop()