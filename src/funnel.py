from ast import literal_eval
from itertools import chain
from json import dump
from operator import itemgetter
from sys import exit
from time import time

from os.path import abspath, dirname, join
from re import I, M, S  # regex flags
from re import compile

# from bs4 import BeautifulSoup

from database.wikipedia import WikipediaPage

start = time()

'''
Imports parsed PDF text.

Input:None
Output: text -> data as string
'''


def FileIO():
    text = ""
    fileName = raw_input("File name: ")

    # Dir is hardcoded
    BASEDIR = dirname(abspath(__file__))
    path = join(BASEDIR, "samples", str(fileName) + ".txt")

    # Avoids issues with bytecodes
    try:
        with open(path, 'r') as inputFile:
            for i in range(sum(1 for line in open(path, 'r'))):
                lines = str(inputFile.readline())
                text += lines

    except IOError:
        exit(str(fileName) + ".txt does not exist.")

    return text


class Funnel(object):
    '''
    Scans through the text to funnel out all relevant data.
    '''

    def __init__(self, text):

        self._text = self._Gunk(text)

    def _Gunk(self, text):

        '''
        Removes irrelevant data to improve content predicting accuracy

        Input:
        None

        Output:
        None
        '''

        gunkPat = compile(r'academic integrity.*\n\n|attendance.*\n\n',
                          I | M | S)
        gunk = gunkPat.findall(text)

        text = text.replace("".join(gunk), "")

        return text

    def FossilFuel(self, options=4):

        '''
        Concept tagging function. Compares parsed data with terminology
        corresponding to a vast list of disciplines.

        Input:
        None

        Output:
        subfields -> list of tuples, containing the subfield and the
        corresponding number of matches.
        '''

        # Imports the data populated by database/weekee.py as a list of
        # dictonaries

        subfieldsData = BigData()

        # Compares keywords in text with imported database, O(n*len(m)*len(k))

        bigList = {}  # Temporary containers
        keys = {}

        if isinstance(self._text, basestring):
            self._text = self._text.split(" ")

        for i in range(len(subfieldsData)):
            values = set(list(chain(*subfieldsData[i].values()))) \
                     & set(self._text)  # intersection of sets

            if values:
                keys[str(" ".join(subfieldsData[i].keys()))] = len(values)
                bigList.update(keys)
                keys = {}

        # Sorts list of tuples in reverse
        minedList = sorted(bigList.items(), key=itemgetter(1), reverse=True)

        # Container to store the maximum 'options' number of options
        maxCounter = []

        for i in minedList:
            maxCounter.append(i[1])

        maxCounter = sorted(set(maxCounter), reverse=True)

        subfields = []

        for i in range(len(minedList)):
            if set(minedList[i]) & set(maxCounter[:options]):
                subfields.append(maxCounter.index(minedList[i][1]) + 1)
                subfields.append(minedList[i][0])

        subfields = zip(subfields[0::2], subfields[1::2])

        subfields = sorted(subfields, key=lambda x: (x[0], x[1]))

        return subfields


def BigData(topic=""):
    # Imports the data populated by database/weekee.py as a list of dictonaries

    subfieldsData = ""

    BASEDIR = dirname(abspath(__file__))
    path = join(BASEDIR, "database", "bigdata.txt")  # Dir is hardcoded

    try:
        with open(path, 'r') as inputFile:
            # Avoids issues with bytecodes
            for i in range(sum(1 for line in open(path, 'r'))):
                lines = str(inputFile.readline())
                if "[" in lines:
                    subfieldsData += lines

    except IOError:
        exit("File does not exist.")

    # Convert file string to Python object (list of dictionaries)
    subfieldsData = literal_eval(subfieldsData)

    if topic:

        return [d.values() for d in subfieldsData if d.keys() == topic][0][0]

    else:

        return subfieldsData


def Disciplines(topic=""):
    # Imports the data populated by database/weekee.py as a list of dictonaries

    disciplines = ""

    BASEDIR = dirname(abspath(__file__))
    path = join(BASEDIR, "database", "disciplines.txt")  # Dir is hardcoded

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


def Hook(parsed):
    disciplines = Disciplines()

    topicsTest = {}
    topics = []

    for i in disciplines:
        if i in parsed.lower():
            try:
                summary = str(WikipediaPage(i).summary)
                summary = Funnel(summary).FossilFuel(2)[:5]
                summary = [i[1] for i in summary]
                topics.extend(summary)
            except:
                continue

    return topics


def Digiorno(topics):
    pie = {}
    counter = 0

    for i in topics:
        pie[i] = float(
                "{0:.2f}".format(float(topics.count(i)) / len(topics) * 100))

    counter = sum(pie.values())

    with open('data.json', 'w') as outfile:
        dump(pie, outfile)

    return pie


########## FOR SPRINKLER ############
# def Sprinkler(url):
# 	DB_URL = "http://dbpedia.org/page/" + str(url)
#
# 	htmlPat = compile('xmlns:ns1="http://www.w3.org/ns/prov#"'
# 					  '.*'
# 					  '<!-- footer -->', I | S | M)
#
# 	try:
# 		import requests
# 		getData = requests.get(DB_URL).text
#
# 	except requests.ConnectionError:
# 		exit("You forgot to turn your Wi-Fi on.")
#
# 	except:
#
# 		try:
# 			print "Requests library not found. Using urllib2."
#
# 			import urllib2
# 			getData = urllib2.urlopen(DB_URL).read()
#
# 		except urllib2.URLError:
# 			exit("Check your internet connection!")
#
# 	htmldata = findall(htmlPat, getData)
#
# 	majors = []
#
# 	soup = BeautifulSoup(" ".join(htmldata), "html.parser")
#
# 	for tag in soup.findAll(attrs={'class': 'uri'}):
# 		try:
# 			tags = str(tag.contents[1]).replace(':', '').replace('_', ' ')
# 			majors.append(tags)
# 		except:
# 			continue
#
# 	disciplines = [i for i in sorted(set(majors))]
# 	disciplines = [i for i in disciplines if i.lower() not in i]
#
# 	return disciplines


########## FOR TESTING ############

# parsed = FileIO()
# # predictList = Funnel(parsed).FossilFuel(5)[:5]
# # print predictList
# parsed = Hook(parsed)
# print Digiorno(parsed)

# predictList = [i[1] for i in predictList]

# user = str(raw_input("\nWhich one? "))

# choice = []

# while user:
# 	if user in predictList:
# 		choice.append(user)
# 		user = str(raw_input("\nWhich one? "))
# 	else:
# 		user = str(raw_input("\nWhich one mofo? "))

# print BigData(choice)

# DSurl = "Category:Data_structures"
# EEurl = "Category:Electrical_engineering"

# print "DS", Sprinkler(DSurl)
# print "EE", Sprinkler(EEurl)

end = time()

print "\nProgram took " + "{0:.3f}".format(
        (end - start)) + " seconds to generate data."
