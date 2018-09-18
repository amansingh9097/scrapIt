import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.pickuplinesgalore.com/cheesy.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
# # print(r.text[0:500])

results = soup.find_all('span', {'class': 'paragraph-text-7'})
# results = soup.find_all('li')

# first_result = results[2].text
# print(first_result)
# print(len(first_result.split()))
# print(first_result.split()[0])

records = []
for result in results:
    records.append(result.text)

# # when there's pagination
# for page in range(2, 48):
#     time.sleep(2)
#     url = 'http://pickup-lines.net/page/{}/'.format(page)
#     print("...scrapping lines from url: {}".format(url))
#     r2 = requests.get(url)
#     soup2 = BeautifulSoup(r2.text, 'html.parser')
#
#     results2 = soup2.find_all('span', {'class': 'loop-entry-line'})
#     for result in results2:
#         records.append(result.text)

print(len(records))
df = pd.DataFrame(records, columns=['NERDY_PICKUP_LINES'])
df.to_csv('pickuplines.csv', index=False, encoding='utf-8')
