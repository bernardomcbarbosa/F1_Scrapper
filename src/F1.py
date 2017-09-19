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

def print_team(team):
    team_url = f1_site + team.find('a').get('href')
    stats = team.findAll("tr")
    podiums = stats[0].find("td", {"class":"stat-value"}).text.strip()
    titles = stats[1].find("td", {"class":"stat-value"}).text.strip()

    team_page = connection(team_url)
    team_parsed = parser(team_page)
    team_info = team_parsed.findAll("div",{"class":"stats-list-component team-stats responsive-element"})
    #team_drivers = team_parsed.findAll("div",{"class":"fom-adaptiveimage"})

    #team_info = team_info.findAll("tr")

    print(team_info)
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

#change directory for data printing
change_dir('..')
change_dir('data')
#print(os.getcwd())

#grab all teams
teams = teams_parsed.findAll("section",{"class":"teamteaser"})

#analize every team
"""
for i in range(0,len(teams)):
    print_team(teams[i])
    """
print_team(teams[0])


#f = open("F1_Drivers.csv", "w")
#f.close()
