import bs4
import os
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

def print_header(f,header):
    for i in range(1,len(header)-1):
        if i != len(header)-2 :
            f.write(header[i].text + ',')
        else:
            f.write(header[i].text + '\n')
    return

def print_drivers_standings(drivers):
    drivers_table = drivers.findAll("tr")
    #grab header
    header = drivers_table[0].findAll('th')

    #open file
    f = open("F1_Driver_Standings.csv", "w")

    #print header
    print_header(f,header)

    for i in range(1, len(drivers_table)):

        position = drivers_table[i].find("td", {"class":"dark"}).text

        refs = drivers_table[i].findAll("a")
        first_name = refs[0].find("span", {"class":"hide-for-tablet"}).text.strip()
        last_name = refs[0].find("span", {"class":"hide-for-mobile"}).text.strip()
        name = first_name + ' ' + last_name

        nationality = drivers_table[i].find("td", {"class":"dark semi-bold uppercase"}).text

        car = refs[1].text.strip()

        points = drivers_table[i].find("td", {"class":"dark bold"}).text

        f.write(position + ',' +  name + ',' + nationality + ',' + car + ',' + points + '\n')
    f.close()
    return

def print_teams_standings(teams):
    teams_table = teams.find("table", {"class":"resultsarchive-table"}).findAll('tr')
    #grab header
    header = teams_table[0].findAll('th')

    #open file
    f = open("F1_Constructor_Standings.csv", "w")

    #print header
    print_header(f,header)

    for i in range(1, len(teams_table)):

        position = teams_table[i].find("td", {"class":"dark"}).text
        name = teams_table[i].find("a").text.strip()
        points = teams_table[i].find("td", {"class":"dark bold"}).text

        f.write(position + ',' +  name + ',' + points + '\n')
    f.close()
    return


drivers_url = 'https://www.formula1.com/en/results.html/2017/drivers.html'
teams_url = 'https://www.formula1.com/en/results.html/2017/team.html'

#connections
Teams_page = connection(teams_url)
Drivers_page = connection(drivers_url)

#parse pages to html
teams_parsed = parser(Teams_page)
drivers_parsed = parser(Drivers_page)

#organize paths for data printing
change_dir('..')
root_dir = os.getcwd()
create_dir(root_dir + '/data')
change_dir('data')
atual_dir = os.getcwd()
create_dir(atual_dir + '/results')
change_dir(atual_dir + '/results')

#print drivers
print_drivers_standings(drivers_parsed)
print_teams_standings(teams_parsed)
