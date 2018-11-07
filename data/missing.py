art =open('2009/2009_articles.csv')
bs = open('2009/2009_box_scores.csv')
count = 0
while True:

    a = art.readline()

    if a is None or len(a) == 0:
        break

    try:
        x = int(a.split(',')[0])
    except ValueError:
        continue
    if x < 1000000:
        continue

    b = bs.readline()
    x = a[:a.index(',')]
    y = b[:b.index(',')]
    if x != y:
        print(x)
        print(y)
        break
    # b = bs.readline()
    #
    # if b is None:
    #     break
    #
    # x = a.split(',')
    # y = a.split(',')
    # if x[0] != y[0]:
    #
    #     print(x[0])
    #     print(x[1])
    #     print(x[2])
    #     break

