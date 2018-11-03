from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from urllib.error import URLError, HTTPError
import os
import time
import csv
import pytz


team_abbreviations = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GS',
						'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NO', 'NY',
						'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SA', 'TOR', 'UTAH', 'WSH',
						'NJ', 'SEA']


def get_dates(year, season_start_dict):
	"""
	Gets a list of dates between season start date and season end date.
	:return: list of dates in format YYYYMMDD
	"""
	season_dates = []

	start_date = season_start_dict[year][0]
	end_date = season_start_dict[year][1]

	delta = end_date - start_date

	for i in range(delta.days + 1):
	    date = start_date + timedelta(i)
	    year = date.year
	    month = '{:02d}'.format(date.month)
	    day = '{:02d}'.format(date.day)

	    date_str = str(year) + str(month) + str(day)
	    season_dates.append(date_str)

	return season_dates


def get_gameids(season_dates):
	"""
	Given a list of dates, will get all the gameids.
	:return list of 9 digit gameids:
	"""
	gameid_str = '{"isExternal":false,"shortText":"Box Score","rel":["boxscore","desktop","event"],"language":"en-IN","href":"http://www.espn.com/nba/boxscore?gameId='
	gameids = []
	for date in season_dates:
		url = 'http://www.espn.in/nba/scoreboard/_/date/' + date
		while True:
			try:
				url_page = urlopen(url)
			except HTTPError:
				continue
			break

		print("Processed games on " + date)

		soup = str(BeautifulSoup(url_page, 'html.parser'))
		
		cur_index = 0
		gameid_index = soup.find(gameid_str, cur_index)
		while gameid_index != -1:
			gameid_index += len(gameid_str)
			gameids.append(soup[gameid_index:gameid_index+9])
			cur_index = gameid_index
			gameid_index = soup.find(gameid_str, cur_index)
		#time.sleep(4.2) # 'The 4.2 is for 420' - Ansh Kothary

	return gameids


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


def article_filename(year):
	"""
	Returns the path of the csv data to be held given the year.
	Creates directory if it does not exist already.
	"""
	directory = 'data/' + str(year) + '/'
	if not os.path.exists(directory):
		os.makedirs(directory)

	filename = directory + str(year) + '_articles.csv'

	return filename


def write_articles(filename, gameids):
	with open(filename, 'a') as outFile:
		article_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		article_writer.writerow(['gameid', 'away_team', 'home_team', 'date', 'article'])

		game_counter = 0
		for gameid in gameids:
			url_date = 'http://www.espn.in/nba/game?gameId=' + gameid
			while True:
				try:
					url_page = urlopen(url_date)
				except HTTPError:
					continue
				break
			
			soup = BeautifulSoup(url_page, 'html.parser')
			get_date = soup.find('div', attrs={'class': 'game-date-time'})
			utc_time = get_date.span['data-date']
			date = convert_utc_est(utc_time)

			url_recap = 'http://www.espn.in/nba/recap?gameId=' + gameid
			while True:
				try:
					url_page = urlopen(url_recap)
				except HTTPError:
					continue
				break
			
			soup = BeautifulSoup(url_page, 'html.parser')

			teams = soup.find_all('td', attrs={'class': 'team-name'})
			try:
				away_team = teams[0].text
				home_team = teams[1].text
			except IndexError:
				print("Game not played.")
				continue

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

if __name__ == '__main__':
	start_end_dates = {2017: (date(2017, 10, 18), date(2018, 4, 12)),
					2016: (date(2016, 10, 26), date(2017, 4, 13)),
					2015: (date(2015, 10, 28), date(2016, 4, 14)),
					2014: (date(2014, 10, 29), date(2015, 4, 16)),
					2013: (date(2013, 10, 30), date(2014, 4, 17)),
					2012: (date(2012, 10, 31), date(2013, 4, 18)),
					2011: (date(2011, 12, 25), date(2012, 4, 27)),
					2010: (date(2010, 10, 27), date(2011, 4, 14)),
					2009: (date(2009, 10, 28), date(2010, 4, 15)),
					2008: (date(2008, 10, 29), date(2009, 4, 16)),
					2007: (date(2007, 10, 31), date(2008, 4, 17)),
					2006: (date(2006, 11, 1), date(2007, 4, 18))}

	for year in start_end_dates:
		season_dates = get_dates(year, start_end_dates)

		gameids = get_gameids(season_dates)

		filename = article_filename(year)
		write_articles(filename, gameids)

