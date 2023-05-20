
import numpy as np
import re
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
    def _duplicateCheck(self, data):
        if self.dataDf.empty:
            return True
        database = self.dataDf.to_dict()
        barcodes = list(database["barcode"].values())
        if data["barcode"][0] in barcodes:
            return False
        else:
            return True
    def store(self, data, location):
        self._extract(location)
        inDataDf = pd.DataFrame(data)
        if(self._duplicateCheck(data)):
            dbConn = sql.connect(self.dbName)
            try:
                inDataDf.to_sql(location, dbConn, if_exists='append', index = False)
            except ValueError as error:
                print("Failed to insert:", error)
            dbConn.commit()
            dbConn.close()
        else:
            print("item already exists")
    def reserve(self, barcode, location):
        self._extract(location)
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        try:
            position = barcodes_val.index(barcode)
        except ValueError as error:
            return
        print(data["reserved"][position])
        if data["reserved"][position] == "false":
            data["reserved"][position] = "true"
            self._update(data, location)
        elif data["reserved"][position] == "true":
            print("Item " + barcode + " is reserved")
        else:
            print("error")
    def _update(self, newData, location):
        newDataDf = pd.DataFrame(newData)
        dbConn = sql.connect(self.dbName)
        newDataDf.to_sql(location, dbConn, if_exists='replace', index=False)
        dbConn.close()
    def printDf(self, location):
        self._extract(location)
        print(self.dataDf)
        
if __name__ == "__main__":
    controls = ["add", "reserve"]
    database = Access("someDB.db")
    location = "e"
    while True:
        control = "false"
        barIn = "false"
        while not control in controls:
            control = input("enter control: ")
        while (not barIn.isnumeric()) or (len(barIn) != barCodeLength):
            barIn = input("enter barcode: ")
            if barIn == "-1":
                break
        if barIn == "-1":
            break
        if control == controls[0]:
            data = {"barcode" : [barIn],
                    "price" : [10],
                    "reserved": ["false"]}
            database.store(data, location)
        elif control == controls[1]:
            database.reserve(barIn, location)
        
        database.printDf(location)