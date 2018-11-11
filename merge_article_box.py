"""
Combines articles and box scores into one file
"""
import pandas as pd

years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

for year in years:
	path = 'data/{}/{}_boxscores.csv'.format(year, year)

	box_score = pd.read_csv(path)

	path = 'data/{}/{}_articles.csv'.format(year, year)
	article = pd.read_csv(path)

	box_score = box_score.applymap(str)
	article = article.applymap(str)

	df = box_score.merge(article, on=['gameid'])
	df = df.iloc[:, list(range(5)) + list(range(8,9))]
	df.rename(columns={'date_x': 'date', 'away_team_x': 'away_team', 'home_team_x': 'home_team'}, inplace=True)

	new_path = 'data/{}/{}_article_box.csv'.format(year, year)

	df.to_csv(new_path, sep=',', index=False)