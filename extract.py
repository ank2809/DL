from csv import writer
from csv import QUOTE_MINIMAL

def clean(year):

    source = open('data/' + year + '/' + year + '_play_by_play.csv')
    dest = open('data/' + year + '/' + year + '_playbyplay.csv', 'w', newline='')
    cleaner = writer(dest, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
    cleaner.writerow(['home_team', 'away_team', 'date', 'excitement_score', 'comeback_score', 'mvp', 'lvp', 'play_by_play'])

    for line in source:

        current = 0
        row = []
        b = True
        for i in range(7):

            try:
                next = line.index(',', current)
                row.append(line[current:next])
                current = next + 1
            except ValueError:
                b = False
                break

        if b:
            row.append(line[current:len(line)-1])
            cleaner.writerow(row)

    source.close()
    dest.close()

for year in range(2006, 2018):

    clean(str(year))