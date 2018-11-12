from pandas import read_csv
for year in range(2006, 2018):
    path = 'data/{}/{}_article_box.csv'.format(year, year)

    art_box = read_csv(path)

    path = 'data/{}/{}_selected_plays.csv'.format(year, year)
    plays = read_csv(path)

    art_box = art_box.applymap(str)
    plays = plays.applymap(str)

    ab = set()

    for i in range(len(art_box)):

        home_team = art_box['home_team'][i]
        ab.add(home_team)

    unique = set()
    for j in range(len(plays)):

        home_team = plays['home_team'][j]
        if home_team not in ab:
            unique.add(home_team)

    print(unique)