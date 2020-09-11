#!/usr/bin/env python
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
from selenium.webdriver.firefox.options import Options
import time
from collections import Counter
import re
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt, mpld3
import sys, getopt


# Pull the info from the browser
# Returns a list of companies and titles elements
# as well as the job description text
def getInfo(driver, results):
    companies = results.find_elements_by_class_name('company')
    titles = results.find_elements_by_class_name("title")
    descriptions = []
    for i in range(len(companies)):
        try:
            titles[i].click()
            time.sleep(.5)
            driver.switch_to.frame('vjs-container-iframe')
            time.sleep(1.5)
            jobDes = driver.find_element_by_xpath('//*[@id="jobDescriptionText"]')
            descriptions.append(jobDes.text.lower())
            driver.switch_to.default_content()
        except Exception as e:
            driver.switch_to.default_content()
            print("******* Error getting job " + str(i))
            print(e)
            continue

    return companies, titles, descriptions

# Print the company, job title, and the job description for a single page. 
def printPageInfo(companies, titles, descriptions):
    for i in range(len(companies)):
        try:
            print("\n----------- JOB " + str(i+1) + " DESCRIPTION--------------\n")
            print(companies[i].text)
            print(titles[i].text.split("\n")[0] + "\n")
            print(descriptions[i])
        except Exception as e:
            print("******* Error printing job " + str(i))
            print(e)
            continue

# Take an input file and make a counter initilized to 0 for each word in the languages file. 
def createLanguageCounter(fileLocation):
    wordCounter = Counter()
    with open(fileLocation, 'r') as languageFile:
        for line in languageFile:
            wordCounter[line.lower().rstrip()] = 0
    languageFile.close()
    return wordCounter

# Traverse each job description for keywords. 
def getWordCount(wordCounter, descriptions):
    for job in descriptions:
        job = re.sub(r"[,.;@#?!&$/]+\ *", " ", job)
        for word in job.split():
            if word in wordCounter:
                wordCounter[word] +=1
    return wordCounter

# Display the graph in sorted order, with language names at the bottom.
def displayGraph(wordCounter, title, location):
    labels, values = zip(*(wordCounter.most_common()))
    y_pos = np.arange(len(wordCounter))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, labels, rotation=60)
    plt.tight_layout()
    plt.title(title + " in " + location)
    plt.ylabel('Occurances')
    plt.xlabel('Languages')
    plt.show()

def main(argv):
    titleSearch = []
    locationSearch = []
    try:
        opts, args = getopt.getopt(argv, "t:l:")
    except Exception as e:
        print("boardReader.py -t [title] -l [location]")
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-t':
            titleSearch = arg.split()
            titleSearch = "+".join(titleSearch)
        if opt == '-l':
            locationSearch = arg.split()
            locationSearch = "+".join(locationSearch)

    

    options = Options()
    options.headless = True    
    webBrowser = webdriver.Firefox(options=options)
    URL = "https://www.indeed.com/jobs?q=" + titleSearch + "&l=" + locationSearch
    webBrowser.get(URL)
    
    resultsCol = webBrowser.find_element_by_id('resultsCol')
    
    print("Getting job info for " + titleSearch + " in " + locationSearch)
    companies, titles, descriptions = getInfo(webBrowser, resultsCol)

    wordCounter = createLanguageCounter('languages.txt')
    wordCounter = getWordCount(wordCounter, descriptions)
    
    wordCounter += Counter() # Removing 0 elements
    print(wordCounter)

    displayGraph(wordCounter, titleSearch, locationSearch)
    webBrowser.quit()

    
if __name__ == '__main__':
    main(sys.argv[1:])


# indeed id="jobDescriptionText" under auxCol
# indeed tr role = main
#td id = resultsCol
# div id = pj_123456789