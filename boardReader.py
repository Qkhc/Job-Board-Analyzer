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


def main():
    profile = FirefoxProfile("/home/bobby/.mozilla/firefox/iwp41fb7.default")
    webBrowser = webdriver.Firefox(profile)
    openFireFox(webBrowser)
    jobTitle(webBrowser, "Software Engineer")
    jobLocation(webBrowser, "San Jose, CA")
    submit = webBrowser.find_element_by_id("HeroSearchButton").click()

if __name__ == '__main__':
    main()
