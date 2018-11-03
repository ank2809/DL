from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import os
import time
import csv
import pytz


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

team_abbreviations = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GS',
						'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NO', 'NY',
						'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SA', 'TOR', 'UTAH', 'WSH']


def convert_utc_est(utc_time):
	"""
	Converts the UTC time given by ESPN India into EST time.
	:return: EST date in format YYYYMMDD
	"""
	utc_year = int(utc_time[:4])
	utc_month = int(utc_time[5:7])
	utc_day = int(utc_time[8:10])
	utc_hour = int(utc_time[11:13])
	utc_minute = int(utc_time[14:16])

	utc_date = pytz.utc.localize(datetime(utc_year, utc_month, utc_day, utc_hour, utc_minute))
	est_date = utc_date.astimezone(pytz.timezone('America/New_York'))
	year = est_date.year
	month = '{:02d}'.format(est_date.month)
	day = '{:02d}'.format(est_date.day)
	date = str(year) + str(month) + str(day)

	return date


date = gameids[0][1]
year = date[:4]

directory = 'data/' + year + '/'
if not os.path.exists(directory):
	os.makedirs(directory)

filename = directory + year + '_articles.csv'

with open(filename, 'a') as outFile:
	article_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	article_writer.writerow(['gameid', 'away_team', 'home_team', 'date', 'article'])

	game_counter = 0
	for game in gameids:
		gameid = game[0]

		url_date = 'http://www.espn.in/nba/game?gameId=' + gameid
		url_page = urlopen(url_date)
		soup = BeautifulSoup(url_page, 'html.parser')
		get_date = soup.find('div', attrs={'class': 'game-date-time'})
		utc_time = get_date.span['data-date']
		date = convert_utc_est(utc_time)

		url_recap = 'http://www.espn.in/nba/recap?gameId=' + gameid
		url_page = urlopen(url_recap)
		soup = BeautifulSoup(url_page, 'html.parser')

		teams = soup.find_all('td', attrs={'class': 'team-name'})
		away_team = teams[0].text
		home_team = teams[1].text

		# Check to confirm not all-star game 
		if away_team not in team_abbreviations or home_team not in team_abbreviations:
			print("Skipped game")
			continue
		else:
			article = soup.find('div', attrs={'class': 'article-body'})
			paragraphs = article.find_all('p')
			article_str = ''
			for t in paragraphs:
				article_str += t.text + ' '

		article_writer.writerow([gameid, away_team, home_team, date, article_str])

		game_counter += 1
		print("Downloaded {} vs {}, {} article. Completed {} / {}".format(away_team, home_team, date, game_counter, len(gameids)))
		time.sleep(1)

print("Downloaded {} game articles.".format(game_counter))