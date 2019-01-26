#!/bin/usr/python3 

import sqlite3
import random

from tkinter import *
from tkinter import messagebox, simpledialog, Widget
from tkinter.ttk import Notebook, Treeview
from Model import Database, TypeItem, Item
from NewItemView import NewItemDialog


class ShowDataWindow(Toplevel):
    def __init__(self,parent, **kw):
        Toplevel.__init__(self,parent, **kw)
        self.parent = parent
        self.title("Bảng thống kê mặt hàng")
        self.geometry("600x400")
        self.data = Database()
        self.drawDialog()
        self.linkAccelerator()

        self.protocol("WM_DELETE_WINDOW", self.quitDialog)
    
    def linkAccelerator(self):
        self.bind_all("<Control-n>",self.onAddItem)
        self.bind_all("<Control-r>", self.onRefresh)


    def drawDialog(self):
        listItem = self.data.getItemList()
        self.table = Notebook(self)
        
        for item in listItem:
            self.onAddToTab(item)

        self.table.pack(side = LEFT, fill = BOTH, expand = True, padx = 5, pady = 5)

    def onAddToTab(self, item):
        treeType =TreeType(self.table,item,self)
        self.table.add(treeType,text = item.name)
        self.table.pack()

    def quitDialog(self):
        self.parent.linkAccelerator()
        self.destroy()

    def onRefresh(self, event = None):
        self.table.destroy()
        self.drawDialog()

    def onAddItem(self, event = None):
        if event != None:
            print("Ctrl+N")
        NewItemDialog(self)

