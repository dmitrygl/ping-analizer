#!/usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode
import cgi, cgitb

# started work with html forms
form = cgi.FieldStorage()

# recive data from form
request = form.getvalue("request")
day = form.getvalue("day")
month = form.getvalue("month")

link = '<a href="../index.html">back</a>'

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML><html><head><meta charset="utf-8"><title>DB report</title></head><body>""")

if request is None or day is None or month is None:
	print("""<h1 align=center style="color:red">"You must choose day and month, and what kind report you want receive - short or long'</h1>""")
	print("{}" .format(link))

# connection with DB
cnx = mysql.connector.connect(user='puser', password='pass1!1SSAP', host='localhost', database='pinganalizdb')
cursor = cnx.cursor()

# translate str in int
request = int(request)
day = int(day)
month = int(month)

# if query to DB is short statistic
if request == 1:
	# send requests to DB for good (1), bad (2) and attention (3) status.
	goodQuery = ("SELECT COUNT(*) FROM pnga_data WHERE day = {} AND month = {} and status = 1".format(day, month))
	cursor.execute(goodQuery)
	goodQuery = cursor.fetchall() 
	goodQuery = goodQuery[0]
	badQuery = ("SELECT COUNT(*) FROM pnga_data WHERE day = {} AND month = {} AND status = 2".format(day, month))
	cursor.execute(badQuery)
	badQuery = cursor.fetchall() 
	badQuery = badQuery[0]
	attentionQuery = ("SELECT COUNT(*) FROM pnga_data WHERE day = {} AND month = {} AND status = 3".format(day, month))
	cursor.execute(attentionQuery)
	attentionQuery = cursor.fetchall() 
	attentionQuery = attentionQuery[0]
	
	cursor.close()
	cnx.close()

	#print data in browser
	print("<h1 align=center>During day of {} of month {}:</h1>".format(day, month))
	print("""<h1 align=center style="color:green">{} hosts wos available</h1>""".format(goodQuery[0]))
	print("""<h1 align=center style="color:red">{} hosts wos unavailable</h1>""".format(badQuery[0]))
	print("""<h1 align=center style="color:orange">{} hosts wos need attention</h1>""".format(attentionQuery[0]))

	
# if query to DB is long statistic
else:
	
	query = ("SELECT pnga_data.time, pnga_hostname.hostname, pnga_status.status FROM pnga_data LEFT JOIN pnga_hostname ON pnga_hostname.id = pnga_data.hostname LEFT JOIN pnga_status ON pnga_status.id = pnga_data.status WHERE day = {} AND month = {}".format(day, month))
	cursor.execute(query)
	query = cursor.fetchall() 

	
	print("<h1 align=center>During day of {} of month {}:</h1>".format(day, month))

	for y in query:
		print("<p align=center> {}  </p>".format(y))

print("{}" .format(link))
cursor.close()
cnx.close()

print("</body></html>")

