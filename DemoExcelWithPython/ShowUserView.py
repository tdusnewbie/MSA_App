#!/usr/bin/env python3

import sqlite3

from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter.ttk import Treeview
from Model import Database, User

class ShowListUserDialog(Toplevel):
    def __init__(self,parent,**kw):
        Toplevel.__init__(self,parent,**kw)
        self.parent = parent
        self.numberTempUserAdd = 0
        self.data = Database()
        self.listUser = self.data.getUserList()

        self.menu = Menu(self)
        self.config(menu = self.menu)
        self.drawMenu(self.menu)
        self.drawDialog()
        
        for user in self.listUser:
            self.addUserIntoTree(user)

        self.linkAccelerator()

    def linkAccelerator(self):
        self.bind_all("<Control-N>",self.onAddUser)
        self.bind_all("<Delete>", self.onDeleteUser)
        self.treeUser.bind(sequence="<Double-Button-1>",func=self.onEditUser)

    def drawMenu(self, parent):
        # Type Menu
        typeMenu = Menu(parent)
        typeMenu.add_command(label = "Thêm User", command = self.onAddUser, accelerator = "Ctrl+Shift+N")
        typeMenu.add_command(label = "Xóa User", command = self.onDeleteUser, accelerator = "Delete")
        parent.add_cascade(label = "Chức năng", menu = typeMenu)
        

    def drawDialog(self):
        layoutTreeUser = Frame(self)
        
        listAttribute = ["Password", "Họ tên"]
        
        yScrollTree = Scrollbar(layoutTreeUser, orient = VERTICAL)
        xScrollTree = Scrollbar(layoutTreeUser, orient = HORIZONTAL)

        # Create Delete, Add and Edit Button

        # Create Tree View
        self.treeUser = Treeview(layoutTreeUser, column = listAttribute,
            yscrollcommand = yScrollTree.set, 
            xscrollcommand = xScrollTree.set
        )

        self.treeUser.heading(column = "#0", text = "Username")
        self.treeUser.column(column = "#0", width = 100, minwidth = 100)
        for nameAttr in listAttribute:
            self.treeUser.heading(column = nameAttr, text = nameAttr)
            self.treeUser.column(column = nameAttr, width = 100, minwidth = 100)

        
        #Create Scrollbar for tree view
        yScrollTree.pack(side = RIGHT, fill = Y)
        xScrollTree.pack(side = BOTTOM, fill = X)
        

        self.treeUser.pack(side = TOP, anchor = "w", fill = BOTH, expand = True)
        yScrollTree.config(command = self.treeUser.yview)
        xScrollTree.config(command = self.treeUser.xview)
        layoutTreeUser.pack(side = TOP, fill = BOTH, expand = True)

    def addUserIntoTree(self,userInput):
        temp = userInput

        # if not self.treeUser.exists(temp.idParent) :
        #     self.treeUser.insert("","end", str(temp.idParent), text = temp.idParent)

        # self.treeUser.item(temp.idParent, open = True)

        self.treeUser.insert("","end", str(temp.username), text = temp.username)
        self.treeUser.set(temp.username, "Password", temp.passWord)
        self.treeUser.set(temp.username, "Họ tên", temp.name)

    def onAddUser(self, event = None):
        if self.numberTempUserAdd > 9:
            messagebox.showwarning("Warning","Bạn chỉ có thể thêm tạm 10 username \n Hãy Sửa ID để lưu lại những loại tạm trên", parent = self)
            return
        userTemp = User(name = "#",username=str(self.numberTempUserAdd),passWord="#")
        self.addUserIntoTree(userTemp)
        self.numberTempUserAdd += 1
    
    def onEditUser(self, event = None):
        listTemp = ["0","1","2","3","4","5","6","7","8","9"]

        curUser = self.treeUser.item(self.treeUser.focus())
        col = self.treeUser.identify_column(event.x)
        print(curUser)
        print(col)
        
        if curUser["text"] in listTemp and col != "#0":
            if col != "#0":
                messagebox.showinfo("Thêm User","Sửa username tạm này để lưu lại vào Database",parent = self)
                return                

        cellValue = None

        if col == "#0":
            temp =  simpledialog.askstring("Đổi Username", "Nhập mới", parent = self)

            if  temp != None:
                if len(temp)>0:
                    cellValue = curUser["text"]
                    try:
                        if cellValue in listTemp:
                            newUser = User(curUser["values"][1],temp,curUser["values"][0])
                            self.data.insertUser(newUser)
                            self.treeUser.update()
                            print("Sau khi sua:",self.treeUser.item(self.treeUser.focus()))
                        else:
                            self.data.updateUsernameOfUser(cellValue,temp)
                    except (sqlite3.IntegrityError, TclError):
                        messagebox.showwarning("Opps !!!!",message="Username bạn nhập đã tồn tại !!!!", parent = self)
                        return
                    if cellValue in listTemp:
                        self.numberTempUserAdd -= 1
                                    
                else:
                    messagebox.showwarning("Empty !!!", "Username không thể để trống",parent = self)
                
                self.treeUser.insert("", str(self.treeUser.index(self.treeUser.focus())), temp ,text = temp, values = curUser["values"])
                self.treeUser.delete(self.treeUser.focus())

            return

        if col == "#1":
            temp =  simpledialog.askstring("Đổi Password", "Nhập Password mới: ", parent = self)
            if temp != None:
                if len(temp) > 0:
                    cellValue = curUser["values"][0]
                    self.data.updatePassOfUser(curUser["text"],temp)
                    curUser["values"][0] = temp
                    print(curUser["text"])
                    self.treeUser.item(curUser["text"], values = curUser["values"])
                    self.treeUser.update()
                else:
                    messagebox.showwarning("Empty !!!", "Password không thể để trống",parent = self)

            return 

        if col == "#2":
            
            temp = simpledialog.askstring("Đổi tên", "Nhập tên mới",parent = self)
            
            if temp != None:
                if len(temp) > 0:                
                    cellValue = curUser["values"][1]
                    self.data.updateNameOfuser(curUser["text"],temp)
                    curUser["values"][1] = temp
                    print(curUser["text"])
                    self.treeUser.item(curUser["text"], values = curUser["values"])
                    self.treeUser.update()
                else:
                    messagebox.showwarning("Empty !!!", "Họ tên không thể để trống",parent = self)
                    
            return 

        print("Cell Values = ", cellValue)
        
    def onDeleteUser(self, event = None):
        curItem = self.treeUser.selection()

        accept = messagebox.askokcancel("Xóa User này","Bạn thật sự muốn xóa!!! Bạn không thể hoàn tác hành động này", parent = self)
        if accept == True:
            if len(curItem) == 0:
                messagebox.showwarning(title = "Empty !!!", message = "Xin hãy chọn User bạn muốn xóa", parent = self)
                return

            for choose in curItem:
                treeItem = self.treeUser.item(choose)
                self.data.deleteUser(treeItem["text"])
                self.treeUser.delete(treeItem["text"])

    def onDestroy(self, event):
        # ask = """
        # Bạn thực sự muốn đóng ứng dụng 
        # """
        # messagebox.askokcancel("Closing!!!",)
        self.parent.linkAccelerator()
        self.destroy()


# if __name__ == "__main__":
#     root = Tk()

#     ShowListUserDialog(root)
    
#     root.mainloop()