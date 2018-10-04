import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = '' #enter the URL here
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
# # print(r.text[0:500])

results = soup.find_all('span', {'class': 'paragraph-text-7'})
# results = soup.find_all('li')

records = []
for result in results:
    records.append(result.text)

""" whenever there's pagination, use the below code block """
# for page in range(2, 48):
#     time.sleep(2)
#     url = 'THE-URL/{}/'.format(page)
#     print("...scrapping lines from url: {}".format(url))
#     r2 = requests.get(url)
#     soup2 = BeautifulSoup(r2.text, 'html.parser')
#
#     results2 = soup2.find_all('span', {'class': 'loop-entry-line'})
#     for result in results2:
#         records.append(result.text)

print(len(records))
df = pd.DataFrame(records, columns=['SCRAPED_LINES'])
df.to_csv('scrappedLines.csv', index=False, encoding='utf-8')
