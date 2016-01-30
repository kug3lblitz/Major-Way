from bs4 import BeautifulSoup
from datetime import datetime
from re import compile, findall
from re import I, M, S  # regex flags
from sys import exit


def Majors():

	bioPat = compile('<h3><span class="mw-headline" id="Biology">'
		'.*'
		'<li><a href="/wiki/Planetary_science" title="Planetary science">Planetary science</a>', I|S|M)

	formalPat = compile('<div class="hatnote relarticle mainarticle">Main article: <a href="/wiki/Formal_science" title="Formal science">Formal science</a></div>'
		'.*'
		'<li><a href="/wiki/World-systems_theory" title="World-systems theory">World-systems theory</a></li>', I|S|M)

	try:
		import requests
		getData = requests.get('https://en.wikipedia.org/wiki/Outline_of_academic_disciplines').text

	except requests.ConnectionError:
		exit("You forgot to turn your Wi-Fi on.")

	except:

		try:			
			print "Requests library not found. Using urllib2."

			import urllib2
			getData = urllib2.urlopen('https://en.wikipedia.org/wiki/Outline_of_academic_disciplines').read()

		except urllib2.URLError:
			exit("Check your internet connection!")

	htmldata = list(
		findall(bioPat, getData) +
		findall(formalPat, getData)
		)

	parentPat = compile('<h3><span class="mw-headline".*</span><s', I)

	parentsData = findall(parentPat, ' '.join(htmldata))

	grandparents = []
	parents = []

	childrenPat = compile('">\D+</span>', I)

	for i in parentsData:
		i = str(i)
		grandparents.extend(findall(childrenPat, i))

	for i in grandparents:
		i = i.replace('">', '')
		i = i.replace('</span>', '')
		parents.append(i)

	majors = []

	soup = BeautifulSoup(" ".join(htmldata), "html.parser")
	for tag in soup.findAll('a', href = True):
		try:
			# if str(tag['title']) in parents:
			print str(tag['title'])
			majors.append(str(tag['title']))
		except:
			continue

	disciplines = [i.lower() for i in majors]
	disciplines = [i for i in disciplines if not any(c.isdigit() for c in i)]
	disciplines = [i for i in disciplines if "list" not in i]
	disciplines = [i for i in disciplines if "edit" not in i]
	disciplines = [i for i in disciplines if "outline" not in i]
	disciplines = [i for i in disciplines if "wikipedia" not in i]
	disciplines = [i for i in disciplines if "portal" not in i]
	disciplines = [i for i in disciplines if "timeline" not in i]
	disciplines = [i for i in disciplines if "the arts" not in i]

	return disciplines


# def Adopted():



def main():

	data = Majors()

	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	with open("disciplines.txt", "w") as outputFile:
		outputFile.write("Last updated " + str(now) + "\n\n")
		outputFile.write(str(data))

if __name__ == '__main__':
    main()
    print "Found", len(Majors()), "disciplines."