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

def print_team(team):
    team_url = f1_site + team.find('a').get('href')
    name = team.find("h2", {"class":"teamteaser-title"}).text.strip()
    stats = team.findAll("tr")
    podiums = stats[0].find("td", {"class":"stat-value"}).text.strip()

    team_page = connection(team_url)
    team_parsed = parser(team_page)
    team_info = team_parsed.find("div",{"class":"stats-list-component team-stats responsive-element"})
    team_drivers = team_parsed.findAll("figcaption",{"class":"driver-details"})

    team_table = team_info.find("table", {"class":"stat-list"})
    team_table = team_table.findAll('tr')

    f = open(name + ".csv", "w")

    for i in range(0,len(team_table)):
        f.write(team_table[i].find("th").text.strip() + ',' +  team_table[i].find("td", {"class":"stat-value"}).text.replace(",", " /") + '\n')
    f.write("Podium Finishes" + ',' + podiums + '\n')
    for j in range(0,len(team_drivers)):
        f.write('Driver ' + str(j+1) + ',')
        f.write(team_drivers[j].find("h1", {"class":"driver-name"}).text.strip() + ' #' + team_drivers[j].find("div", {"class":"driver-number"}).find('span').text + '\n')
    f.close()
    return

def print_driver(driver):
    driver_url = f1_site + driver.get('href')
    name = driver.find("h1", {"class":"driver-name"}).text.strip()
    number = driver.find("div", {"class":"driver-number"}).find('span').text

    driver_page = connection(driver_url)
    driver_parsed = parser(driver_page)
    driver_table = driver_parsed.find("table", {"class":"stat-list"})
    driver_table = driver_table.findAll('tr')

    f = open(name + ".csv", "w")

    f.write(name + ',' + str(number) + '\n')
    for i in range(0,len(driver_table)):
        f.write(driver_table[i].find("th").text.strip() + ',' +  driver_table[i].find("td", {"class":"stat-value"}).text.replace(",", " /") + '\n')
    f.close()
    return

f1_teams = 'https://www.formula1.com/en/championship/teams.html'
f1_drivers = 'https://www.formula1.com/en/championship/drivers.html'
f1_site = 'https://www.formula1.com'

#connections
F1_Teams_page = connection(f1_teams)
F1_Drivers_page = connection(f1_drivers)

#parse pages to html
teams_parsed = parser(F1_Teams_page)
drivers_parsed = parser(F1_Drivers_page)

#organize paths for data printing
change_dir('..')
root_dir = os.getcwd()
create_dir(root_dir + '/data')
change_dir('data')
atual_dir = os.getcwd()
create_dir(atual_dir + '/teams')
create_dir(atual_dir + '/drivers')

#grab all teams
teams = teams_parsed.findAll("section",{"class":"teamteaser"})

#grab all drivers
drivers = drivers_parsed.findAll("a",{"class":"driver-title driver-teaser"})

#analize every team
change_dir(atual_dir + '/teams')
for i in range(0,len(teams)):
    print_team(teams[i])

#analize every driver
change_dir(atual_dir + '/drivers')
for i in range(0,len(drivers)):
    print_driver(drivers[i])
