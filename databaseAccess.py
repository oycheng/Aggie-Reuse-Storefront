
import numpy as np
import pandas as pd
import sqlite3 as sql

barCodeLength = 9

class Access:
    def __init__(self, dbName):
        self.dbName = dbName
        self.dataDf = pd.DataFrame()
    def _extract(self, location):
        dbConn = sql.connect(self.dbName)
        try:
            self.dataDf = pd.read_sql_query("SELECT * FROM `" + location + "`", con = dbConn)
        except:
            self.dataDf = pd.DataFrame()
        dbConn.close()
        
    def _dupCheck(self, barcode):
        if self.dataDf.empty:
            return
        database = self.dataDf.to_dict()
        barcodes = list(database["barcode"].values())
        if barcode in barcodes:
            return True
        else:
            return False
    def store(self, barcode, location):
        self._extract(location)
        if(not self._dupCheck(barcode)):
            data = {"barcode" : [barcode],
                    "reserved": ["false"]}
            inDataDf = pd.DataFrame(data)
            dbConn = sql.connect(self.dbName)
            try:
                inDataDf.to_sql(location, dbConn, if_exists='append', index = False)
            except ValueError as error:
                print("Failed to insert:", error)
            dbConn.commit()
            dbConn.close()
        else:
            print("item already exists")
    def removeItem(self, barcode, location):
        self._extract(location)
        if not self._dupCheck(barcode):
            print("Item not in inventory")
            return
        self._extract(location)
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        position = barcodes_val.index(barcode)
        for item, itemdata in data.items():
            itemdata.pop(position)
            data[item] = itemdata
        self._update(data, location)
    def reserve(self, barcode, location):
        if not self._dupCheck(barcode):
            print("Item does not exist")
            return
        self._extract(location)
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        position = barcodes_val.index(barcode)
        if data["reserved"][position] == "false":
            reserveId = input("reserve ID: ")
            data["reserved"][position] = reserveId
            self._update(data, location)
        else:
            print("Item " + barcode + " is reserved")
    def unreserve(self, barcode, location):
        if not self._dupCheck(barcode):
            print("Item does not exist")
            return
        self._extract(location)
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        position = barcodes_val.index(barcode)
        data["reserved"][position] = "false"
        self._update(data, location)
    def _update(self, newData, location):
        newDataDf = pd.DataFrame(newData)
        dbConn = sql.connect(self.dbName)
        newDataDf.to_sql(location, dbConn, if_exists='replace', index=False)
        dbConn.close()
    def printDf(self, location):
        self._extract(location)
        print(self.dataDf)

def Run():
    controls = ["quit", "show", "add", "remove", "reserve", "unreserve"]
    database = Access("someDB.db")
    location = "db"
    while True:
        control = "false"
        barIn = "false"
        while not control in controls:
            control = input("enter control: ")
        if control == controls[0]:
            break
        elif control == controls[1]:
            database.printDf(location)
        else:
            while (not barIn.isnumeric()) or (len(barIn) != barCodeLength):
                barIn = input("enter barcode: ")
                if barIn == "-1":
                    break
            if barIn == "-1":
                break
            if control == controls[2]:
                database.store(barIn, location)
            elif control == controls[3]:
                database.removeItem(barIn, location)
            elif control == controls[4]:
                database.reserve(barIn, location)
            elif control == controls[5]:
                database.unreserve(barIn, location)
                
if __name__ == "__main__":
    Run()