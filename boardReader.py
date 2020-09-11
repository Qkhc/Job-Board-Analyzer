#!/usr/bin/env python
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
from selenium.webdriver.firefox.options import Options
import time
from collections import Counter
import re
#----------------------------------#
#         Selenium functions

# Pull the info from the browser
# Returns a list of companies and titles elements
# as well as the job description text
def getInfo(driver, results):
    companies = results.find_elements_by_class_name('company')
    titles = results.find_elements_by_class_name("title")
    descriptions = []
    print("Getting job descriptions")
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

def createLanguageCounter(fileLocation):
    wordCounter = Counter()
    with open(fileLocation, 'r') as languageFile:
        for line in languageFile:
            wordCounter[line.lower().rstrip()] = 0
    languageFile.close()
    return wordCounter

def getWordCount(wordCounter, descriptions):
    for job in descriptions:
        job = re.sub(r"[,.;@#?!&$/]+\ *", " ", job)
        for word in job.split():
            if word in wordCounter:
                wordCounter[word] +=1
    return wordCounter
def main():
    options = Options()
    options.headless = True    
    webBrowser = webdriver.Firefox(options=options)
    URL = "https://www.indeed.com/jobs?q=software+engineer&l=San+Jose%2C+CA"
    webBrowser.get(URL)
    
    resultsCol = webBrowser.find_element_by_id('resultsCol')
    companies, titles, descriptions = getInfo(webBrowser, resultsCol)
    #  maybe pages = [(companies, titles, descriptions)]
    printPageInfo(companies, titles, descriptions)
    wordCounter = createLanguageCounter('languages.txt')
    wordCounter = getWordCount(counter, descriptions)
    print(wordCounter)
    webBrowser.quit()

    
if __name__ == '__main__':
    main()


# indeed id="jobDescriptionText" under auxCol
# indeed tr role = main
#td id = resultsCol
# div id = pj_123456789