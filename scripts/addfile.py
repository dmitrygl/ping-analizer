#!/usr/bin/env python3
import cgi, cgitb

# started work with html forms
form = cgi.FieldStorage()

# recive data from form
name = form.getvalue('name')
ipaddr = form.getvalue('ipaddr')
mac = form.getvalue('mac')
sep = '='
lineW = name+sep+ipaddr+sep+mac+sep

if name is None or ipaddr is None or mac is None:
        message = 'You must add data in all field'
else:
        # open file for add one line
        f = open('../file', 'a')
        print(lineW, file=f)

        f.close()
        message = 'Data was written'

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML><html><head><meta charset="utf-8"><title>Add line</title></head><body>""")

print("<h1>{}</h1>" .format(message))

print("</body></html>")

