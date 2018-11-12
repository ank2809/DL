from pandas import read_csv
from csv import writer
from csv import QUOTE_MINIMAL

team_names = {
    'ATL': 'ATL',
    'BKN': 'BRK',
    'BOS': 'BOS',
    'CHA': 'CHA',
    'CHI': 'CHI',
    'CLE': 'CLE',
    'DAL': 'DAL',
    'DEN': 'DEN',
    'DET': 'DET',
    'GSW': 'GSW',
	'HOU': 'HOU',
    'IND': 'IND',
    'LAC': 'LAC',
    'LAL': 'LAL',
    'MEM': 'MEM',
    'MIA': 'MIA',
    'MIL': 'MIL',
    'MIN': 'MIN',
    'NOH': 'NOH',
    'NOP': 'NOP',
    'NOK': 'NOK',
    'NYK': 'NYK',
	'OKC': 'OKC',
    'ORL':'ORL',
    'PHI': 'PHI',
    'PHX': 'PHO',
    'POR': 'POR',
    'SAC': 'SAC',
    'SAS': 'SAS',
    'TOR': 'TOR',
    'UTA': 'UTA',
    'WAS': 'WAS',
	'NJN': 'NJN',
    'SEA': 'SEA'
}
def read(year, out):

    play_by_play = read_csv('data/' + year + '/' + year + '_playbyplay.csv', index_col=False)
    imp = dict()
    for i in range(len(play_by_play)):

        playlist = play_by_play['play_by_play'][i].replace('\"\"','').replace('\"','')
        play_max = None
        prob_max = 0
        ind = 1
        plays = []
        if len(playlist) > 2:
            while ind < len(playlist):

                comma = playlist.index(',', ind)
                # except IndexError:
                #     print(playlist)
                #     print(ind)
                #     print(playlist[ind-5:ind+5])
                while playlist[comma+2] != '\'':
                    comma = playlist.index(',', comma+1)

                percent = playlist.index('%', comma)
                play = playlist[ind+1:comma].replace('"','')
                prob = float(playlist[comma+3:percent])
                ind = percent + 5
                if prob > 20:
                    plays.append((play, prob))

        home_team = team_names[play_by_play['home_team'][i]]
        date = play_by_play['date'][i]
        out.writerow([home_team, date, plays])

    # for i in range(len(reader)):
    #
    #     home_team = reader['home_team'][i]
    #     date = reader['date'][i]
    #
    #     if (home_team, date) in imp:
    #
    #         away_team = reader['away_team'][i]
    #         article = reader['article'][i]
    #         box_score = reader['box_score'][i]
    #         plays = imp[(home_team, date)]
    #         print(plays)
    #         out.writerow([home_team, away_team, date, box_score, plays, article])


for i in range (2006, 2005, -1):
    year = str(i)
    file = open('data/' +  year + '/' + year + '_selected_plays.csv', 'w', newline='')
    out = writer(file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
    out.writerow(['home_team','date', 'plays'])
    read(year, out)

