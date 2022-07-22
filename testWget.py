import os
import re

'''
startURL = "https://mahadalitvikasmission.org/VMR/DistrictWiseDetailsUploaded.do"
rootURL = "https://mahadalitvikasmission.org/VMR/"

rootDir = os.getcwd()

stream = os.popen('wget -O ' + os.path.join(rootDir, "rootPage.html" + " " + startURL))
print(stream.read())
'''

rootDir = os.getcwd()
rootURL = "https://mahadalitvikasmission.org/VMR/"
startURL = "https://mahadalitvikasmission.org/VMR/BlockWiseDetailsUploaded.do?dt=212" 

stream = os.popen('wget -O ' + os.path.join(rootDir, "katihar.html") + " " + startURL)
print(stream.read())

stream = os.popen('grep href= katihar.html')
grepOutput = stream.read()

links = re.findall('href=".*"', grepOutput)
trimmedLinks = []

for link in links:
    trimmedLinks.append(link[len('href='):].strip('"'))

def fetchHtml(relativeURL, outputDir):
    filename = relativeURL.rsplit("=", maxsplit = 1)[-1]
    print('Fetching ' + relativeURL)
    stream = os.popen('wget -O ' + os.path.join(outputDir, filename) + " " + rootURL + relativeURL)

def extractLinks(filename):
    stream = os.popen('grep href= ' + filename)
    grepOutput = stream.read()
    links = re.findall('href=".*"', grepOutput)
    trimmedLinks = []
    trimmedLinks.append(link[len('href='):].strip('"'))
    return trimmedLinks

try:
    os.mkdir("blocks")
except FileExistsError:
    pass

for link in trimmedLinks:
    fetchHtml(link, "blocks")
    


'''
katiharLink = trimmedLinks[15]

stream = os.popen('wget -O ' + os.path.join(rootDir, "katiharDir.html" + " " + rootURL + katiharLink))
print(stream.read())

'''


