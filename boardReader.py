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
    descriptions = []
    companies = results.find_elements_by_class_name('company')
    titles = results.find_elements_by_class_name("title")
    for i in range(len(companies)):
        try:
            driver.execute_script("arguments[0].click();", titles[i])
            time.sleep(1)
            driver.switch_to.frame('vjs-container-iframe')
            time.sleep(0.5)
            jobDes = driver.find_element_by_xpath('//*[@id="jobDescriptionText"]')
            descriptions.append(jobDes.text.lower())
            driver.switch_to.default_content()
        except Exception as e:
            descriptions.append("")
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
        job = job.split()
        new_job_list = list(dict.fromkeys(job)) # Removes duplicates
        for word in new_job_list:
            if word in wordCounter:
                wordCounter[word] +=1
    return wordCounter

# Display the graph in sorted order, with language names at the bottom.
def displayGraph(wordCounter, title, location, pages):
    labels, values = zip(*(wordCounter.most_common()))
    y_pos = np.arange(len(wordCounter))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, labels, rotation=90)
    plt.title(title + " in " + location)
    plt.ylabel("Occurances over " + str(pages) + " page(s). ")
    plt.xlabel('Languages')
    plt.savefig('graph.jpg', bbox_inches='tight')
    plt.show()

# Create the counter
# Look through the job descriptions and count the words
# remove entries with 0 count
# return the counter
def doAnalysis(descriptions):
    wordCounter = createLanguageCounter('languages.txt')
    wordCounter = getWordCount(wordCounter, descriptions)
    wordCounter += Counter() # Removes 0 elements
    return wordCounter

# Go through the number of pages and get each job description. 
def startSearch(webBrowser, numPages, verbose):
    descriptions = []
    # Go through the next n-1 pages and get each job info
    for i in range(0, numPages):
        print("---------- Page " + str(i + 1) + " starting. ----------")
        resultsCol = webBrowser.find_element_by_id('resultsCol')
        companies2, titles2, descriptions2 = getInfo(webBrowser, resultsCol)
        descriptions += descriptions2
        if verbose:
            printPageInfo(companies2, titles2, descriptions2)
        nextPage = webBrowser.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/nav/div/ul/li[6]")
        webBrowser.execute_script("arguments[0].click();", nextPage)
        print("---------- Page " + str(i + 1) + " finished. ----------\n")
    return descriptions

# Prints the help info. 
def help():
    print("Usage: boardReader.py [-h] [-v] [-n number] -l=<location> -t=<title>")
    print("------------------------------------")
    print(f"{'Long arg':<12} {'Short arg':<12} {'With value':<12}")
    print("------------------------------------")
    print(f"{'--title':<12} {'-t':<12} {'yes':<12}")
    print(f"{'--location':<12} {'-l':<12} {'yes':<12}")
    print(f"{'--number':<12} {'-n':<12} {'yes':<12}")
    print(f"{'--verbose':<12} {'-v':<12} {'no':<12}")
    print(f"{'--help':<12} {'-h':<12} {'no':<12}")
    print("------------------------------------")

def main(argv):
    titleSearch = "Software+Engineer"
    title = "Software Engineer"
    locationSearch = "San+Jose+CA"
    location = "San Jose CA"
    numPages = 1
    verbose = False
    
    # Get command line args
    try:
        opts, args = getopt.getopt(argv, "vht:l:n:", ["verbose", "help", "title=", "location=", "number="])  
    except Exception as e:
        print("Usage: boardReader.py [-v] [-n number] -l=<location> -t=<title>")
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        # Job title
        if opt in ("-t", "--title"):
            title = arg
            titleSearch = arg.split()
            titleSearch = "+".join(titleSearch)
        # Job location
        elif opt in ('-l', '--location'):
            location = arg
            locationSearch = arg.split()
            locationSearch = "+".join(locationSearch)
        # Number of pages
        elif opt in ('-n', '--number'):
            numPages = int(arg)
        elif opt in ('-v', "--verbose"):
            verbose = True
        elif opt in ('-h', '--help'):
            help()
            sys.exit(2)

    # Start firefox browser and go to indeed.com and search for a job
    options = Options()
    options.headless = True    
    webBrowser = webdriver.Firefox(options=options)
    URL = "https://www.indeed.com/jobs?q=" + titleSearch + "&l=" + locationSearch
    webBrowser.get(URL)
    print("Getting job info for " + title + " in " + location + " across " + str(numPages) + " pages.")
    
    # Get all the job descriptions across all pages. 
    descriptions = startSearch(webBrowser, numPages, verbose)

    # Go through each description and count the words. 
    wordCounter = doAnalysis(descriptions)
    if verbose:
        print(wordCounter)
    # Save the graph to 'graph.jpg' for viewing. 
    displayGraph(wordCounter, title, location, numPages)
    webBrowser.quit()

if __name__ == '__main__':
    main(sys.argv[1:])