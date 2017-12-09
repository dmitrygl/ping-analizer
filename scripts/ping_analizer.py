#!/usr/bin/env python3
import subprocess
import cgi

sep = '====='
ok = 'phone is available'
bad = 'phone is unavailable'
newLine = '<br><br>'
spanOpenOk = '<span style="color:green">'
spanOpenBad = '<span style="color:red">'
spanOpenBadMac = '<span style="color:orange">'
spanClose = '</span>'
macError = 'Can\'t find mac-address'


print("Content-type: text/html\n")
print('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Available phones</title></head><body align="center">')

f = open('../file', 'r')
for line in f:
	temp = line.split('=')
	namedev = temp[0]
	ipaddr = temp[1]
	mac = temp[2]

	#sending ping requests
	ping = subprocess.call(['ping', '-c', '2', ipaddr], stdout=subprocess.DEVNULL)
	#receiving mac-address from arp-table
	macSearch = subprocess.check_output(['ip', 'neigh'])
	#converting string data from bytes
	trMacSearch = macSearch.decode()
	#searching our mac-address and ip-address in arp-table
	macArg1 = trMacSearch.find(mac)
	macArg2 = trMacSearch.find(ipaddr)
	
	# if ping wos sucsesful
	if ping == 0:
		# if variable exist
		if macArg1 != -1:
			#if space in arp-table, between mac and ip-addresses, less than 50 symbol, then mac and ip address are in one line, and it's mean that this ip really has this mac-address
			if macArg1 - macArg2 < 50:
				print(spanOpenOk, namedev, sep, ipaddr, sep, mac, sep, sep, sep, ok, spanClose, newLine)
			else:
				print(spanOpenOk, namedev, sep, ipaddr, sep, spanOpenBadMac, mac, spanClose, sep, sep, sep, ok, spanClose, newLine)
		else:
			print(spanOpenBad, namedev, sep, ipaddr, sep, mac, sep, sep, sep, ok, macError, spanClose, newLine)
	else:
		print(spanOpenBad, namedev, sep, ipaddr, sep, mac, sep, sep, sep, bad, spanClose, newLine)

f.close()
print('</body></html>')

