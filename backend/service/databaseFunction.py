from .dataBase import Access
from .dataBase import Traffic
import logging
import math
import barcode
import random
from config import databaseName, location


def store(databaseName: str, location: str, barcode, tags):
    name = "/dataBase/" + databaseName
    database = Access(databaseName)
    database.store(barcode, tagInput = tags)
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
        imgURL += ["/dataBase/img/" + inventory[i] + ".png"]
        currentTags = [] # get tags of current item from database =======

        Tags += [currentTags]



    response = {"Barcode": Barcode, "URL": imgURL, "Tags": Tags, "TotalTags": TotalTags, "TotalNumber": TotalNumber}
    return response


def add_items(image, tags):
    random.seed()  # Initialize random number generator 
    barcode_number = ''.join(str(random.randint(0, 9)) for _ in range(9))
    print("[" + barcode_number +"]")
    print("[" + tags +"]")
    imgName = "service/dataBase/img/" + barcode_number + ".png"
    image.save(imgName)
    store(databaseName, location, barcode_number, tags)

    return 'success'