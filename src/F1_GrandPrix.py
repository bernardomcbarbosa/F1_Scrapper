import os
import bs4
from multiprocessing import Process
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def connection(url):
    Con = uReq(url)
    page = Con.read()
    Con.close()
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

def print_race_results(race):
    race_url = f1_site + race.find('a').get('href')
    name = race.find('a').text

    race_page = connection(race_url)
    race_table = race_page.find("table", {"class":"resultsarchive-table"}).findAll('tr')

    #grab header
    header = race_table[0].findAll('th')

    #open file
    f = open(name + ".csv", "w")

    #print header
    print_header(f,header)

    #print table
    for i in range(1,len(race_table)):
        driver_table = race_table[i].findAll('td')
        for j in range(1,len(header)-1):
            if j == len(header)-2:
                f.write(driver_table[j].text + '\n')
            elif j!=3:
                f.write(driver_table[j].text + ',')
            else:
                f.write(driver_table[j].find("span", {"class":"hide-for-tablet"}).text + ' ' + driver_table[j].find("span", {"class":"hide-for-mobile"}).text + ',')
    f.close()
    return

def print_grand_prix(i,grand_prix):
    grand_prix_url = f1_site + grand_prix.find('a').get('href')
    name = grand_prix.find('a').find("span", {"class":"clip"}).text

    #organize paths for data printing
    path = atual_dir + '/' + str(i) + ' - ' + name
    create_dir(path)
    change_dir(path)

    gp_page = connection(grand_prix_url)
    grand_prix_results = gp_page.findAll("li", {"class":"side-nav-item"})

    for i in range(1,len(grand_prix_results)):
        print_race_results(grand_prix_results[i])

    print(name + ' ✓')
    return

def print_standings(name,table,driver):
    #grab header
    header = table[0].findAll('th')

    #open file
    f = open(name + ".csv", "w")

    #print header
    print_header(f,header)

    #print table
    for i in range(1,len(table)):
        element_table = table[i].findAll('td')
        for j in range(1,len(header)-1):
            if j == len(header)-2:
                f.write(element_table[j].text.strip() + '\n')
            elif (j==2 and driver==1):
                f.write(element_table[j].find("span", {"class":"hide-for-tablet"}).text.strip() + ' ' + element_table[j].find("span", {"class":"hide-for-mobile"}).text.strip() + ',')
            else:
                f.write(element_table[j].text.strip() + ',')
    f.close()
    print(name + ' ✓')
    return

year = input("Year: ")
f1_results = 'https://www.formula1.com/en/results.html/' + year + '/races.html'
drivers_url = 'https://www.formula1.com/en/results.html/' + year + '/drivers.html'
teams_url = 'https://www.formula1.com/en/results.html/' + year + '/team.html'
f1_site = 'https://www.formula1.com'

#connections and parse pages to html
f1_page = connection(f1_results)
drivers_page = connection(drivers_url)
teams_page = connection(teams_url)

#grab all races
f1_races = f1_page.findAll("ul", {"class":"resultsarchive-filter ResultFilterScrollable"})

if(len(f1_races) == 3):
    year_races = f1_races[2].findAll("li", {"class":"resultsarchive-filter-item"})
else:
    exit(1)

#organize paths for data printing
change_dir('..')
root_dir = os.getcwd()
create_dir(root_dir + '/data')
change_dir('data')
atual_dir = os.getcwd()
create_dir(atual_dir + '/results')
change_dir('results')
atual_dir = os.getcwd()
create_dir(atual_dir + '/' + year)
change_dir(year)
atual_dir = os.getcwd()

#grab drivers and teams standings table
drivers_table = drivers_page.findAll("tr")
drivers_table_name = drivers_page.find("h1", {"class":"ResultsArchiveTitle"}).text.strip()
print_standings(drivers_table_name,drivers_table,1)

if int(year) >= 1958:
    teams_table = teams_page.find("table", {"class":"resultsarchive-table"}).findAll('tr')
    teams_table_name = teams_page.find("h1", {"class":"ResultsArchiveTitle"}).text.strip()
    print_standings(teams_table_name,teams_table,0)

#analize every race results
for i in range(1,len(year_races)):
    p = Process(target=print_grand_prix, args=(i,year_races[i])).start()
