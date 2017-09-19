import os
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def connection(url):
    Con = uReq(url)
    page = Con.read()
    Con.close()
    return page

def parser(page):
    page_parsed = soup(page, "html.parser")
    return page_parsed

def change_dir(str):
   os.chdir(str)
   return

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return

year = input("Year: ")
f1_results = 'https://www.formula1.com/en/results.html/' + year + '/races.html'

print(f1_results)
