import pandas as pd
import time
from sodapy import Socrata
from dateutil.parser import parse
import pyproj
from mappings import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import gmplot
import webbrowser
import os

# from Levenshtein import *
# from textblob.classifiers import NaiveBayesClassifier
# from textblob import TextBlob

# Dependencies
	# pip install PyMySQL
	# pip install pandas
	# pip install sodapy
	# pip install "requests[security]"
	# pip install gmplot

# How to install basemap:
	# cd /usr/local
	# git clone https://github.com/matplotlib/basemap.git
	# cd basemap/geos-3.3.3
	# ./configure
	# sudo make
	# sudo make install
	# cd ..
	# python setup.py sdist
	# python setup.py install


def createRow(r, city):
	crime_description = r[crimeCols[city]]
	# cols = columnNames[city]
	maximum = 0
	crime_code = None
	for j in master:
		m = len(filter(lambda x: x in crime_description, master[j]))
		if m > maximum:
			maximum = m
			crime_code = j
	datetime_occured = parse(r[dateCols[city]][0:11] + \
							(r[timeCols[city]] if timeCols[city] !='' else '')).strftime("%Y-%m-%d %H:%M:%S")	
	try:
		locDesc = r[locationCols[city]]
	except: 
		locDesc = None
	return (1, crime_description, crime_code, datetime_occured, locDesc, \
			r[longLatCols[city]]['coordinates'][1], r[longLatCols[city]]['coordinates'][0])


# Unauthenticated client only works with public data sets

def insert(connection, city):
	client = Socrata(urls[city], 
					"FXdTHdcGpX9fqDNp9wnN9DGTq", 
					username = "vn602@nyu.edu", 
					password = "PurpleDeer152")
	lim = 50000
	inc = 0
	results = ['']
	while len(results) > 0:
		results = client.get(datasets[city], content_type="json", limit = lim, offset = lim*inc)
		rows = []
		for i in xrange(len(results)):
			try:
				rows.append(createRow(results[i],city))
			except: 
				pass
		cursor = connection.cursor()
		query = "INSERT INTO %s " % city
		query = query + "(`city_id`,`crime_description`, `crime_code`, `datetime_occured`, `location_description`, \
						  `latitude`, `longitude`) \
							VALUES (%s, %s, %s, %s, %s, %s, %s)"
		cursor.executemany(query, rows)
		connection.commit()
		inc += 1
	client.close()


# def plotCrimes(city, crime_code, start, end):
# 	cursor = connection.cursor()
# 	query = "SELECT g.latitude, g.longitude FROM geodata g \
# 			INNER JOIN cities c ON g.city_id = c.ID \
# 			WHERE c.name = '%s' \
# 			AND g.crime_code  = '%s' \
# 			AND datetime_occured > %s AND datetime_occured < %s" % (city, crime_code, start, end)
# 	cursor.execute(query)
# 	data = cursor.fetchall()
# 	lats = [float(i['latitude']) for i in data]
# 	lons = [float(i['longitude']) for i in data]
# 	gmap = gmplot.GoogleMapPlotter.from_geocode(city)
# 	gmap.heatmap(lats, lons)
# 	# gmap.scatter(lats, lons, '#3B0B39', size=40, marker=False)
# 	file = "%s_%s_%s_to_%s.html" % (city,crime_code,start,end)
# 	gmap.draw(file)
# 	webbrowser.open('file://' + os.path.realpath(file))


def plotCrimes(city, crime_code, start, end):
	cursor = connection.cursor()
	query = "SELECT latitude, longitude FROM %s WHERE crime_code = '%s' \
			AND datetime_occured > %s AND datetime_occured < %s" % (city,crime_code, start, end)
	cursor.execute(query)
	data = cursor.fetchall()
	lats = [float(i['latitude']) for i in data]
	lons = [float(i['longitude']) for i in data]
	gmap = gmplot.GoogleMapPlotter.from_geocode(city)
	gmap.heatmap(lats, lons)
	# gmap.scatter(lats, lons, '#3B0B39', size=40, marker=False)
	file = "%s_%s_%s_to_%s.html" % (city,crime_code,start,end)
	gmap.draw(file)
	webbrowser.open('file://' + os.path.realpath(file))


if __name__ == "__main__":
	for city in datasets.keys():
		insert(connection, city)
	connection.close()


#-----------------TESTING CODE----------------------

# # Initial scraping of all crime descriptions to create standardied crime_code. Repeated for each city

# def mapCrimes(crimes):
# 	new = {y : '' for y in crimes}
# 	for i in crimes:
# 		maximum = 0
# 		final = ''
# 		for j in master:
# 			m = len(filter(lambda x: x in i, master[j]))
# 			if m > maximum:
# 				maximum = m
# 				final = j
# 		new[i] = final
# 	return {i:new[i] for i in new if new[i] != ''}



# client = Socrata("data.cityofnewyork.us", 
# 					"FXdTHdcGpX9fqDNp9wnN9DGTq", 
# 					username = "vn602@nyu.edu", 
# 					password = "PurpleDeer152")

# i = 0
# lim = 50000
# crimes = set()
# results = ['']
# while len(results) > 0:
# 	results = client.get("9s4h-37hy", content_type="json", limit = lim, offset = lim*i)
# 	for j in xrange(len(results)):
# 		try:
# 			crimes |= set([results[j]['ofns_desc']])
# 		except KeyError:
# 			pass
# 	i+=1


# ny = mappings(crimes)
# for i in ny.keys():
# 	if new[i]=='':
# 		print i, "   " , new[i]


# # Naive-Bayes classifier for classifying crime descriptions into crime_codes...Didn't have very good accuracy

# from textblob.classifiers import NaiveBayesClassifier
# from textblob import TextBlob

# cities = [ny.keys(),la.keys(),chi.keys()]
# train = []
# for city in cities:
# 	crimes = mapCrimes(city)
# 	train += [(i,crimes[i]) for i in crimes]

# train = list(set(train))
# cl = NaiveBayesClassifier(train)


# # testing classifier on fort_worth crime descriptions

# fw = map(string.upper,fw)

# for i in fw:
# 	print('%-50s %6s' % (i,cl.classify(i)))

# # basemap plotting...not as good as gmplot

# m = Basemap()
# x, y = m(lons,lats)
# m.scatter(x,y,3,marker='o',color='k')
# plt.show()
# results_df = pd.DataFrame.from_records(result_list)



