import json
from itertools import chain
from json import dump
from operator import itemgetter
from sys import exit
from time import time

from bs4 import BeautifulSoup
from database.wikipedia import WikipediaPage
from os.path import abspath, dirname, join
from re import I, M, S  # regex flags
from re import compile
from ast import literal_eval

def main():
    finalValues = [['biology',0],['chemistry',0],['physics',0],['earth science',0],['space science',0],['formal science',0],['mathematics',0],['computer science',0],['logic',0],['statistics',0],['systems science',0]]

    finalDict = dict()
    finalDict['biology'] = 0
    finalDict['chemistry'] = 0
    finalDict['physics'] = 0
    finalDict['earth science'] = 0
    finalDict['space science'] = 0
    finalDict['formal science'] = 0
    finalDict['mathematics'] = 0
    finalDict['computer science'] = 0
    finalDict['logic'] = 0
    finalDict['statistics'] = 0
    finalDict['systems science'] = 0

    
#    for key, value in finalDict.items():
#        if key == "biology":
#            print (value)
    perc1 = 0
    
   
    items1 = open('data.json','r')
    itemStr = items1.read()
    
    itemsJson = json.loads(itemStr)
#    for u in itemsJson:
 #       print(u)
 #       print(itemsJson[u])
 #       perc1 += float(itemsJson[u])
 #   print ("hiihhihih")
 #   print(perc1)
    dictList = Disciplines()
    perc = float(0)
    for n in itemsJson:
        flag1 = False
        flag2 = False
        for key, value in dictList.items():
            for p in value:
                if flag2 == True:
                    break
                if p == n:
                    print(key)
                    finalDict[key] = float(finalDict[key]) + float(itemsJson[n])
                    perc += float(itemsJson[n])
                    print(itemsJson[n])
                    flag2 = True
                    flag1 = True
    print(perc)
#                    for key1, value1 in finalDict.items():
 #                       if key1 == key:
                            
  #                  print(key)
                
        
#    print(itemsJson['ecology'])

    print(finalDict)
    fout1 = open("data1.json",'w')
    fout1.write("{")
            
    fout1.write('"')
    fout1.write("biology")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["biology"]))
    fout1.write(",")
    
    fout1.write('"')
    fout1.write("chemistry")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["chemistry"]))
    fout1.write(",")
    
    fout1.write('"')
    fout1.write("physics")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["physics"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("earth science")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["earth science"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("space science")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["space science"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("formal science")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["formal science"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("mathematics")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["mathematics"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("computer science")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["computer science"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("logic")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["logic"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("statistics")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["statistics"]))
    fout1.write(",")

    fout1.write('"')
    fout1.write("systems science")
    fout1.write('"')
    fout1.write(":")
    fout1.write(str(finalDict["systems science"]))

    fout1.write("}")

    
    fout1.close()
    
def Disciplines(topic=""):
    # Imports the data populated by database/weekee.py as a list of dictonaries

    disciplines = ""

    BASEDIR = dirname(abspath(__file__))
    path = join(BASEDIR, "disciplines1.txt")  # Dir is hardcoded

    try:
        with open(path, 'r') as inputFile:
            # Avoids issues with bytecodes
            for i in range(sum(1 for line in open(path, 'r'))):
                lines = str(inputFile.readline())
                if "[" in lines:
                    disciplines += lines

    except IOError:
        exit("File does not exist.")

    # Convert file string to Python object (list of dictionaries)
    disciplines = literal_eval(disciplines)

    return disciplines

main()
#items2 = json.loads(items1)

#print(string(items2))
