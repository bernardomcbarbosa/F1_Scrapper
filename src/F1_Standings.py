import bs4
import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

f1_url = 'https://www.formula1.com/en/results.html/2017/drivers.html'

def change_dir(str):
   os.chdir(str)
   return

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return

#open connection
Con = uReq(f1_url)

#read website
F1_page = Con.read()

#close connection
Con.close()

#organize paths for data printing
change_dir('..')
root_dir = os.getcwd()
create_dir(root_dir + '/data')
change_dir('data')
atual_dir = os.getcwd()
create_dir(atual_dir + '/results')

#parse to html
F1_parsed = soup(F1_page, "html.parser")

#grab drivers
drivers = F1_parsed.findAll("tr")

#grab header
header = drivers[0].findAll('th')

#open file 
change_dir(atual_dir + '/results')
f = open("F1_Standings.csv", "w")

#print header
for i in range(1,len(header)-1):
    if i != len(header)-2 :
        f.write(header[i].text + ',')
    else:
        f.write(header[i].text + '\n')


#print drivers standings
for i in range(1, len(drivers)):

    position = drivers[i].find("td", {"class":"dark"}).text

    refs = drivers[i].findAll("a")
    first_name = refs[0].find("span", {"class":"hide-for-tablet"}).text.strip()
    last_name = refs[0].find("span", {"class":"hide-for-mobile"}).text.strip()
    name = first_name + ' ' + last_name

    nationality = drivers[i].find("td", {"class":"dark semi-bold uppercase"}).text

    car = refs[1].text.strip()

    points = drivers[i].find("td", {"class":"dark bold"}).text

    f.write(position + ',' +  name + ',' + nationality + ',' + car + ',' + points + '\n')

f.close()
