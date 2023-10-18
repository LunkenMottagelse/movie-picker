import json
import webParser

def updateDataFile():
    dataDict = webParser.ParseImdb()
    with open("movieDB", "w") as fp:
        json.dump(dataDict , fp)

def requestDataFile():
    with open("movieDB", "r") as fp:
        dataDict = json.load(fp)
    return dataDict

updateDataFile()