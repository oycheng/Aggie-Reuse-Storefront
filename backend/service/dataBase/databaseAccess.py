
import numpy as np
import re
import pandas as pd
import sqlite3 as sql

class Access:
    def __init__(self, dbName):
        self.dbName = dbName
        self.dataDf = pd.DataFrame()
    def _extract(self, location):
        dbConn = sql.connect(self.dbName)
        try:
            dataDf = pd.read_sql_query("SELECT * FROM `" + location + "`", con = dbConn)
        except:
            dataDf = pd.DataFrame()
        dbConn.close()
        return dataDf
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
        self.dataDf = self._extract(location)
        inDataDf = pd.DataFrame(data)
        if(self._duplicateCheck(data)):
            dbConn = sql.connect(self.dbName)
            try:
                inDataDf.to_sql(location, dbConn, if_exists='append', index = False)
            except ValueError as error:
                print("Failed to insert:", error)
            dbConn.commit()
            dbConn.close()
    def reserve(self, barcode, location):
        data = self._extract(location)
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        position = barcodes_val.index(barcode)
        print(position)
    def _update(self, newDataDf, location):
        dbConn = sql.connect(self.dbName)
        newDataDf.to_sql(location, dbConn, if_exists='replace', index=False)
        dbConn.close()
    def printDf(self, location):
        print(self._extract(location))
        
if __name__ == "__main__":
    database = Access("someDB.db")
    location = "b"
    while True:
        barIn = "false"
        while not barIn.isnumeric():
            barIn = input("enter barcode: ")
            if barIn == "-1":
                break
        if barIn == "-1":
            break
        data = {"barcode" : [barIn],
                "price" : [10],
                "reserved": ["false"]}
        database.store(data, location)
        database.printDf(location)