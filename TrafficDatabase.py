import pandas as pd
import sqlite3 as sql
import numpy as np

class Traffic:
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
    def store(self, time, location):
        data = {"entry time" : [time],
                "reserved": ["false"]}
        inDataDf = pd.DataFrame(data)
        dbConn = sql.connect(self.dbName)
        try:
            inDataDf.to_sql(location, dbConn, if_exists='append', index = False)
        except ValueError as error:
            print("Failed to insert:", error)
        dbConn.commit()
        dbConn.close()
    