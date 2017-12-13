#!/usr/bin/env python3
import mysql.connector
import datetime
import subprocess

# connectiong to database;
cnx = mysql.connector.connect(user='puser', password='pass1!1SSAP', host='localhost', database='pinganalizdb')
cursor = cnx.cursor(buffered = True)

# checkign tables in DB. If DB empty, then will make tables, if tables exist - will add data. 
check = ("SHOW TABLES")
cursor.execute(check)
check = cursor.fetchall()
if not check:
	TABLES = {}
	TABLES['pnga_hostname'] = (
        	"CREATE TABLE `pnga_hostname` ("
	        "`id` int NOT NULL AUTO_INCREMENT,"
        	"`hostname` varchar(18) NOT NULL,"
        	"UNIQUE (`hostname`),"
        	"PRIMARY KEY (`id`)"
        	") ENGINE=InnoDB")

	TABLES['pnga_status'] = (
        	"CREATE TABLE `pnga_status` ("
	        "`id` int NOT NULL AUTO_INCREMENT,"
	        "`status` varchar(10) NOT NULL,"
	        "UNIQUE (`status`),"
       		"PRIMARY KEY (`id`)"
	        ") ENGINE=InnoDB")

	TABLES['pnga_data'] = (
        	"CREATE TABLE `pnga_data` ("
	        "`id` int NOT NULL AUTO_INCREMENT,"
	        "`day` int NOT NULL,"
	        "`month` int NOT NULL,"
	        "`time` timestamp default current_timestamp,"
	        "`hostname` int NOT NULL,"
	        "`status` int NOT NULL,"
	        "PRIMARY KEY (`id`)"
	        ") ENGINE=InnoDB")

	for name, ddl in TABLES.items():
		cursor.execute(ddl)
	
	temp = ['good', 'bad', 'attention']
	# add data in static table
	for t in temp:
		addLine = ("INSERT INTO pnga_status (status) VALUES ('{}')".format(t))
		cursor.execute(addLine)
	cnx.commit()

else:
	# similar like ping_analizer.py, but data add in table DB.
	date = datetime.datetime.now()
	day = date.day
	month = date.month	
	f = open('../file', 'r')
	for line in f:
		temp = line.split('=')
		namedev = temp[0]
		ipaddr = temp[1]
		mac = temp[2]
			
		searchHost = ("SELECT * FROM pnga_hostname WHERE hostname = '{}'".format(namedev))
		cursor.execute(searchHost)
		searchHost = cursor.fetchall()
		if not searchHost:
			add = ("INSERT INTO pnga_hostname (hostname) VALUES ('{}')".format(namedev))
			cursor.execute(add)
			cnx.commit()

		ping = subprocess.call(['ping', '-c', '2', ipaddr], stdout=subprocess.DEVNULL)
		macSearch = subprocess.check_output(['ip', 'neigh'])
		trMacSearch = macSearch.decode()
		macArg1 = trMacSearch.find(mac)
		macArg2 = trMacSearch.find(ipaddr)

		if ping == 0:
			if macArg1 != -1:
				if macArg1 - macArg2 < 50:
					searchHost = ("SELECT * FROM pnga_hostname WHERE hostname = '{}'".format(namedev))
					cursor.execute(searchHost)
					searchHost = cursor.fetchall()
					searchHost = searchHost[0]
					add = ("INSERT INTO pnga_data (day, month, hostname, status) VALUES ('{}', '{}', '{}', '1')".format(day, month, searchHost[0]))
					cursor.execute(add)
					cnx.commit()
				else:
					searchHost = ("SELECT * FROM pnga_hostname WHERE hostname = '{}'".format(namedev))
					cursor.execute(searchHost)
					searchHost = cursor.fetchall()
					searchHost = searchHost[0]
					add = ("INSERT INTO pnga_data (day, month, hostname, status) VALUES ('{}', '{}', '{}', '3')".format(day, month, searchHost[0]))
					cursor.execute(add)
					cnx.commit()
			else:
				searchHost = ("SELECT * FROM pnga_hostname WHERE hostname = '{}'".format(namedev))
				cursor.execute(searchHost)
				searchHost = cursor.fetchall()
				searchHost = searchHost[0]
				add = ("INSERT INTO pnga_data (day, month, hostname, status) VALUES ('{}', '{}', '{}', '2')".format(day, month, searchHost[0]))
				cursor.execute(add)
				cnx.commit()
		else:
			searchHost = ("SELECT * FROM pnga_hostname WHERE hostname = '{}'".format(namedev))
			cursor.execute(searchHost)
			searchHost = cursor.fetchall()
			searchHost = searchHost[0]
			add = ("INSERT INTO pnga_data (day, month, hostname, status) VALUES ('{}', '{}', '{}', '2')".format(day, month, searchHost[0]))
			cursor.execute(add)
			cnx.commit()

	f.close()

cursor.close()
cnx.close()

