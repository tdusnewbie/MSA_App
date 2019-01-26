#!/usr/bin/env python3

import sqlite3
import datetime

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from Model import BillInfoModel, Database

class AddBillDialog:
    def __init__(self, master):
        self.dialog = Toplevel(master)
        self.dialog.resizable(0,0)
        self.dialog.title("Thêm hóa đơn")
        self.master = master
        self.headerID = "##"
        self.footerID = "##"
        self.tempPrice = IntVar()
        self.unitPrice = 0
        self.amountOfType = 0
        self.data = Database()
        self.listItem = self.data.getItemList()
        self.drawDialog(self.dialog)
        self.dialog.bind_all("<Escape>",self.onCancel)
        self.dialog.bind_all("<Return>",self.onAddBill)
    
    def drawDialog(self, dialog):
        layoutSetInfo = Frame(dialog)

        layoutMakeBill = Frame(layoutSetInfo, bd = 0, highlightthickness = 1)

        self.setBillInfo(layoutMakeBill)        
        
        layoutMakeBill.pack(side = TOP, fill = BOTH, expand = True, pady = 10)

        layoutButton = Frame(layoutSetInfo)
        btnAddBill = Button(layoutButton, text = "Thêm hóa đơn", command = self.onAddBill)
        btnCancel = Button(layoutButton, text = "Hủy", command = self.onCancel)

        btnAddBill.grid(row = 0, column = 0, columnspan = 1)
        btnCancel.grid(row = 0, column = 1, columnspan = 2)
        layoutButton.pack(side = TOP, fill = X, expand = True, pady = 10)

        layoutSetInfo.pack(side = LEFT, expand = True, padx = 10)

    def setBillInfo(self, parent):
        # Choose Object
        listNameItem = []
        for item in self.listItem:
            listNameItem.append(item.name)
        
        lblObject = Label(parent, text = "Mặt hàng: ")
        self.comboObject = Combobox(parent, values = listNameItem)
        self.comboObject.bind(sequence = "<<ComboboxSelected>>",func = self.onChangeComboObjectValues)

        # Choose type of Object
        lblType = Label(parent, text = "Loại hàng: ")
        self.comboType = Combobox(parent)
        self.comboType.bind(sequence = "<<ComboboxSelected>>", func = self.onChangeComboTypeValues)

        # Input amount of object
        lblAmount = Label(parent, text = "Số lượng xuất: ")
        self.entryAmount = Spinbox(parent,textvariable = self.tempPrice)
        self.tempPrice.trace("w",self.onEntryChanged)

        # View The Id of Object
        lblIdTitle = Label(parent, text = "ID: ")
        self.lblIdObject = Label(parent, text = "##-##")

        # View The Price of one object
        lblPriceTitle = Label(parent, text = "Thành giá: ")
        self.lblPrice = Label(parent, text = 0)
        lblPriceUnit = Label(parent, text = "VND")

        # Choose Date Make Bill
        lblChooseDateTitle = Label(parent, text = "Ngày tạo: ")
        self.lblChooseDate = Label(parent, text = str(datetime.datetime.now().date().strftime("%d-%m-%Y")))

        # Add widgets into grid layout

        lblObject.grid(row = 0, column = 0, sticky = "w", pady = 5)
        self.comboObject.grid(row = 0, column = 1, columnspan = 3,pady = 5)
        self.comboObject.focus_set()

        lblType.grid(row = 1, column = 0, sticky = "w", pady = 5)
        self.comboType.grid(row = 1, column = 1, columnspan = 3,pady = 5)

        lblAmount.grid(row = 2, column = 0, sticky = "w", pady = 5)
        self.entryAmount.grid(row = 2, column = 1, columnspan = 3, pady = 5)

        lblIdTitle.grid(row = 3, column = 0, sticky = "w", pady = 5)
        self.lblIdObject.grid(row = 3, column = 1, sticky = "w", pady = 5)

        lblPriceTitle.grid(row = 4, column = 0, sticky = "w", pady = 5)
        self.lblPrice.grid(row = 4, column = 1, sticky = "w", pady = 5)
        lblPriceUnit.grid(row = 4, column = 3, sticky = "w", pady = 5)

        lblChooseDateTitle.grid(row = 5, column = 0, sticky = "w", pady = 5)
        self.lblChooseDate.grid(row = 5, column = 1, sticky = "w", pady = 5)

    def onAddBill(self):
        # sqlite3.IntegrityError
        if self.comboObject.current() == -1:
            messagebox.showwarning("Empty !!!!",message="Xin hãy chọn một mặt hàng")
            return
        
        if self.comboType.current() == -1:
            messagebox.showwarning("Empty !!!!",message="Xin hãy chọn một loại hàng")
            return
        
        if int(self.entryAmount.get()) > self.amountOfType:
            messagebox.showwarning("Too Large !!!!",message="Vượt quá số lượng còn lại")
            self.entryAmount.delete(0,END)
            self.entryAmount.insert(0,self.amountOfType)
            return

        if self.amountOfType == 0:
            messagebox.showwarning("Empty !!!!",message="Loại hàng này đã hết!!! Xin hãy chọn loại hàng khác")
            return

        if int(self.entryAmount.get()) <= 0 and self.amountOfType != 0:
            messagebox.showwarning("Too Small !!!!",message="Số lượng xuất quá nhỏ")
            self.entryAmount.delete(0,END)
            self.entryAmount.insert(0,0)
            return

        bill = BillInfoModel()
        bill.name = self.comboObject.get()
        bill.type = self.comboType.get()
        bill.id = self.lblIdObject["text"]
        bill.amount = int(self.entryAmount.get())
        bill.price = int(self.lblPrice["text"])
        bill.CreatedDate = self.lblChooseDate["text"]
        bill.CreatedTime = datetime.datetime.now().time().strftime("%H:%M:%S")
        bill.CreatedUser = self.master.userCreate

        self.data.insertBill(bill)
        if bill.amount == self.amountOfType:
            answer = messagebox.askquestion("Empty", "Loại hàng hiện tại sẽ hết khi bạn xuất hóa đơn \nBạn có muốn xóa luôn loại hàng này không ?")
            if answer == True:
                self.data.deleteType(self.footerID)
            elif answer == False:
                self.data.updateAmountOfType(self.footerID,0)

        else:
            self.data.updateAmountOfType(self.footerID,self.amountOfType - bill.amount)

        self.master.addBillIntoTree(bill)
        self.master.treeBill.focus_set()
        self.dialog.destroy()

    def onCancel(self, event = None):
        self.dialog.destroy()

    def onChangeComboObjectValues(self, event = None):
        pos = self.comboObject.current()
        listNameType = []
        self.listType = self.listItem[pos].type
        for typeItem in self.listType:
            listNameType.append(typeItem.name)
        self.comboType.config(values = listNameType)
        self.headerID = self.listItem[pos].id
        self.onChangeID()
        
    def onChangeComboTypeValues(self,event = None):
        pos = self.comboType.current()
        self.footerID = self.listType[pos].idType
        amount = self.listType[pos].amount
        self.unitPrice = int(self.listType[pos].unitPrice)
        self.amountOfType = amount
        self.lblPrice["text"] = self.unitPrice
        self.onChangeID()

    def onEntryChanged(self,*args):
        temp = int(self.tempPrice.get() * self.unitPrice )
        self.lblPrice['text'] = temp 
        # print(self.lblPrice['text'])

    def onChangeID(self):
        temp = self.headerID + "-" + self.footerID
        self.lblIdObject['text'] = temp
