from .dataBase import Access
from .dataBase import Traffic
import logging
import math
import barcode
import random
import pandas
from config import databaseName, location


def store(databaseName: str, location: str, barcode, imgName, tags):
    name = "/dataBase/" + databaseName
    database = Access(databaseName)
    database.store(barcode, imgName, location, tagInput = tags)
    database.printDf(location)



def get_items(startIndex, endIndex, getTags, getPages, selectedTag):
    Barcode = []
    imgURL = []
    Tags = []
    TotalTags = []
    TotalNumber = 0
    pageSize = endIndex - startIndex

    name = "/dataBase/" + databaseName
    database = Access(databaseName)

    # get all barcode from database
    inventory = database.getBarcodes(location)

    if (getTags == "true"):
        # get total tags from dtatbase
        tags2D = database.getTags(location)

        for i in range(len(tags2D)):
            TotalTags += tags2D[i]

        TotalTags = list(set(TotalTags))
        TotalTags.remove("none")
    
    if (getPages == "true"):
        TotalNumber = math.ceil(len(inventory) / pageSize)

    currentIndex = startIndex
    count = 0
    while count < pageSize and currentIndex < len(inventory):
        currentTags = database.retrieveTags(inventory[currentIndex]) # get tags of current item from database
        
        if (selectedTag == "none" or hasTag(currentTags, selectedTag)):
            if (database.checkReserve(inventory[currentIndex], location) == -1):
                Barcode += [inventory[currentIndex]]
                imgURL += ["../../backend/service/dataBase/img/" + inventory[currentIndex] + ".png"]

                Tags += [currentTags]
                count += 1
        
        currentIndex += 1

    response = {"Barcode": Barcode, "imgURL": imgURL, "Tags": Tags, "TotalTags": TotalTags, "TotalNumber": TotalNumber}
    return response


def hasTag(currentTags, selectedTag):
    for i in range(len(currentTags)):
        if currentTags[i] == selectedTag:
            return True
    
    return False


def add_items(image, tags):
    random.seed()  # Initialize random number generator 
    barcode_number = ''.join(str(random.randint(0, 9)) for _ in range(9))
    print("[" + barcode_number +"]")
    print("[" + tags +"]")
    imgName = "service/dataBase/img/" + barcode_number + ".png"
    image.save(imgName)
    store(databaseName, location, barcode_number, imgName, tags)

    return 'success'


def reserve_items(barcodes):
    name = "/dataBase/" + databaseName
    database = Access(databaseName)
    for i in range(len(barcodes)):
        database.reserve(barcodes[i], location)


def unreserve_items(barcodes):
    name = "/dataBase/" + databaseName
    database = Access(databaseName)
    for i in range(len(barcodes)):
        database.unreserve(barcodes[i], location)