class TreeType(Frame):
    def __init__(self, parent, item, dialog):
        Frame.__init__(self,parent)
        self.parent = parent
        self.item = item
        self.numTypeAdded = 0
        self.dialogParent = dialog
        self.listType = item.type
        self.data = Database()
        self.drawScreen()

        self.linkAccelerator()

        for typeItem in self.listType:
            self.addTypeIntoTree(typeItem)

    def linkAccelerator(self):
        self.bind_all("<Shift-Delete>",self.onDeleteItem)
        self.bind_all("<Control-N>",self.onAddType)
        self.bind_all("<Delete>", self.onDeleteType)
        
    def drawScreen(self):
        # self.pack(fill = BOTH, anchor = "w", expand = True)

        ########## Listing all Bills which has been created ###########
        layoutList = Frame(self)

        self.drawTreeOfType(layoutList)

        layoutList.pack(side = LEFT, fill = BOTH, expand = True)

        self.menu = Menu(self)
        self.dialogParent.config(menu = self.menu)
        self.drawMenu(self.menu)

    def drawTreeOfType(self,parent):
        self.pack(fill = BOTH , expand = True)

        listAttribute = ["Loại hàng", "Số lượng tồn", "Đơn giá"]
        
        yScrollTree = Scrollbar(parent, orient = VERTICAL)
        xScrollTree = Scrollbar(parent, orient = HORIZONTAL)

        # Create Delete, Add and Edit Button
        layoutButton = Frame(self)
        
        btnAddType = Button(layoutButton, text = "+", fg = "green", command = self.onAddType)
        btnDelType = Button(layoutButton, text = "-", fg = "red", command = self.onDeleteType)
        btnRefresh = Button(layoutButton, text = "Refresh", fg = "blue", command = self.dialogParent.onRefresh)
        btnAddType.pack(side = LEFT)
        btnDelType.pack(side = LEFT)
        btnRefresh.pack(side = RIGHT)
        
        layoutButton.pack(side = TOP, fill = X, anchor = "w")

        # Create Tree View
        self.treeType = Treeview(parent, column = listAttribute,
            yscrollcommand = yScrollTree.set, 
            xscrollcommand = xScrollTree.set
        )
        self.treeType.bind(sequence="<Double-Button-1>",func=self.onEditType)

        self.treeType.heading(column = "#0", text = "ID")
        self.treeType.column(column = "#0", width = 100, minwidth = 100)
        for nameAttr in listAttribute:
            self.treeType.heading(column = nameAttr, text = nameAttr)
            self.treeType.column(column = nameAttr, width = 100, minwidth = 100)

        
        #Create Scrollbar for tree view
        yScrollTree.pack(side = RIGHT, fill = Y)
        xScrollTree.pack(side = BOTTOM, fill = X)
        

        self.treeType.pack(side = TOP, anchor = "w", fill = BOTH, expand = True)
        yScrollTree.config(command = self.treeType.yview)
        xScrollTree.config(command = self.treeType.xview)

    def drawMenu(self, parent):
        # Item Menu
        itemMenu = Menu(parent)
        itemMenu.add_command(label = "Thêm mặt hàng", command = self.dialogParent.onAddItem, accelerator = "Ctrl+N")
        itemMenu.add_command(label = "Xóa mặt hàng", command = self.onDeleteItem, accelerator = "Shift+Delete")
        parent.add_cascade(label = "Mặt hàng", menu = itemMenu)

        # Type Menu
        typeMenu = Menu(parent)
        typeMenu.add_command(label = "Thêm loại hàng", command = self.onAddType, accelerator = "Ctrl+Shift+N")
        typeMenu.add_command(label = "Xóa loại hàng", command = self.onDeleteType, accelerator = "Delete")
        parent.add_cascade(label = "Loại hàng", menu = typeMenu)

    def addTypeIntoTree(self,typeInput):
        temp = typeInput

        # if not self.treeType.exists(temp.idParent) :
        #     self.treeType.insert("","end", str(temp.idParent), text = temp.idParent)

        # self.treeType.item(temp.idParent, open = True)

        self.treeType.insert("","end", str(temp.idType), text = temp.idType)
        self.treeType.set(temp.idType, "Loại hàng", temp.name)
        self.treeType.set(temp.idType, "Số lượng tồn", temp.amount)
        self.treeType.set(temp.idType, "Đơn giá", int(temp.unitPrice))

    def onEditType(self, event = None):
        listTemp = ["0","1","2","3","4","5","6","7","8","9"]

        curItem = self.treeType.item(self.treeType.focus())
        col = self.treeType.identify_column(event.x)
        print(curItem)
        print(col)
        
        if curItem["text"] in listTemp and col != "#0":
            if col != "#0":
                messagebox.showinfo("Thêm loại","Sửa ID loại tạm này để lưu lại vào Database",parent = self)
                return                

        cellValue = None

        if col == "#0":
            temp =  simpledialog.askstring("Đổi ID", "Nhập ID mới", parent = self)

            if  temp != None:
                if len(temp)>0:
                    cellValue = curItem["text"]
                    try:
                        if cellValue in listTemp:
                            idTab = self.parent.select()
                            frameChosen = self.parent._nametowidget(idTab)
                            typeItem = TypeItem(curItem["values"][0],0,0,temp,frameChosen.item.id)
                            self.data.insertTypeItem(typeItem)
                            frameChosen.treeType.update()
                            print("Sau khi sua:",self.treeType.item(self.treeType.focus()))
                        else:
                            self.data.updateIdOfType(cellValue,temp)
                    except (sqlite3.IntegrityError, TclError):
                        messagebox.showwarning("Opps !!!!",message="ID bạn nhập đã tồn tại !!!!", parent = self)
                        return
                    
                    if cellValue in listTemp:
                        frameChosen.numTypeAdded -= 1

                    self.treeType.update()
                else:
                    messagebox.showwarning("Empty !!!", "ID không thể để trống",parent = self)
                
                self.treeType.insert("", str(self.treeType.index(self.treeType.focus())), temp ,text = temp, values = curItem["values"])
                self.treeType.delete(self.treeType.focus())

            return

        if col == "#1":
            
            temp =  simpledialog.askstring("Đổi tên loại hàng", "Nhập tên mới",parent = self)
            
            if temp != None:
                if len(temp) > 0:             
                    cellValue = curItem["values"][0]
                    self.data.updateNameOfType(curItem["text"],temp)
                    curItem["values"][0] = temp
                    self.treeType.item(curItem["text"], values = curItem["values"])
                    self.treeType.update()
                else:
                    messagebox.showwarning("Empty !!!", "Tên loại hàng không thể để trống",parent = self)
                    
            return 


        if col == "#2":
            temp =  simpledialog.askinteger("Đổi số lượng tồn", "Nhập số lượng tồn mới: ", parent = self)
            if temp != None:
                if temp >= 0:
                    cellValue = curItem["values"][1]
                    self.data.updateAmountOfType(curItem["text"],temp)
                    curItem["values"][1] = temp
                    print(curItem["text"])
                    self.treeType.item(curItem["text"], values = curItem["values"])
                    self.treeType.update()
                else:
                    messagebox.showwarning("Empty !!!", "Số lượng không thể là số âm",parent = self)

            return 

        if col == "#3":
            temp =  simpledialog.askfloat("Đổi đơn giá", "Nhập đơn giá mới: ",parent = self)
            if temp != None:
                if temp >= 0:
                    cellValue = curItem["values"][2]
                    self.data.updateUnitOfType(curItem["text"],temp)
                    curItem["values"][2] = temp
                    print(curItem["text"])
                    self.treeType.item(curItem["text"], values = curItem["values"])
                    self.treeType.update()
                else:
                    messagebox.showwarning("Empty !!!", "Đơn giá không thể là số âm",parent = self)

            return
        print("Cell Values = ", cellValue)
    
    def onAddType(self, event = None):
        idTab = self.parent.select()
        frameChosen = self.parent._nametowidget(idTab)
        if frameChosen.numTypeAdded > 9:
            messagebox.showwarning("Warning","Bạn chỉ có thể thêm tạm 10 loại \n Hãy Sửa ID để lưu lại những loại tạm trên", parent = self)
            return
        
        typeItem = TypeItem(name = frameChosen.numTypeAdded, amount = 0, unitPrice = 0, idType = "#", idParent = frameChosen.item.id)
        frameChosen.addTypeIntoTree(typeItem)
        frameChosen.numTypeAdded += 1

    def onDeleteType(self, event = None):
        idTab = self.parent.select()
        frameChosen = self.parent._nametowidget(idTab)
        curItem = frameChosen.treeType.selection()

        accept = messagebox.askokcancel("Xóa loại hàng này","Bạn thật sự muốn xóa!!! Bạn không thể hoàn tác hành động này", parent = self)
        if accept == True:
            if len(curItem) == 0:
                messagebox.showwarning(title = "Empty !!!", message = "Xin hãy chọn loại hàng bạn muốn xóa", parent = self)
                return

            for choose in curItem:
                treeItem = frameChosen.treeType.item(choose)
                self.data.deleteType(treeItem["values"][0])
                frameChosen.treeType.delete(treeItem["text"])
    
    def onDeleteItem(self, event = None):
        idTab = self.parent.select()
        frameChosen = self.parent._nametowidget(idTab)
        accept = messagebox.askokcancel("Xóa loại hàng này","Bạn thật sự muốn xóa!!! Bạn không thể hoàn tác hành động này", parent = self)
        if accept == True:
            idTab = self.parent.select()
            frameChosen = self.parent._nametowidget(idTab)

            self.data.deleteItem(frameChosen.item.id)
            self.parent.forget(idTab)
            self.parent.update()

    def onDestroy(self, event):
        # ask = """
        # Bạn thực sự muốn đóng ứng dụng 
        # """
        # messagebox.askokcancel("Closing!!!",)
        self.dialogParent.destroy()

if __name__ == "__main__":
    root = Tk()
    ShowDataWindow(root)
    root.mainloop()