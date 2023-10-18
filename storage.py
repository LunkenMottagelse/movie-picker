import json
import webParser

def updateDataFile():
    dataDict = webParser.ParseImdb()
    with open("movieDB.json", "w") as fp:
        json.dump(dataDict , fp)

def requestDataFile():
    with open("movieDB.json", "r") as fp:
        dataDict = json.load(fp)
    return dataDict


# updateDataFile()