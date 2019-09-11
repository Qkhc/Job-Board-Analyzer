#!/usr/bin/env python
import time
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

def getCompany(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f'li.jl:nth-child({num}) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1)').text
    except:
        return "0"

def getJobTitle(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f'li.jl:nth-child({num}) > div:nth-child(2) > a:nth-child(2)').text
    except:
        return "0"

def getJobLocation(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f"li.jl:nth-child({num}) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)").text
    except:
        return "0"

def getJobSalary(webBrowser, num):
    try:
        return webBrowser.find_element_by_css_selector(f"li.jl:nth-child({num}) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text
    except:
        return "0"

def nextPage(webBrowser):
    webBrowser.find_element_by_css_selector(".next").click()

def main():
    profile = FirefoxProfile("/home/bobby/.mozilla/firefox/iwp41fb7.default")
    webBrowser = webdriver.Firefox(profile)
    openFireFox(webBrowser)
    jobTitle(webBrowser, "Software Engineer")
    jobLocation(webBrowser, "San Jose, CA")
    submit = webBrowser.find_element_by_id("HeroSearchButton").click()

    pageNum = 1
    while True:

        print("--------------------------------")
        print(f"Page {pageNum}")
        print()
        for i in range(1,34):
            print(getCompany(webBrowser, i))
            print(getJobTitle(webBrowser, i))
            print(getJobLocation(webBrowser, i))
            print(getJobSalary(webBrowser, i))
            print()
        try:
            nextPage(webBrowser)
            pageNum +=1
        except:
            break
        print(f"Total Pages: {pageNum}")

if __name__ == '__main__':
    main()
