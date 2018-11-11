from pandas import read_csv
from csv import writer
from csv import QUOTE_MINIMAL

def read(year, out):

    play_by_play = read_csv('data/' + year + '/' + year + '_playbyplay.csv', index_col=False)
    imp = dict()
    for i in range(len(play_by_play)):

        playlist = play_by_play['play_by_play'][i].replace('\"\"','').replace('\"','')
        play_max = None
        prob_max = 0
        ind = 1
        plays = []
        while ind < len(playlist):

            comma = playlist.index(',', ind)
            percent = playlist.index('%', comma)
            play = playlist[ind+1:comma]
            prob = float(playlist[comma+3:percent])
            ind = percent + 5
            if prob > 20:
                plays.append((play, prob))
        imp[(play_by_play['home_team'][i], play_by_play['date'][i])] = plays

    for i in range(len(reader)):

        home_team = reader['home_team'][i]
        date = reader['date'][i]

        if (home_team, date) in imp:

            away_team = reader['away_team'][i]
            article = reader['article'][i]
            box_score = reader['box_score'][i]
            plays = imp[(home_team, date)]
            print(plays)
            out.writerow([home_team, away_team, date, box_score, plays, article])


for year in range (2017, 2012, -1):
    file = open('data/' +  year + '/' + year + '_play.csv', 'w')
    out = writer(file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
    out.writerow(['home_team', 'away_team', 'date', 'box_score', 'play_by_play', 'article'])
    read(str(year), out)

