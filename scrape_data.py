from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
import re
import time

start_date = date(2017, 10, 18)
end_date = date(2018, 4, 12)

season_dates = []

delta = end_date - start_date

for i in range(delta.days + 1):
    date = start_date + timedelta(i)
    year = date.year
    month = '{:02d}'.format(date.month)
    day = '{:02d}'.format(date.day)

    date_str = str(year) + str(month) + str(day)
    season_dates.append(date_str)


gameid_str = '{"isExternal":false,"shortText":"Box Score","rel":["boxscore","desktop","event"],"language":"en-IN","href":"http://www.espn.com/nba/boxscore?gameId='
gameids = []
for date in season_dates:

	url = 'http://www.espn.in/nba/scoreboard/_/date/' + date

	url_page = urlopen(url)
	print("Success")
	print(date)

	soup = str(BeautifulSoup(url_page, 'html.parser'))
	
	cur_index = 0
	gameid_index = soup.find(gameid_str, cur_index)
	while gameid_index != -1:
		gameid_index += len(gameid_str)
		gameids.append((soup[gameid_index:gameid_index+9], date))
		cur_index = gameid_index
		gameid_index = soup.find(gameid_str, cur_index)

	time.sleep(4.2) # 'The 4.2 is for 420' - Ansh Kothary




team_abbreviations = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GS'
						'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NO', 'NY',
						'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SA', 'TOR', 'UTAH', 'WSH']


for game in gameids:
	gameid = game[0]
	date = game[1]
	year = date[:4]
	url = 'http://www.espn.in/nba/recap?gameId=' + gameid

	url_page = urlopen(url)

	soup = BeautifulSoup(url_page, 'html.parser')

	teams = soup.find_all('td', attrs={'class': 'team-name'})
	away_team = teams[0].text
	home_team = teams[1].text

	article = soup.find('div', attrs={'class': 'article-body'})
	paragraphs = article.find_all('p')

	filename = "data/" + year + '/' + away_team + "_" + home_team + '_' + date + '.csv'
	with open(filename, 'w') as outFile:
		for t in paragraphs:
			outFile.write(t.text)
			outFile.write("\n")

		outFile.write("\n\n\n\n")

	time.sleep(4.2) # 'The 4.2 is for 420' - Ansh Kothary
