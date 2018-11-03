from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from time import sleep
from urllib.error import HTTPError


list_of_stats = ['mp', 'fg', 'fg_pct', 'fg3', 'fg3_pct', 'ft', 'ft_pct', 'pts', 'orb', 'trb', 'ast', 'stl', 'blk', 'tov']

team_names = {
    'ATL': 'ATL',
    'BOS': 'BOS',
    'BKN': 'BRK',
    'CHA': 'CHO',
    'CHI': 'CHI',
    'CLE': 'CLE',
    'DAL': 'DAL',
    'DEN': 'DEN',
    'DET': 'DET',
    'HOU': 'HOU',
    'IND': 'IND',
    'GS': 'GSW',
    'LAC': 'LAC',
    'LAL': 'LAL',
    'MEM': 'MEM',
    'MIA': 'MIA',
    'MIL': 'MIL',
    'MIN': 'MIN',
    'NO': 'NOP',
    'NY': 'NYK',
    'OKC': 'OKC',
    'ORL': 'ORL',
    'PHI': 'PHI',
    'PHX': 'PHO',
    'POR': 'POR',
    'SAC': 'SAC',
    'SA': 'SAS',
    'TOR': 'TOR',
    'UTAH': 'UTA',
    'WSH': 'WAS',
}

def extract_name(row):

    try:
        start = row.index('csk') + 5
        end = row.index('\"', start)
        return row[start:end]

    except ValueError:

        return None


def extract(row, tag):

    try:
        start = row.index('\"' + tag) + len(tag) + 3
        end = row.index('<', start)
        return row[start:end]
    except ValueError:

        return None


def process_box(soup, team):

    table_name = 'box_' + team.lower() + '_basic'
    box = soup.find('table', attrs={'id': table_name})

    rows  = box.find_all('tr')
    ret = []

    for t in rows:

        row  = str(t)

        if 'th class=\"left \"' in row:

            if 'csk' in row:

                val = [extract_name(row)]
            else:

                val = [team]

            for stat in list_of_stats:
                val.append(extract(row, stat))

            ret.append(tuple(val))
    return ret


def scrape(home, away, d, file):

    str_d = d.strftime("%Y%m%d")
    try:
        url = 'https://www.basketball-reference.com/boxscores/' + str_d + '0' + home + '.html'
        url_page = urlopen(url)
    except HTTPError:
        sleep(60)
        url_page = urlopen(url)
    print(url)
    file.write(str_d + ',' + away + ',' + home)
    soup = BeautifulSoup(url_page, 'html.parser')
    file.write(','+str(process_box(soup, home)))
    file.write(','+str(process_box(soup, away)))


def process_year(year):

    game_list = open('data/'+year+'/'+year+'_articles.csv', 'r')
    file = open('data/'+year+'/'+year+'_box_scores.csv', 'a')

    for game in game_list:

        tokens = game.split(',')
        try:
            away = team_names[tokens[1]]
            home = team_names[tokens[2]]
            d = datetime.strptime(tokens[3], "%Y%m%d")
            file.write(tokens[0]+',')
            scrape(home, away, d, file)
            sleep(5)
            file.write('\n')
        except KeyError:
            continue
    game_list.close()
    file.close()

process_year('2017')
# file = open('test.txt','w')
# d = datetime.strptime('20171123', '%Y%m%d')
# scrape('BRK','POR',d, file)