from pandas import read_csv

def read(year):

    reader = read_csv('data/' + year + '/' + year + '_article_box.csv', delimiter=',')
    play_by_play = read_csv('data/' + year + '/' + year + '_playbyplay.csv', delimiter=',')
    imp = dict()
    for i in range(len(play_by_play)):

        playlist = play_by_play['home_team'][i]
        print(playlist)
        play_max = None
        prob_max = 0
        ind = 1
        break
        while ind < len(playlist):

            comma = playlist.index(',', ind)
            percent = playlist.index('%', comma)
            play = playlist[ind+1:comma]
            print(play)
            prob = float(playlist[comma+3:percent])
            print(prob)
            ind = percent + 4
            break
        break
        imp[(play_by_play['home_team'][i], play_by_play['date'][i])]


read('2017')
