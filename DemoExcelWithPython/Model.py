#!/usr/bin/env python3
import sqlite3
import datetime

class BillInfoModel:
    def __init__(self, name = None, type = [], id = None,
                 price = None, amount = None, CreatedDate = None, 
                 CreatedTime = None, CreatedUser = None):
        self.name = name
        self.type = type
        self.id = id
        self.price = price
        self.amount = amount
        self.CreatedDate = CreatedDate
        self.CreatedTime = CreatedTime
        self.CreatedUser = CreatedUser


class Item:
    def __init__(self, name = None, typeItem = None, idItem = None):
        self.name = name
        self.type = typeItem
        self.id = idItem


class TypeItem:
    def __init__(self, name = None, amount = None, unitPrice = None, 
                idType = None, idParent = None):
        self.name = name
        self.amount = amount
        self.unitPrice = unitPrice
        self.idType = idType
        self.idParent = idParent


class User:
    def __init__(self, name = None, username = None, passWord = None):
        self.name = name
        self.username = username
        self.passWord = passWord


class Database:
    def __init__(self):
        self.data = sqlite3.connect("data.db")
        self.createTable()

    def createTable(self):
        cursor = self.data.cursor()
        # Create Table
        UserTable = """
        CREATE TABLE IF NOT EXISTS User(
            name TEXT,
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """
        
        ItemTable = """
        CREATE TABLE IF NOT EXISTS Item(
            name TEXT,
            id TEXT PRIMARY KEY
        )
        """

        TypeItemTable = """
        CREATE TABLE IF NOT EXISTS TypeItem(
            name TEXT,
            id TEXT PRIMARY KEY,
            amount INTEGER,
            unitPrice REAL,
            idParent TEXT
        )
        """

        BillTable = """
        CREATE TABLE IF NOT EXISTS Bill(
            itemName TEXT,
            typeName TEXT,
            amount INTEGER,
            price REAL,
            id TEXT,
            CreatedTime TEXT,
            CreatedDate TEXT,
            CreatedUser TEXT
        )
        """

        cursor.execute(UserTable)
        cursor.execute(ItemTable)
        cursor.execute(TypeItemTable)
        cursor.execute(BillTable)

    def insertUser(self, user):
        cursor = self.data.cursor()
        cursor.execute("INSERT INTO User (name, username, password) VALUES (?,?,?)",
                        (user.name, user.username, user.passWord))
        self.data.commit()
        cursor.close()
    
    def insertItem(self, item):
        cursor = self.data.cursor()
        cursor.execute("INSERT INTO Item (name, id) VALUES (?,?)",
                        (item.name, item.id))
        self.data.commit()
        cursor.close()

    def insertTypeItem(self, typeItem):
        cursor = self.data.cursor()
        cursor.execute("INSERT INTO TypeItem (name, id, amount, unitPrice, idParent) VALUES (?,?,?,?,?)",
                        (typeItem.name, typeItem.idType, int(typeItem.amount), float(typeItem.unitPrice), typeItem.idParent))
        self.data.commit()
        cursor.close()
   
    def insertBill(self,bill):
        cursor = self.data.cursor()
        cursor.execute("INSERT INTO Bill (itemName, typeName, amount, price, id, CreatedTime, CreatedDate, CreatedUser) VALUES (?,?,?,?,?,?,?,?)",
                        (bill.name, bill.type, bill.amount, bill.price, bill.id, bill.CreatedTime, bill.CreatedDate, bill.CreatedUser))
        self.data.commit()
        cursor.close()

    def getUserList(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT * FROM User")
        listUser = []
        for row in cursor.fetchall():
            user = User(name=row[0], username= row[1], passWord=row[2])
            listUser.append(user)
        
        return listUser
    
    def getUserInfo(self, username):
        cursor = self.data.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ?",(username,))
        user = User()
        for row in cursor.fetchall():
            temp = User(name=row[0], username= row[1], passWord=row[2])
            user = temp
        return user

    def getItemList(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT * FROM Item")
        listItem = []
        for row in cursor.fetchall():
            item = Item(name=row[0], idItem = row[1])
            typeList = self.getTypeItemList(item.id)
            item.type = typeList
            listItem.append(item)
        
        return listItem
    
    def getTypeItemList(self,idParent):
        cursor = self.data.cursor()
        cursor.execute("SELECT * FROM TypeItem WHERE idParent = ?",(idParent,))
        listType = []
        for row in cursor.fetchall():
            # print(row)
            typeItem = TypeItem(name = row[0], idType = row[1], amount = row[2], 
                                unitPrice = row[3], idParent = row[4])
            listType.append(typeItem)
        return listType
   
    def getBillList(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT * FROM Bill")
        listBill = []
        for row in cursor.fetchall():
            bill = BillInfoModel(name = row[0], type = row[1], amount = row[2],
                                price = row[3], id = row[4], CreatedTime = row[5],
                                CreatedDate = row[6], CreatedUser = row[7])
            listBill.append(bill)
        
        return listBill

    def getListBillAtDate(self,date):
        cursor = self.data.cursor()
        cursor.execute("SELECT * FROM Bill WHERE CreatedDate = ?",(date,))
        listBill = []
        for row in cursor.fetchall():
            bill = BillInfoModel(name = row[0], type = row[1], amount = row[2],
                                price = row[3], id = row[4], CreatedTime = row[5],
                                CreatedDate = row[6], CreatedUser = row[7])
            listBill.append(bill)
        return listBill

    def deleteBillAtTime(self, time):
        cursor = self.data.cursor()
        cursor.execute("DELETE FROM Bill WHERE CreatedTime = ?",(time,))
        self.data.commit()
        cursor.close()

    def deleteAllBillAtDate(self, date):
        cursor = self.data.cursor()
        cursor.execute("DELETE FROM Bill WHERE CreatedDate = ?",(date,))
        self.data.commit()
        cursor.close()

    def deleteType(self, idType):
        cursor = self.data.cursor()
        cursor.execute("DELETE FROM TypeItem WHERE id = ?",(idType,))
        self.data.commit()
        cursor.close()

    def deleteTypeWithIdParent(self, idParent):
        cursor = self.data.cursor()
        cursor.execute("DELETE FROM TypeItem WHERE idParent = ?",(idParent,))
        self.data.commit()
        cursor.close()

    def deleteItem(self, idItem):
        cursor = self.data.cursor()
        cursor.execute("DELETE FROM Item WHERE id = ?",(idItem,))
        self.deleteTypeWithIdParent(idItem)
        self.data.commit()
        cursor.close()

    def deleteUser(self, username):
        cursor = self.data.cursor()
        cursor.execute("DELETE FROM User WHERE username = ?",(username,))
        self.data.commit()
        cursor.close()

    def updateAmountOfType(self, idType, newAmount):
        cursor = self.data.cursor()
        cursor.execute("UPDATE TypeItem SET amount = ? WHERE id = ?",(newAmount,idType))
        self.data.commit()
        cursor.close()
    
    def updateNameOfType(self, idType, newName):
        cursor = self.data.cursor()
        cursor.execute("UPDATE TypeItem SET name = ? WHERE id = ?",(newName,idType))
        self.data.commit()
        cursor.close()
 
    def updateIdOfType(self, idType, newId):
        cursor = self.data.cursor()
        cursor.execute("UPDATE TypeItem SET id = ? WHERE id = ?",(newId,idType))
        self.data.commit()
        cursor.close()

    def updateUnitOfType(self, idType, newUnit):
        cursor = self.data.cursor()
        cursor.execute("UPDATE TypeItem SET unitPrice = ? WHERE id = ?",(newUnit,idType))
        self.data.commit()
        cursor.close()

    def updateNameOfuser(self, username, newName):
        cursor = self.data.cursor()
        cursor.execute("UPDATE User SET name = ? WHERE username = ?",(newName,username))
        self.data.commit()
        cursor.close()
    
    def updatePassOfUser(self, username, newPass):
        cursor = self.data.cursor()
        cursor.execute("UPDATE User SET passWord = ? WHERE username = ?",(newPass,username))
        self.data.commit()
        cursor.close()

    def updateUsernameOfUser(self, username, newUsername):
        cursor = self.data.cursor()
        cursor.execute("UPDATE User SET username = ? WHERE username = ?",(newUsername,username))
        self.data.commit()
        cursor.close()

# data = Database()
# for i in range(10):
#     user = User(name="user"+ str(i), username="u"+str(i),passWord="123456")
#     data.insertUser(user)
# user = User("user0", "u0","123456")
# if user not in data.getUserList():
#     print("Not In")
# else:
#     print("In")