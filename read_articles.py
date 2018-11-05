import csv

years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

for year in years:
	directory = 'data/' + str(year) + '/'
	filename = directory + str(year) + '_articles.csv'

	with open(filename) as inFile:
		csv_reader = csv.reader(inFile, delimiter=',')
		line_count = -1
		for row in csv_reader:
			line_count += 1
		print(year, line_count)