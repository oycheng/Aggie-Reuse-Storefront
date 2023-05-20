
import numpy as np
import re
import pandas as pd
import sqlite3 as sql

class Access:
    def __init__(self, dbName):
        self.dbConn = sql.connect(dbName)
        self.cursor = self.dbConn.cursor()
    def __del__(self):
        self.dbConn.close()
    def extract(self):
        dataDf = pd.read_sql_query("SELECT * FROM `inventory`", con = self.dbConn)
        return dataDf
class Store:
    def __init__(self, dbName):
        self.dbConn = sql.connect(dbName)
        self.cursor = self.dbConn.cursor()
    def store(self, data):
        dataDF = pd.DataFrame(data)
        try:
            dataDF.to_sql("inventory", self.dbConn, if_exists='append', index = False)
        except ValueError as error:
            print("Failed to insert:", error)
        self.dbConn.commit()
    def __del__(self):
        self.dbConn.close()


if __name__ == "__main__":
    while True:
        barIn = "false"
        while not barIn.isnumeric():
            barIn = input("enter barcode: ")
            if barIn == "-1":
                break
        if barIn == "-1":
            break
        data = {"barcode" : [barIn]}

        store = Store("someDB.db")
        store.store(data)

        extract = Access("someDB.db")
        print(extract.extract())
    