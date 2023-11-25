# filename: fetch_shse_index.py
import pandas as pd
from bs4 import BeautifulSoup
import requests

def fetch_shse_index():
    url = 'http://quotes.money.163.com/quote.html?code=000001&token=975668691752833888'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup is None:
        print("Failed to parse HTML content.")
        return None
    table = soup.find('table', attrs={'class': 'f-tb'})
    if table is None:
        print("Failed to find the table element.")
        return None
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    df = pd.DataFrame(data[1:], columns=data[0])
    df['date'] = pd.to_datetime(df['日期'], format='%Y%m%d')
    df.set_index('date', inplace=True)
    return df

df = fetch_shse_index()
if df is not None:
    print(df)
else:
    print("No dataframe was returned")