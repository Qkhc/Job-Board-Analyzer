#!/usr/bin/env python
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
from selenium.webdriver.firefox.options import Options

#----------------------------------#
#         Selenium functions
def openFireFox(webBrowser):
    glassdoor = 'https://www.glassdoor.com/index.htm'
    webBrowser.get(glassdoor)

def jobTitle(webBrowser, title):
    jobSearch = webBrowser.find_element_by_id("sc.keyword")
    jobSearch.click()
    jobSearch.clear()
    jobSearch.send_keys(title)

def jobLocation(webBrowser, location):
    locationSearch = webBrowser.find_element_by_id("sc.location")
    locationSearch.click()
    locationSearch.clear()
    locationSearch.send_keys(location)

def getCompany(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f'li.jl:nth-child({num}) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1)').text
    except:
        return 'None'

def getJobTitle(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f'li.jl:nth-child({num}) > div:nth-child(2) > a:nth-child(2)').text
    except:
        return 'None'

def getJobLocation(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f"li.jl:nth-child({num}) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)").text
    except:
        return 'None'

def getJobSalary(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f"li.jl:nth-child({num}) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text
    except:
        return 'None'

def nextPage(webBrowser):
    webBrowser.find_element_by_css_selector(".next").click()

def main():
    options = Options()
    options.headless = True    
    webBrowser = webdriver.Firefox(options=options)
    # openFireFox(webBrowser)
    URL = "https://www.indeed.com/q-software-engineer-l-Valencia,-CA-jobs.html"
    webBrowser.get(URL)
    res = webBrowser.find_element_by_id('pj_083b886315193c53')
    print(res.text)
    res = res.find_element_by_class_name('company')
    print(res.text)

    # print(page.text)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # results = soup.find_all("div", id="tab-details")
    # print(des)
    # job = results.findAll("div", {"id": "pj_a9af049c355e31ab"})
    # for job in results:
    # print(results)
    webBrowser.quit()
if __name__ == '__main__':
    main()


# indeed id="jobDescriptionText" under auxCol
# indeed tr role = main
#td id = resultsCol
# div id = pj_123456789