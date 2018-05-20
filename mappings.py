import pymysql.cursors
import pymysql

connection = pymysql.connect(host='localhost',
	user='root',
	password='password',
	db='crime',
	cursorclass=pymysql.cursors.DictCursor)

# TODO add this data to city_mappings table in mysql 

urls = {'Fort_Worth' : 'data.fortworthtexas.gov', 'Chicago' : 'data.cityofchicago.org', 'New_York_City' : 'data.cityofnewyork.us', 'Los_Angeles' : 'data.lacity.org'}
datasets = {'Fort_Worth' : 'fauf-2yhn', 'Chicago' : '6zsd-86xi', "Los_Angeles" : "7fvc-faax", "New_York_City" : "9s4h-37hy"}
crimeCols = {'Fort_Worth' : 'nature_of_call', 'Chicago' : 'primary_type', "Los_Angeles" : "crm_cd_desc", "New_York_City" : "ofns_desc"}
locationCols = {'Fort_Worth' : 'locationtypedescription', 'Chicago' : 'location_description', "Los_Angeles" : "premis_desc", "New_York_City" : "prem_typ_desc"}
longLatCols = {'Fort_Worth' : 'location_1', 'Chicago' : 'location', "Los_Angeles" : "location_1", "New_York_City" : "lat_lon"}
dateCols = {'Fort_Worth' : 'from_date', 'Chicago' : 'date', "Los_Angeles" : "date_occ", "New_York_City" : "cmplnt_fr_dt"}
timeCols = {'Fort_Worth' : '', 'Chicago' : '', "Los_Angeles" : "time_occ", "New_York_City" : "cmplnt_fr_tm"}


master = {'' : '', 
'PROPERTY DAMAGE' : ['DAMAGE','VANDAL'],
'HOMICIDE': ['MURDER', 'HOMICIDE', 'HOM', 'MANSL', 'MANSLAUGHTER'], 
'PUBLIC DISTURBANCE': ['PUBLIC'], 
'KIDNAPPING': ['KIDNAPPING', 'KIDNAP'], 
'WEAPONS INFARCTION': ['WEAPON', 'WEAP', 'FIREARM'], 
'ARSON': ['ARSON'], 
'DRUGS': ['NARCOTIC', 'DRUG', 'NARC'], 
'PROSTITUTION': ['PROSTITUTION', 'PROSTITUT'], 
'BURGLARY': ['BURGLARY', 'BURG'], 
'ASSAULT': ['ASSAULT', 'BATTERY'], 
'FRAUD': ['FRAUD'], 
'TRESPASSING': ['TRES','TRESPASSING'], 
'HARASSMENT': ['HARAS','HARASSMENT', 'HARRASSMENT'], 
'ROBBERY': ['ROBBERY', 'ROB'], 
'SEXUAL RELATED': ['SEX', 'ASSAULT', 'SEXUAL', 'RAPE'], 
'GAMBLING': ['GAMBLING'], 
'THEFT': ['THEFT', 'LARCENY', 'STOLEN']}


# la:
# >>> results[0]['date_occ']
# u'2010-06-17T00:00:00.000'
# >>> results[0]['time_occ']
# u'2310'

# nyc:
# >>> results[0]['cmplnt_fr_dt']
# u'2015-04-06T00:00:00.000'
# >>> results[0]['cmplnt_fr_tm']
# u'12:00:00'

# Chi:
# >>> results[0]['date']
# u'2001-09-15T02:00:00.000'

# Fw:
# >>> results[0]['from_date']
# u'2017-06-01T00:00:00.000'

# def parseDateTime(r,city):
# 	if city == 'Los_Angeles':
# 		return parse(r['date_occ'][0:11] + r['time_occ']).strftime("%Y-%m-%d %H:%M:%S")
# 	elif city == 'New_York_City':
# 		return parse(r['cmplnt_fr_dt'][0:11] + r['cmplnt_fr_tm']).strftime("%Y-%m-%d %H:%M:%S")
# 	elif city == 'Chicago':
# 		return parse(r['date']).strftime("%Y-%m-%d %H:%M:%S")
# 	elif city == 'Fort_Worth':
# 		return parse(r['from_date']).strftime("%Y-%m-%d %H:%M:%S")


# a = datetime.strptime(u'2017-06-01T02:00:00.000'[0:10],'%Y-%m-%d').date()
# b = datetime.strptime(u'2017-06-01T02:00:00.000'[11:19],'%H:%M:%S').time()
# datetime.combine(a, b)



