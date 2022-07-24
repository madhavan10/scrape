import os
import sys
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fetchHtml(relativeURL, outputDir, filename, maxDepth):
    absFilename = os.path.join(outputDir, filename)
    seleniumRequired = (INITIAL_MAX_DEPTH - maxDepth == 2)
    links, linkTexts = None, None
    if seleniumRequired:
        print('Fetching via Selenium ' + absFilename)
        links, linkTexts = fetchHtmlViaSelenium(relativeURL, absFilename)
    else:
        print('Fetching ' + absFilename)
        stream = os.popen('wget -O ' + '\''+ absFilename + '\'' + " " + rootURL + relativeURL)
        exitStatus = stream.close()
        if exitStatus is not None:
            sys.exit('EXIT STATUS IS NOT NONE')
    
    if maxDepth == 0:
        return
    
    newDirname = os.path.join(outputDir, filename.rsplit('.', 1)[0])
    try:
        os.mkdir(newDirname)
    except FileExistsError:
        pass
    
    if not seleniumRequired:
        temp = extractLinks(absFilename)
        links, linkTexts = temp[0], temp[1]
    
    for i, link in enumerate(links):
        fetchHtml(links[i], newDirname, linkTexts[i] + '.html', maxDepth - 1) 
    
def fetchHtmlViaSelenium(relativeURL, absFilename):
    driver.switch_to.new_window('tab')
    driver.get(rootURL + relativeURL)
    linkElements = driver.find_elements(By.TAG_NAME, 'a')
    links = []
    linkTexts = []
    for elt in linkElements:
        links.append(elt.getAttribute('href'))
        linkTexts.append(elt.text)
    
    driver.close()
    return (links, linkTexts)

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
INITIAL_MAX_DEPTH = 3

# setup selenium webdriver
chromeDriverPath = r"C:\Users\madha\chromedriver.exe"
driver = webdriver.Chrome(executable_path = chromeDriverPath)

fetchHtml(startURL, rootDir, 'katihar.html', maxDepth = INITIAL_MAX_DEPTH)


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


