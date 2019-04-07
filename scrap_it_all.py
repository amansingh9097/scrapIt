# utf-8
# author: Aman Singh
# Last Editted Date: 07-Apr-2019


"""
[NOTE:]
start Webdriver for the respective browser.
Make sure, the Webdriver is run from the same PATH where the script is run
or where the python is residing.
"""

from config import Config as cfg
from selenium import webdriver

browser = webdriver.Chrome() #replace with .Firefox() if using firefox's webdriver
url = cfg['url']['login_url']
browser.get(url) #navigating to login page

"""
[TODO: done]
Get the IDs/name of the form fields used for login
username form field--> login_name
password form field--> login_pwd
login button form field--> login_btn
"""
username = browser.find_element_by_name("login_name")
password = browser.find_element_by_name("login_pwd")

username.send_keys(cfg['login']['username'])
password.send_keys(cfg['login']['password'])

loginButton = browser.find_element_by_name("login_btn")
loginButton.click()

"""
[TODO: done]
click on Contracts
"""
browser.get(cfg['url']['contracts_page_url']) #contracts pgae
innerHTML = browser.execute_script("return document.body.innerHTML")

"""
[TODO: done]
fill-in search criterias and click on search
procurement type form field --> procurement_type
published from form field --> srch_sdate
published to form field -->  srch_edate
search button --> type='submit' and value='Search' (use xpath)
"""
filter_procurement_type = browser.find_element_by_name("procurement_type")
filter_published_from = browser.find_element_by_name("srch_sdate")
filter_published_to = browser.find_element_by_name("srch_edate")

filter_procurement_type.send_keys(cfg['search']['procurement_type'])
filter_published_from.send_keys(cfg['search']['published_from'])
filter_published_to.send_keys(cfg['search']['published_to'])

searchButton = browser.find_element_by_xpath('//input[@type="submit" and @value="Search"]')
searchButton.click()

"""
begin the scrapping
"""
