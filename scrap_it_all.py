# utf-8
# author: Aman Singh
# Last Editted Date: 08-Apr-2019


"""
[NOTE:]
start Webdriver for the respective browser.
Make sure, the Webdriver is run from the same PATH where the script is run
or where the python is residing.
"""
import time
from datetime import datetime
from config import Config as cfg
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import math

browser = webdriver.Chrome()  # replace with .Firefox() if using firefox's webdriver
url = cfg['url']['login_url']
browser.get(url)  # navigating to login page

columns = ['contract', 'awarded_to', 'consortium_companies', 'amount', 'currency', 'published_date', 'reference', 'funding_agencies', 'locations', 'sectors']
data = pd.DataFrame(columns=columns)

"""
Get the IDs/name of the form fields used for login
"""
username = browser.find_element_by_name("login_name")
password = browser.find_element_by_name("login_pwd")

username.send_keys(cfg['login']['username'])
password.send_keys(cfg['login']['password'])

loginButton = browser.find_element_by_name("login_btn")
loginButton.click()

"""
navigate to Contracts search page
"""
browser.get(cfg['url']['contracts_page_url'])  # contracts page
innerHTML = browser.execute_script("return document.body.innerHTML")

"""
fill-in search criteria and click on search
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
grab total search results, calculate total result pages (each page has 20 results shown)
get all the links for the search results
"""
result_page_url = browser.current_url
result_pg_html = browser.page_source
result_pg_soup = BeautifulSoup(result_pg_html, 'html.parser')
# total search results
total_results = int(result_pg_soup.find("div", attrs={"class": "row content"}).find("p").text.split()[2])
# total pages in search result
total_pages = math.ceil(total_results/20)
# navigation link for pages
results = browser.find_elements_by_tag_name("a")
navigation_link = []
for result in results:
    if '&act=contract&page=' in result.get_attribute("href"):
        lnk = result.get_attribute("href")[:-1]
        if len(navigation_link) < 1:
            navigation_link.append(lnk)
pagination_url_txt = navigation_link[0]

time.sleep(10)  # wait time

idx = 0
for n in range(1, total_pages + 1):
    url = pagination_url_txt + str(n)
    print('...scrapping results on page:', str(n))
    browser.get(url)

    results_on_page = []

    results = browser.find_elements_by_tag_name("a")

    navigation_link = []
    for result in results:
        if result.get_attribute("class") == "blue":
            results_on_page.append(result.get_attribute("href"))  # link to each search result

    for result in results_on_page:
        innerHTML = browser.get(result)

        html_doc = browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')

        """
        fields to fetch from tags:
        Contract-name, Contracted-companies, Amount, Currency, 
        Published-date, Reference, Funding-agent, Countries, Sectors"
        """
        row_content = soup.find("div", {"class": "row content"})
        contract_name = row_content.find('h4').get_text().strip()  # Contract-name

        contracted_companies_lst = []
        for item in row_content.find_all('td', attrs={"class": "title_list"}):
            if item:
                contracted_companies_lst.append(item.get_text().strip('\n\t'))  # Contracted-companies

        awarded_to = []
        consortium_companies = []
        for each in contracted_companies_lst:
            if 'in association with' in each:  # check for awardee
                awarded_to.append(' '.join(each.split()[:-3]))  # append to awarded_to removing last 3 words
            elif 'and' in each.split()[-1]:
                consortium_companies.append(' '.join(each.split()[:-1]))  # append to consortium-companies removing last word
            else:
                consortium_companies.append(' '.join(each.split()))  # append to consortium-companies as it is

        amount_lst = []
        currency_lst = []
        for item in soup.find_all('td', attrs={'class': 'budget2'}):
            if item.text.strip().replace('\xa0', ''):
                amount_lst.append(item.text.strip().replace('\xa0', '')[:-3])  # Amount
                if len(currency_lst) < 1:
                    currency_lst.append(item.text.strip().replace('\xa0', '')[-3:])  # Currency

        published_date = []
        column_history_active_content = soup.find("div", attrs={"class": "column history active"})
        if column_history_active_content:
            items = column_history_active_content.find_all("span")
        else:
            items = None
        if not items:
            items = soup.find("div", attrs={"class": "drawer active"}).find_all("p")
            for item in items:
                if 'Published' in item.text:
                    date_str = item.findNext("p").text.replace('\xa0', ' ')
                    published_date.append(datetime.strptime(date_str, '%d %B %Y').strftime('%d-%m-%Y'))
        else:
            for item in items:
                if 'Contract' in item.text:
                    date_str = item.findNext("span").text.strip()  # Contract-date
                    published_date.append(datetime.strptime(date_str, '%d %b %Y').strftime('%d-%m-%Y'))

        items = soup.find_all("p", {"class": "title"})
        procurement_type, reference, donors, locations = [], [], [], []
        for item in items:
            if 'Procurement type' in item.text:
                procurement_type.append(item.findNext('p').text)  # Procurement-type
            if 'Reference' in item.text:
                reference.append(item.findNext('p').text)  # Reference
            if 'Funding Agency' in item.text:
                donors.append(item.findNext('p').text)  # Funding-Agencies
            if 'Countries' in item.text:
                locations.append(item.findNext('p').text)  # Countries

        items = soup.find_all("div", {"class": "eleven columns"})
        sectors = []
        for item in items:
            for i in item.find_all("span", {"class": ""}):
                if str(i.text)[:2].isupper():  # check first two letters are upper case
                    sectors.append(i.text.split(':')[0])

        description_container = soup.find("table", attrs={"class": "notice"})
        description = description_container.find("p").get_text()

        data.loc[idx, 'contract'] = contract_name
        data.loc[idx, 'awarded_to'] = ';'.join(awarded_to)
        data.loc[idx, 'consortium_companies'] = ';'.join(consortium_companies)
        data.loc[idx, 'amount'] = ';'.join(amount_lst)
        data.loc[idx, 'currency'] = ';'.join(currency_lst)
        data.loc[idx, 'published_date'] = published_date[0]
        data.loc[idx, 'reference'] = reference[0]
        data.loc[idx, 'funding_agencies'] = ';'.join(donors)
        data.loc[idx, 'locations'] = ';'.join(locations)
        data.loc[idx, 'sectors'] = ';'.join(sectors)

        if idx == 0:
            data.to_csv(cfg['save_as']['file_name'], index=False, mode='w') # write to csv with column names
        else:
            data.to_csv(cfg['save_as']['file_name'], header=False, index=False, mode='a') # append to csv without column names

        browser.implicitly_wait(10)  # seconds
        print('search result ' + str(idx+1) + 'done.')

        idx = idx + 1
    time.sleep(10)  # wait-time in seconds