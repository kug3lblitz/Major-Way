from ast import literal_eval
from datetime import datetime
from os.path import abspath, dirname, join
from time import time

from wikipedia import WikipediaPage, exceptions

start = time()


def Majors():
    majors = ""

    # Dir is hardcoded
    BASEDIR = dirname(abspath(__file__))
    path = join(BASEDIR, "disciplines.txt")

    # Avoids issues with bytecodes
    try:
        with open(path, 'r') as inputFile:
            for i in range(sum(1 for line in open(path, 'r'))):
                lines = str(inputFile.readline())
                if "[" in lines:
                    majors += lines

    except IOError:
        exit("File does not exist.")

    return literal_eval(majors)


def GenerateData():
    majors = Majors()

    pages = []
    pageLinks = {}
    bigdata = []

    for i in majors:

        try:

            pages = WikipediaPage(i).links
            for j in range(len(pages)):
                try:
                    pages[j] = str(pages[j]).lower()
                except UnicodeError:
                    pages[j] = ""

            pageLinks[i] = sorted(list(set(pages)))

            bigdata.append(pageLinks)
            print "Generating database for", str(i) + "."
            pageLinks = {}

        except (IndentationError, StopIteration, exceptions.PageError) as e:
            print e
            continue

    return bigdata


def main():
    bigdata = GenerateData()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open("bigdata.txt", "w") as outputFile:
        outputFile.write("Last updated " + str(now) + "\n\n")
        outputFile.write(str(bigdata))


if __name__ == '__main__':
    main()

end = time()

print "Program took " + "{0:.3f}".format(
        (end - start)) + " seconds to generate data."
