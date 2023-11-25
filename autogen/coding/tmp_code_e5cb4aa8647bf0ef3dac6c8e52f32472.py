from bs4 import BeautifulSoup
import requests

def parse_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for title in titles:
        print(title.text)

parse_webpage('https://www.example.com')  # 替换为您想要解析的网址