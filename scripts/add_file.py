#!/usr/bin/env python3
import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

fd = form['filename']
link = '<a href="../index.html">back</a>'

if fd.filename:
	fn = os.path.basename(fd.filename)
	open('../' + fn, 'wb').write(fd.file.read())
	
	message = 'The file "' + fn + '" was uploaded successfully'
else:
	message = 'no file was uloaded'

print("Content-Type: text/html\n")
print("""<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="../style.css"><title>File load</title></head><body>""")
print("<h1 align=center>{}</h1>" .format(message))
print("{}" .format(link))
print("</body></html>")

