#!/usr/data/dir

import sqlite3

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from Model import BillInfoModel, Database

class ShowBillDialog:
    def __init__(self,parent):
        self.parent = parent
        self.data = Database()
        self.listBill = self.data.getBillList()
        self.dialog = Toplevel(parent)
        self.dialog.title("Bảng thống kê Hóa đơn")
        self.dialog.geometry("1000x400")

        self.drawDialog(self.dialog)

    def drawDialog(self, parent):

        layoutTree = Frame(parent)
        
        self.drawTreeBill(layoutTree)

        for bill in self.listBill:
            self.addBillIntoTree(bill)

        layoutTree.pack(side = TOP, fill = BOTH, expand = True)

    def drawTreeBill(self, parent):
        listAttribute = ["Mặt hàng", "Loại hàng", "ID", "Số lượng xuất", "Thành giá", "Người tạo"]
        
        yScrollTree = Scrollbar(parent, orient = VERTICAL)
        xScrollTree = Scrollbar(parent, orient = HORIZONTAL)

        # Create Delete, Add and Edit Button
        # layoutButton = Frame(parent)
        
        # btnAddBill = Button(layoutButton, text = "+", fg = "green", command = self.onAddBill)
        # btnDelBill = Button(layoutButton, text = "-", fg = "red", command = self.onDeleteBill)
        # btnEditBill = Button(layoutButton, text = "Edit", fg = "blue")

        # btnAddBill.pack(side = LEFT)
        # btnDelBill.pack(side = LEFT)
        # btnEditBill.pack(side = LEFT)
        
        # layoutButton.pack(side = TOP, anchor = "w")

        # Create Tree View
        self.treeBill = Treeview(parent, column = listAttribute,
            yscrollcommand = yScrollTree.set, 
            xscrollcommand = xScrollTree.set
        )
        # self.treeBill.bind(sequence="<Double-Button-1>",func=self.onEditBill)

        self.treeBill.column(column = "#0", width = 100, minwidth = 100)
        for nameAttr in listAttribute:
            self.treeBill.heading(column = nameAttr, text = nameAttr)
            self.treeBill.column(column = nameAttr, width = 100, minwidth = 100)

        
        #Create Scrollbar for tree view
        yScrollTree.pack(side = RIGHT, fill = Y)
        xScrollTree.pack(side = BOTTOM, fill = X)
        

        self.treeBill.pack(side = TOP, anchor = "w", fill = BOTH, expand = True)
        yScrollTree.config(command = self.treeBill.yview)
        xScrollTree.config(command = self.treeBill.xview)

    def addBillIntoTree(self,billInput):
        bill = billInput

        if not self.treeBill.exists(bill.CreatedDate) :
            self.treeBill.insert("","end", str(bill.CreatedDate), text = bill.CreatedDate, tags = "parents")

        self.treeBill.item(bill.CreatedDate, open = True)

        self.treeBill.insert(bill.CreatedDate,END, bill.CreatedTime, text = bill.CreatedTime, tags = "childs")
        self.treeBill.set(bill.CreatedTime, "Mặt hàng", bill.name)
        self.treeBill.set(bill.CreatedTime, "Loại hàng", bill.type)
        self.treeBill.set(bill.CreatedTime, "ID", bill.id)
        self.treeBill.set(bill.CreatedTime, "Số lượng xuất", bill.amount)
        self.treeBill.set(bill.CreatedTime, "Thành giá", int(bill.price))
        self.treeBill.set(bill.CreatedTime, "Người tạo", bill.CreatedUser)


if __name__ == '__main__':
    root = Tk()

    dialog = ShowBillDialog(root)

    root.mainloop()
