import pandas as pd
import sqlite3 as sql
import pickle
import datetime

barCodeLength = 9

class Access:
    def __init__(self, dbName = "storeDB.db"):
        self.dbName = dbName
        self.dataDf = pd.DataFrame()
    def _extract(self, location = "inventory"):
        dbConn = sql.connect(self.dbName)
        try:
            self.dataDf = pd.read_sql_query("SELECT * FROM `" + location + "`", con = dbConn)
        except:
            self.dataDf = pd.DataFrame()
        dbConn.close()
    def _dupCheck(self, barcode):
        if self.dataDf.empty:
            return False
        database = self.dataDf.to_dict()
        barcodes = list(database["barcode"].values())
        if barcode in barcodes:
            return True
        else:
            return False
    def _pickleTags(self, tagInput):
        tags = tagInput.split()
        return pickle.dumps(tags)
    def retrieveTags(self, barcode, location = "inventory"):
        self._extract(location)
        data = self.dataDf.to_dict()
        position = list(data["barcode"].values()).index(barcode)
        tag = pickle.loads(data["tags"][position])
        return tag
    def store(self, barcode, imageLink, location = "inventory", tagInput = "none none none none none"):
        self._extract(location)
        if(not self._dupCheck(barcode)):
            data = {"barcode" : barcode,
                    "tags" : [self._pickleTags(tagInput)],
                    "image" : [imageLink],
                    "reserved" : ["false"],
                    "reserve time" : ["false"]}
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
    def removeItem(self, barcode, location = "inventory"):
        self._extract(location)
        if not self._dupCheck(barcode):
            print("Item not in inventory")
            return
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        position = list(barcodes.values()).index(barcode)
        if(len(barcodes) == 1):
            dbConn = sql.connect(self.dbName)
            dbConn.cursor().execute("DROP TABLE " + location)
            dbConn.close()
        else:
            for item, itemdata in data.items():
                itemdata.pop(position)
                data[item] = itemdata
            self._update(data, location)
    def _update(self, newData, location = "inventory"):
        newDataDf = pd.DataFrame(newData)
        dbConn = sql.connect(self.dbName)
        newDataDf.to_sql(location, dbConn, if_exists='replace', index=False)
        dbConn.close()
    def reserve(self, barcode, reserveId = "123123123", location = "inventory"):
        self._extract(location)
        if not self._dupCheck(barcode):
            print("Item does not exist")
            return
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        position = barcodes_val.index(barcode)
        if data["reserved"][position] == "false":
            data["reserved"][position] = reserveId
            data["reserve time"][position] = datetime.datetime.now()
            self._update(data, location)
        else:
            print("Item " + barcode + " is reserved")
    def checkReserve(self, barcode, location = "inventory"):
        self._extract(location)
        if not self._dupCheck(barcode):
            print("Item does not exist")
            return -1
        data = self.dataDf.to_dict()
        barcodes = data["barcode"]
        barcodes_val = list(barcodes.values())
        position = barcodes_val.index(barcode)
        if data["reserved"][position] != "false":
            return -1
        return 0
    def unreserve(self, barcode, location = "inventory"):
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
    def printDf(self, location = "inventory"):
        self._extract(location)
        data = self.dataDf.to_dict()
        if bool(data):
            for key, pickleData in data["tags"].items():
                data["tags"][key] = pickle.loads(pickleData)
        print(data)
    def getBarcodes(self, location = "inventory"):
        self._extract(location)
        data = self.dataDf.to_dict()
        barcodes = list(data["barcode"].values())
        return barcodes
    def getTags(self, location = "inventory"):
        self._extract(location)
        data = self.dataDf.to_dict()
        tags = list()
        for pickedTags in list(data["tags"].values()):
            tags.append(pickle.loads(pickedTags))
        return tags
def Run():
    controls = ["quit", "show", "add", "remove", "reserve", "unreserve"]
    database = Access()
    while True:
        control = "false"
        barIn = "false"
        while not control in controls:
            control = input("enter control: ")
        if control == controls[0]:
            break
        elif control == controls[1]:
            database.printDf()
        else:
            while (not barIn.isnumeric()) or (len(barIn) != barCodeLength):
                barIn = input("enter barcode: ")
            if control == controls[2]:
                database.store(barIn)
            elif control == controls[3]:
                database.removeItem(barIn)
            elif control == controls[4]:
                database.reserve(barIn)
            elif control == controls[5]:
                database.unreserve(barIn)
                
if __name__ == "__main__":
    Run()