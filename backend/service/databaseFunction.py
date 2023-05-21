from .dataBase import Access

def store(databaseName: str, location: str, barcode):
    name = "/dataBase/" + databaseName
    database = Access(databaseName)
    data = {"barcode" : [barcode], "price" : [10], "reserved": ["false"]}
    database.store(data, location)
    database.printDf(location)