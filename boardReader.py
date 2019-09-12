#!/usr/bin/env python
import psycopg2
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from configparser import ConfigParser

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

#----------------------------------#
#           Database functions

def config(filename='database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    conn = None:
    try:
        params = config()
        print("Connecting to database.")
        return psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(Error)

def disconnect(connection):
    if connection is not None:
        conn.close()
        print("Disconnecting from database.")

#----------------------------------#

def main():

    # Open firefox with my profile so it is already logged in.
    profile = FirefoxProfile("/home/bobby/.mozilla/firefox/iwp41fb7.default")
    webBrowser = webdriver.Firefox(profile)
    openFireFox(webBrowser)

    # TODO: Add user input for job and location in future
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
