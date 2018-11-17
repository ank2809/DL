from preprocess import str_to_tup
import csv
import re
import json

player_list = set()

years = list(range(2017, 2018))

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


for year in years:
	file = 'data/{}/{}_article_box.csv'.format(year, year)
	with open(file) as inFile:
		csv_reader = csv.reader(inFile, delimiter=',')
		next(csv_reader)
		for line in csv_reader:
			box_score = line[4]
			game_data = str_to_tup(box_score)
			for record in game_data:
				if len(record) < 15:
					continue
				name = record[0]
				#if name not in team_map:
				player_list.add(name)


d = dict([(y,x+1) for x,y in enumerate(player_list)])

with open('players_2017.json', 'w') as fp:
    json.dump(d, fp)
