import os
import subprocess
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# fetches the HTML rendered at url and calls itself recursively for every link in the HTML fetched upto a depth of maxDepth
def fetchHtml(url, outputDir, filename, maxDepth):
    absFilename = os.path.join(outputDir, filename)
    links, linkTexts = None, None

    # This should be true for panchayat-level directory pages if we started by fetching a district-level directory page,
    # for example, the page with the list of blocks in Katihar district
    seleniumRequired = (INITIAL_MAX_DEPTH - maxDepth == 2)
    if seleniumRequired:
        print('Fetching via Selenium ' + absFilename)
        links, linkTexts = fetchHtmlViaSelenium(url, absFilename)
    else:
        print('Fetching ' + absFilename)
        process = subprocess.Popen(['wget', '-O', absFilename, url], stdout = logfile, stderr = logfile)
        process.communicate()
    
    if maxDepth == 0:
        # base case: we are at the leaf-level page and do not want to parse links or recurse further
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
        if not links[i].startswith('http'):
            # dealing with a relative URL not an absolute one
            links[i] = rootURL + links[i]
        fetchHtml(links[i], newDirname, linkTexts[i] + '.html', maxDepth - 1) 

# both loads the given url and parses out the links    
def fetchHtmlViaSelenium(url, absFilename):
    driver.get(url)
    linkElements = driver.find_elements(By.TAG_NAME, 'a')
    links = []
    linkTexts = []
    for elt in linkElements:
        hrefVal = elt.get_attribute('href')
        links.append(hrefVal)
        linkTexts.append(elt.text)
        # debug
        print('Link text', elt.text, 'points to', hrefVal)
    
    # driver.close()
    return (links, linkTexts)

# parses out links from the given html file
def extractLinks(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    linkTags = soup.find_all('a')
    links = []
    linkTexts = []
    for tag in linkTags:
        links.append(tag['href'])
        linkTexts.append(tag.string)
        # debug
        print('Link text:', tag.string)

    return (links, linkTexts)

# program parameters
rootDir = os.getcwd()
rootURL = 'https://mahadalitvikasmission.org/VMR/'
districtName = 'Sheohar' # used to name downloaded html file and wget log file
startURL = "BlockWiseDetailsUploaded.do?dt=205"
logfilename = districtName + '.log'
INITIAL_MAX_DEPTH = 4 # 4 is the maximum value if we start by fetching a district-level page, 5 if we are fetching the state-level page

# setup selenium webdriver
chromeDriverPath = '/home/madhavan.somanathan/Downloads/chromedriver_linux64/chromedriver' 
driver = webdriver.Chrome(executable_path = chromeDriverPath)

with open(logfilename, 'w') as logfile:
    fetchHtml(rootURL + startURL, rootDir, districtName + '.html', maxDepth = INITIAL_MAX_DEPTH)

# close selenium-driven browser window
driver.quit()

# end-of-file

