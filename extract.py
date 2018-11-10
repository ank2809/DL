from csv import writer
from csv import QUOTE_MINIMAL

def clean(year):

    source = open('data/' + year + '/' + year + '_box_scores.csv')
    dest = open('data/' + year + '/' + year + '_boxscores.csv', 'w', newline='')
    cleaner = writer(dest, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
    cleaner.writerow(['gameid', 'date', 'away_team', 'home_team', 'box_score'])

    for line in source:

        current = 0
        row = []
        for i in range(4):

            next = line.index(',', current)
            row.append(line[current:next])
            current = next + 1

        row.append(line[current:len(line)-1])
        cleaner.writerow(row)

    source.close()
    dest.close()

for i in range(2006, 2017):
    clean(str(i))