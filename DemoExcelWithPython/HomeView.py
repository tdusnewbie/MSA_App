#!/usr/bin/env python3

import datetime

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview

from ExportItemFile import *
from Model import BillInfoModel, Database
from NewItemView import NewItemDialog 
from NewTypeView import NewTypeDialog 
from AddBillView import AddBillDialog
from ShowDataView import ShowDataWindow
from ShowBillView import ShowBillDialog
from ShowUserView import ShowListUserDialog
from UserInfoView import UserInfoDialog


class HomeScreen(Frame):
    def __init__(self, parent, username):
        Frame.__init__(self, parent)
        self.parent = parent
        self.data = Database()
        self.userCreate = username
        self.drawScreen()

        self.linkAccelerator()
        
        date = datetime.datetime.now().date().strftime("%d-%m-%Y")
        self.listBill = self.data.getListBillAtDate(date)
        for bill in self.listBill:
            self.addBillIntoTree(bill)

    def linkAccelerator(self):
        if self.userCreate == "root":  
            self.bind_all("<Control-U>", self.onViewListUser)
            self.bind_all("<Control-l>", self.onViewActivityLog)

        self.bind_all("<Control-n>", self.onNewItem)
        self.bind_all("<Control-N>", self.onNewType)
        self.bind_all("<Control-q>", self.onQuit)
        self.bind_all("<Control-L>", self.onLogOut)

        self.bind_all("<Delete>",self.onDeleteBill)
        self.bind_all("<Control-A>", self.onAddBill)
        self.bind_all("<Control-v>", self.onViewItemTable)
        self.bind_all("<Control-V>", self.onViewBillTable)

    def drawScreen(self):
        self.pack(fill = BOTH, anchor = "w", expand = True, padx = 10, pady = 10)

        ########## Listing all Bills which has been created ###########
        layoutList = Frame(self)

        self.drawTreeOfBill(layoutList)

        layoutList.pack(side = LEFT, fill = BOTH, expand = True)

        ########## Create Menu for HomePage ##########

        self.menu = Menu(self.parent)
        self.parent.config(menu = self.menu)
        self.drawMenu(self.menu)
    
    def drawMenu(self, parent):
        # File Menu
        fileMenu = Menu(parent)

        newPopupMenu = Menu(fileMenu)
        newPopupMenu.add_command(label = "Thêm mặt hàng ...", command = self.onNewItem, accelerator = "Ctrl+N")
        newPopupMenu.add_command(label = "Thêm loại hàng ...", command = self.onNewType, accelerator = "Ctrl+Shift+N")
        fileMenu.add_cascade(label = "Thêm", menu = newPopupMenu)

        fileMenu.add_separator()

        exportPopupMenu = Menu(fileMenu)
        exportPopupMenu.add_command(label = "Xuất File Mặt Hàng", command = self.onExportExcelFile)
        exportPopupMenu.add_command(label = "Xuất File Đơn Hàng", command = self.onExportExcelBillFile)

        fileMenu.add_cascade(label = "Xuất File Excel", menu = exportPopupMenu)

        statPopupMenu = Menu(fileMenu)
        statPopupMenu.add_command(label = "Thống Kê Mặt Hàng", command = self.onViewItemTable, accelerator = "Ctrl+V")
        statPopupMenu.add_command(label = "Thống Kê Hóa Đơn", command = self.onViewBillTable, accelerator = "Ctrl+Shift+V")
        fileMenu.add_cascade(label = "Thống kê", menu = statPopupMenu)
        if self.userCreate == "root":
            fileMenu.add_command(label = "Xem nhật kí hoạt động", command = self.onViewActivityLog)
        
        fileMenu.add_separator()

        fileMenu.add_command(label = "Thoát", command = self.onQuit, accelerator = "Ctrl+Q")
        parent.add_cascade(label = "Tệp", menu = fileMenu, underline = 0)

        # User Menu
        userMenu = Menu(parent)
        userMenu.add_command(label = "Xem thông tin User", command = self.onViewInfo)
        if self.userCreate == "root":
            userMenu.add_command(label = "Danh sách các User", command = self.onViewListUser)

        userMenu.add_separator()

        userMenu.add_command(label = "Đăng xuất", command = self.onLogOut, accelerator = "Ctrl+Shift+L")
        parent.add_cascade(label = "User", menu = userMenu, underline = 0)

        # About Menu
        windowMenu = Menu(parent)
        windowMenu.add_command(label = "About", command = self.onAbout)
        parent.add_cascade(label = "Windows", menu = windowMenu, underline = 0  )

    def drawTreeOfBill(self,parent):
        listAttribute = ["Mặt hàng", "Loại hàng", "ID", "Số lượng xuất", "Thành giá", "Người tạo"]
        
        yScrollTree = Scrollbar(parent, orient = VERTICAL)
        xScrollTree = Scrollbar(parent, orient = HORIZONTAL)

        # Create Delete, Add and Edit Button
        layoutButton = Frame(parent)
        
        btnAddBill = Button(layoutButton, text = "+", fg = "green", command = self.onAddBill)
        btnDelBill = Button(layoutButton, text = "-", fg = "red", command = self.onDeleteBill)
        # btnEditBill = Button(layoutButton, text = "Edit", fg = "blue")

        btnAddBill.pack(side = LEFT)
        btnDelBill.pack(side = LEFT)
        # btnEditBill.pack(side = LEFT)
        
        layoutButton.pack(side = TOP, anchor = "w")

        # Create Tree View
        self.treeBill = Treeview(parent, column = listAttribute,
            yscrollcommand = yScrollTree.set, 
            xscrollcommand = xScrollTree.set
        )
        self.treeBill.bind(sequence="<Double-Button-1>",func=self.onEditBill)

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

    def onAddBill(self, event = None):
        AddBillDialog(self)

    def onEditBill(self, event):
        pass

    def onDeleteBill(self, event = None):
        # if len(self.treeBill.selection()) == 0:
        #     messagebox.showwarning(title = "Empty !!!", message = "Xin hãy chọn Hóa đơn bạn muốn xóa")
        #     return

        # for choose in self.treeBill.selection():
        #     treeItem = self.treeBill.item(choose)
            
        #     if treeItem["tags"][0] == "childs":
        #         self.data.deleteBillAtTime(treeItem["text"])
        #     elif treeItem["tags"][0] == "parents":
        #         self.data.deleteAllBillAtDate(treeItem["text"])
            
        #     self.treeBill.delete(treeItem["text"])
        messagebox.showerror("Opps !!!!","Bạn không thể xóa !!!!", parent = self)

    ######### Menu Function #####################
    def onExportExcelFile(self):
        self.filePath = filedialog.asksaveasfile(title = "Choose where you want to save File",
                                                    filetypes = (("Microsoft Excel","*.xlsx"),("All Files","*.*")))
        if self.filePath == None:
            return
        wb = Workbook()
        ws = wb.active

        data = Database()
        listItem = data.getItemList()

        for item in listItem:
            ws = createSheetAsItem(wb,item)
            createTitleTypeItem(ws, item)
            adjustColumn(ws)
            addTypeIntoSheet(ws,item.type)

        wb.remove_sheet(wb.active)
        wb.save(self.filePath.name)

    def onExportExcelBillFile(self):
        self.filePath = filedialog.asksaveasfile(title = "Choose where you want to save File",
                                                    filetypes = (("Microsoft Excel","*.xlsx"),("All Files","*.*")))
        if self.filePath == None:
            return
        wb = Workbook()
        ws = wb.active

        data = Database()
        listBill = data.getBillList()

        listDate = [listBill[0].CreatedDate]

        for bill in listBill:
            if bill.CreatedDate not in listDate:
                listDate.append(bill.CreatedDate)
        
        for date in listDate:
            listBillAtDate = data.getListBillAtDate(date)
            ws = createSheetAsDate(wb,date)
            createTitleBillInDate(ws,date)
            adjustColumn(ws)
            addBillIntoSheet(ws,listBillAtDate)

        wb.remove_sheet(wb.active)
        wb.save(self.filePath.name)

    def onViewItemTable(self, event = None):
        ShowDataWindow(self)

    def onViewBillTable(self, event = None):
        ShowBillDialog(self)

    def onQuit(self, event = None):
        exit()

    def onViewInfo(self):
        UserInfoDialog(self,self.userCreate)

    def onLogOut(self, event = None):
        self.destroy()
        self.menu.destroy()
        self.parent.geometry("400x400")
        self.parent.backToPreviousFrame()
        
    def onNewType(self,event = None):
        NewTypeDialog(self)

    def onNewItem(self,event = None):
        NewItemDialog(self)

    def onViewListUser(self, event = None):
        ShowListUserDialog(self)

    def onViewActivityLog(self, event = None):
        pass

    def onAbout(self):
        about = """
        Developer: Trần Dũng
        Tên Ứng dụng: Managing Selling App
        Version: 1.0
        Release: 06-01-2019
        """
        popup = Toplevel(self)
        popup.title("About")
        layoutAbout = Frame(popup)

        lblAbout = Label(layoutAbout, text = about)
        lblAbout.pack(side = TOP, fill= BOTH, expand = True)

        layoutAbout.pack(side = TOP, fill= BOTH, expand = True, padx = 10, pady = 10)


if __name__ == "__main__":
    root = Tk()
    root.geometry("700x400")
    root.update()
    home = HomeScreen(root,"tdusnewbie")

    root.mainloop()