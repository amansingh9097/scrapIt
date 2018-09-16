import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('http://www.kamilagornia.com/35-funny-pick-up-lines-marketing-nerds/')
soup = BeautifulSoup(r.text, 'html.parser')
print(r.text[0:500])

results = soup.find_all('p')
# first_result = results[2].text
# print(first_result)
records = []
for result in results:
    records.append(result.text)

df = pd.DataFrame(records, columns=['NERDY_PICKUP_LINES'])
# df1 = pd.read_csv('nerdy_pickuplines.csv')
# df1.append(df)
# df1.to_csv('pickuplines.csv', index=False, encoding='utf-8')
print(df.head(15))
