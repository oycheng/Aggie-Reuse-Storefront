import pandas as pd
import sqlite3 as sql

class Traffic:
    def __init__(self, dbName = "storeDB.db"):
        self.dbName = dbName
        self.dataDf = pd.DataFrame()
    def retrieve(self, location = "traffic"):
        dbConn = sql.connect(self.dbName)
        try:
            self.dataDf = pd.read_sql_query("SELECT * FROM `" + location + "`", con = dbConn)
        except:
            self.dataDf = pd.DataFrame()
        dbConn.close()
    def store(self, time, location = "traffic"):
        data = {"entry time" : [time]}
        inDataDf = pd.DataFrame(data)
        dbConn = sql.connect(self.dbName)
        try:
            inDataDf.to_sql(location, dbConn, if_exists='append', index = False)
        except ValueError as error:
            print("Failed to insert:", error)
        dbConn.commit()
        dbConn.close()
        
    