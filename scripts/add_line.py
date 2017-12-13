#!/usr/bin/env python3
import cgi, cgitb

# started work with html forms
form = cgi.FieldStorage()

# recive data from form
name = form.getvalue('name')
ipaddr = form.getvalue('ipaddr')
mac = form.getvalue('mac')
sep = '='
link = '<a href="../index.html">back</a>'

if name is None or ipaddr is None or mac is None:
	message = '<h1 align="center" style="color:red">You must add data in all field</h1>'
else:
	# make link to back on mainpage
	lineW = name+sep+ipaddr+sep+mac+sep
	# open file for add one line
	f = open('../file', 'a')
	print(lineW, file=f)
	
	f.close()
	message = '<h1>"' + name + ',' + ipaddr + ','+mac+ '" was written to file</h1>'

# print in browser
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML><html><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="../style.css"><title>Add line</title></head><body>""")

print('{}' .format(message))
print("<br>{}" .format(link))

print("</body></html>")

