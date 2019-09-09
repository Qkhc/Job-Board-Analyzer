#!/usr/bin/env python
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile

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

def getCompany(webBrowser):
    return webBrowser.find_element_by_css_selector(".jobInfoItem.jobEmpolyerName").text

def getJobTitle(webBrowser):
    return webBrowser.find_element_by_css_selector(".jobTitle.h2.strong").text

def getJobLocation(webBrowser):
    return webBrowser.find_element_by_css_selector(".jobInfoItem.empLoc").text

def getJobSalary(webBrowser):
    return webBrowser.find_element_by_css_selector(".salaryText").text

def main():
    profile = FirefoxProfile("/home/bobby/.mozilla/firefox/iwp41fb7.default")
    webBrowser = webdriver.Firefox(profile)
    openFireFox(webBrowser)
    jobTitle(webBrowser, "Software Engineer")
    jobLocation(webBrowser, "Santa Cruz, CA")
    submit = webBrowser.find_element_by_id("HeroSearchButton").click()

    print(getCompany(webBrowser))
    print(getJobTitle(webBrowser))
    print(getJobLocation(webBrowser))
    print(getJobSalary(webBrowser))

if __name__ == '__main__':
    main()
