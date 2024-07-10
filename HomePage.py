import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://results.eci.gov.in/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

def fetchHTMLDataandsave(url,path):
    req = requests.get(url,headers=headers)
    with open(path, "w") as filedata:
        filedata.write(req.text)


with open("scrappedData/eci.html","r") as data:
    html_doc = data.read()

soup = BeautifulSoup(html_doc, "html.parser")
# print(soup.prettify())


# Find the main tag
main_tag = soup.find('main')

# Find all a tags within the main tag
href_list = []
if main_tag:
    links = main_tag.find_all('a')
    hrefs = [link.get('href') for link in links]

    # Print all hrefs
    for href in hrefs:
        href_list.append(href)
        # print(href)
else:
    print("Main tag not found")

# print(href_list)
    
fetchHTMLDataandsave(url,"scrappedData/eci.html")


