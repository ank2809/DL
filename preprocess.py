"""
Preprocess team names and player names.
Some code modified from https://github.com/harvardnlp/data2text/blob/master/non_rg_metrics.py
"""

import csv
import re

team_map = {'ATL' : 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BRK': 'Brooklyn Nets', 
			'CHO': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers',
			'DET': 'Detroit Pistons', 'IND': 'Indiana Pacers', 'MIA': 'Miami Heat',
			'MIL': 'Milwaukee Bucks', 'NYK': 'New York Knicks', 'ORL': 'Orlando Magic',
			'PHI': 'Philadelphia 76ers', 'TOR': 'Toronto Raptors', 'WAS': 'Washington Wizards',
			'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'GSW': 'Golden State Warriors',
			'HOU': 'Houston Rockets', 'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers',
			'MEM': 'Memphis Grizzlies', 'MIN': 'Minnesota Timberwolves', 'NOP': 'New Orleans Pelicans',
			'OKC': 'Oklahoma City Thunder', 'PHO': 'Phoenix Suns', 'POR': 'Portland Trail Blazers',
			'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs', 'UTA': 'Utah Jazz',
			'NJN': 'New Jersey Nets', 'SEA': 'Seattle SuperSonics', 'CHA': 'Charlotte Bobcats'}

years = list(range(2006, 2018))

def preprocess_teams():
	equiv_teams = {}
	cities = []
	teams = []
	for abbrev in team_map:
		team_name = team_map[abbrev]
		parts = team_name.split()
		if len(parts) == 2:
			equiv_teams[abbrev] = [parts[0], parts[1], team_name]
		elif parts[0] == 'Portland':
			equiv_teams[abbrev] = [parts[0], team_name, 'Trail Blazers', 'Blazers']
		else:
			equiv_teams[abbrev] = [" ".join(parts[:2]), parts[2], team_name]

	return equiv_teams

def preprocess_players(names):
	equiv_names = {}
	for name in names:
		parts = name.split()


def str_to_tup(string):
	game_data = []
	tokens = string.split(')')[:-1]
	for token in tokens:
		values = re.findall(r"'(.*?)'", token)
		game_data.append(values)

	return game_data

def get_tuples(box_data):
	game_data = str_to_tup(box_data)
	tuple_space = []
	for record in game_data:
		if len(record) < 15:
			continue
		name = record[0]
		field_goals = record[2]
		fg_percent = record[3]
		threes = record[4]
		three_percent = record[5]
		free_throws = record[6]
		ft_percent = record[7]
		points = record[8]
		o_rebounds = record[9]
		rebounds = record[10]
		assists = record[11]		
		steals = record[12]
		blocks = record[13]
		turnovers = record[14]

		tuple_space.extend([(name, 'fg', field_goals), (name, 'fg_pct', fg_percent), (name, 'fg3', threes),
			(name, 'fg3_pct', three_percent), (name, 'ft', free_throws), (name, 'ft_pct', ft_percent),
			(name, 'pts', points), (name, 'orb', o_rebounds), (name, 'trb', rebounds),
			(name, 'ast', assists), (name, 'stl', steals), (name, 'blk', blocks), (name, 'tov', turnovers)])

	return tuple_space

for year in years:
	file_read = 'data/{}/{}_article_box.csv'.format(year, year)
	file_write = 'data/{}/{}_tuple_space.csv'.format(year, year)
	with open(file_read) as inFile:
		with open(file_write, 'w') as outFile:
			csv_reader = csv.reader(inFile, delimiter=',')
			next(csv_reader)
			article_writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			article_writer.writerow(['gameid', 'away_team', 'home_team', 'date', 'tuples'])
			for line in csv_reader:
				gameid = line[0]
				date = line[1]
				away_team = line[2]
				home_team = line[3]
				box_score = line[4]

				tuples = get_tuples(box_score)

				article_writer.writerow([gameid, away_team, home_team, date, tuples])