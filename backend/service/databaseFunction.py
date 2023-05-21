from .dataBase import Access
from .dataBase import Traffic
import math


def store(databaseName: str, location: str, barcode):
    name = "/dataBase/" + databaseName
    database = Access(databaseName)
    data = {"barcode" : [barcode], "price" : [10], "reserved": ["false"]}
    database.store(data, location)
    database.printDf(location)



def get_items(startIndex, endIndex, getTags, getPages, selectTag):
    Barcode = []
    imgURL = []
    Tags = []
    TotalTags = []
    TotalNumber = 0
    pageSize = endIndex - startIndex

    # get all barcode from database =====================================
    inventory = []

    if (getTags == "true"):
        # get total tags from dtatbase  =================================
        TotalTags = []
    
    if (getPages == "true"):
        TotalNumber = math.ceil(len(inventory) / pageSize)

    currentIndex = startIndex
    for i in range(pageSize):
        Barcode += [inventory[i]]
        imgURL += ["/img/" + inventory[i] + ".png"]
        currentTags = [] # get tags of current item from database =======

        Tags += [currentTags]

        

    response = {"Barcode": Barcode, "URL": imgURL "Tags": Tags, "TotalTags": TotalTags, "TotalNumber": TotalNumber}
    return response