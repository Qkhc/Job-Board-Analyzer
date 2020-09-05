#!/usr/bin/env python
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
from selenium.webdriver.firefox.options import Options
import time
#----------------------------------#
#         Selenium functions

def getInfo(results):
    companies = results.find_elements_by_class_name('company')
    titles = results.find_elements_by_class_name("title")

    return companies, titles

def printPageInfo(driver, companies, titles):
    
    for i in range(len(companies)):
        print("\n----------- JOB " + str(i+1) + " DESCRIPTION--------------\n")
        print(companies[i].text)
        print(titles[i].text.split("\n")[0] + "\n")
        companies[i].click()
        driver.switch_to.frame('vjs-container-iframe')
        time.sleep(3)
        jobDes = driver.find_element_by_xpath('//*[@id="jobDescriptionText"]')
        print(jobDes.text)
        driver.switch_to.default_content()

def main():
    options = Options()
    options.headless = True    
    webBrowser = webdriver.Firefox(options=options)
    URL = "https://www.indeed.com/jobs?q=software+engineer&l=San+Jose%2C+CA"
    webBrowser.get(URL)
    
    resultsCol = webBrowser.find_element_by_id('resultsCol')
    companies, titles = getInfo(resultsCol)

    printPageInfo(webBrowser, companies, titles)
      
    webBrowser.quit()

    
if __name__ == '__main__':
    main()


# indeed id="jobDescriptionText" under auxCol
# indeed tr role = main
#td id = resultsCol
# div id = pj_123456789