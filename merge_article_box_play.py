from pandas import read_csv


for year in range(2006, 2014):
    path = 'data/{}/{}_article_box.csv'.format(year, year)

    art_box = read_csv(path)

    path = 'data/{}/{}_selected_plays.csv'.format(year, year)
    plays = read_csv(path)

    art_box = art_box.applymap(str)
    plays = plays.applymap(str)

    df = art_box.merge(plays, on=['home_team', 'date'])

    new_path = 'data/{}/{}_article_box_play.csv'.format(year, year)

    df.to_csv(new_path, sep=',', index=False)