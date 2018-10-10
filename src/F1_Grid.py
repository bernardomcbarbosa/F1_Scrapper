import os
import bs4
import requests
from bs4 import BeautifulSoup as soup

def connection(url):
    HEADER = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    response = requests.get(url, headers=HEADER, timeout=5)
    page_parsed = soup(response.content, "html.parser")
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
    team_info = team_page.find("div",{"class":"stats-list-component team-stats responsive-element"})
    team_drivers = team_page.findAll("figcaption",{"class":"driver-details"})

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

    print(name + ' ✓')
    return

def print_driver(driver):
    driver_url = f1_site + driver.get('href')
    name = driver.find("h1", {"class":"driver-name"}).text.strip()
    number = driver.find("div", {"class":"driver-number"}).find('span').text

    driver_page = connection(driver_url)
    driver_table = driver_page.find("table", {"class":"stat-list"})
    driver_table = driver_table.findAll('tr')

    f = open(name + ".csv", "w")

    f.write(name + ',' + str(number) + '\n')
    for i in range(0,len(driver_table)):
        f.write(driver_table[i].find("th").text.strip() + ',' +  driver_table[i].find("td", {"class":"stat-value"}).text.replace(",", " /") + '\n')
    f.close()

    print(name + ' ✓')
    return

f1_teams = 'https://www.formula1.com/en/championship/teams.html'
f1_drivers = 'https://www.formula1.com/en/championship/drivers.html'
f1_site = 'https://www.formula1.com'

#connections
F1_Teams_page = connection(f1_teams)
F1_Drivers_page = connection(f1_drivers)

#organize paths for data printing
change_dir('..')
root_dir = os.getcwd()
create_dir(root_dir + '/data')
change_dir('data')
atual_dir = os.getcwd()
create_dir(atual_dir + '/teams')
create_dir(atual_dir + '/drivers')

#grab all teams
teams = F1_Teams_page.findAll("section",{"class":"teamteaser"})

#grab all drivers
drivers = F1_Drivers_page.findAll("a",{"class":"driver-title driver-teaser"})

#analize every team
print('------ Teams ------')
change_dir(atual_dir + '/teams')
for i in range(0,len(teams)):
    print_team(teams[i])

#analize every driver
print('------ Drivers ------')
change_dir(atual_dir + '/drivers')
for i in range(0,len(drivers)):
    print_driver(drivers[i])
