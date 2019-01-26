#!/bin/usr/python3 

from tkinter import *
from LoginView import LoginScreen
from Model import Database


class ManagingSellingApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Managing Selling App")
        self.frame = []
        self.data = Database()
        frame = LoginScreen(self)

        self.showFrame(frame)

    def showFrame(self,openFrame):
        self.frame.append(openFrame)
        pos = len(self.frame) -1 
        frame = self.frame[pos]
        frame.tkraise()
        
    def backToPreviousFrame(self):
        self.frame.pop()
        pos = len(self.frame) -1 
        frame = self.frame[pos]
        frame.pack(fill = X , expand = True)
        frame.tkraise()

app = ManagingSellingApp()
app.geometry("400x400")
app.mainloop()