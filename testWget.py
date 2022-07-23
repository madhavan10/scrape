import os
import sys
import re
from bs4 import BeautifulSoup

'''
startURL = "https://mahadalitvikasmission.org/VMR/DistrictWiseDetailsUploaded.do"
rootURL = "https://mahadalitvikasmission.org/VMR/"

rootDir = os.getcwd()

stream = os.popen('wget -O ' + os.path.join(rootDir, "rootPage.html" + " " + startURL))
print(stream.read())
'''

def fetchHtml(relativeURL, outputDir, filename, maxDepth):
    absFilename = os.path.join(outputDir, filename)
    print('Fetching ' + absFilename)
    stream = os.popen('wget -w 5 -O ' + '\''+ absFilename + '\'' + " " + rootURL + relativeURL)
    exitStatus = stream.close()
    if exitStatus is not None:
        sys.exit('EXIT STATUS IS NOT NONE')

    
    if maxDepth == 0:
        return

    temp = extractLinks(absFilename)
    links, linkTexts = temp[0], temp[1]
    newDirname = os.path.join(outputDir, filename.split('.', 1)[0])
    try:
        os.mkdir(newDirname)
    except FileExistsError:
        pass
    for i, link in enumerate(links):
        fetchHtml(links[i], newDirname, linkTexts[i] + '.html', maxDepth - 1) 
    


def extractLinks(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    linkTags = soup.find_all('a')
    links = []
    linkTexts = []
    for tag in linkTags:
        links.append(tag['href'])
        linkTexts.append(tag.string)
        print(tag.string)

    return (links, linkTexts)

rootDir = os.getcwd()
rootURL = 'https://mahadalitvikasmission.org/VMR/'
startURL = "BlockWiseDetailsUploaded.do?dt=212" 


fetchHtml(startURL, rootDir, 'katihar.html', maxDepth = 3)


'''


for file in os.listdir():
    split = file.rsplit('.', 1)
    if split[-1] != 'html':
        continue
    temp = extractLinks(file)
    links, linkTexts = temp[0], temp[1]
    try:
        os.mkdir(split[0])
    except FileExistsError:
        pass
    for i, link in enumerate(links):
        fetchHtml(links[i], split[0], linkTexts[i] + '.html')


try:
    os.mkdir("blocks")
except FileExistsError:
    pass

for link in trimmedLinks:
    fetchHtml(link, "blocks")

stream = os.popen('grep href= katihar.html')
grepOutput = stream.read()
links = re.findall('href=".*"', grepOutput)
trimmedLinks = []
for link in links:
    trimmedLinks.append(link[len('href='):].strip('"'))


katiharLink = trimmedLinks[15]

stream = os.popen('wget -O ' + os.path.join(rootDir, "katiharDir.html" + " " + rootURL + katiharLink))
print(stream.read())

'''


