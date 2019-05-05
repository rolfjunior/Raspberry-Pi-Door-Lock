import requests
import threading
import time
import sys
sys.path.insert(0, "/home/pi/pi-rc522/ChipReader")
from pirc522 import RFID
import signal
import os
import json
from pprint import pprint
import cPickle as pickle
import webbrowser
#import subprocess
from teste import lock
from teste import unlock

CARDS_ALLOWED = {
    '3C:2F:4F:0:2D': 'Teste',
	'81:8:173:121:141': 'Rolf1',
	'97:244:30:57:178': 'Rolf2',
	'53:188:162:67:104': 'Rolf3',
	'197:248:221:82:178': 'Rolf4',
}

#def lock():
	#print ("passou comando de abrir browser")
	#webbrowser.open('https://maker.ifttt.com/trigger/tagclose/with/key/dkA6CLpfLT3CL4wO64893f')
	#time.sleep(10)
	#print ("\nClose web browser.\n")
	#os.system("pkill chromium")

#def unlock():
	#print ("passou comando de abrir browser")
	#webbrowser.open('https://maker.ifttt.com/trigger/tagopen/with/key/dkA6CLpfLT3CL4wO64893f')
	#time.sleep(10)
	#print ("\nClose web browser.\n")
	#os.system("pkill chromium")

with open('card_data.json') as data_file:
	extract = json.load(data_file)

#start tags reading, waiting for tags
try:
	rfid = RFID()

	util = rfid.util()

	util.debug = False

	print ("Waiting for tag\n")

	while True:
		#Request tag
		(error, data) = rfid.request()
		if not error:
			print ("Tag Detected")

        	(error, uid) = rfid.anticoll()
        	if not error:

			#Print UID
				print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4]))
				print uid
				for i in xrange (len(extract["data"])):

					for value in extract["data"][i].itervalues():
						if uid == value:
							time.sleep(1)
							print "Authorized Tag detected"
							pickle_filepath = "/home/pi/lockstate.pickle"
							with open(pickle_filepath, "rb") as pickle_handle:
								doorstatus = pickle.load(pickle_handle)
								lockstatus = pickle.load(pickle_handle)
								pickle_handle.close()
								print lockstatus
							if lockstatus == "Locked":
								unlock()
#								print ("Open web browser to unlock")
#								webbrowser.get('chromium-browser').open_new("https://www.google.com")
#								p = subprocess.Popen("exec chromium-browser http://google.com", stdout=subprocess.PIPE,shell=True)
#								p = subprocess.Popen("exec chromium-browser https://maker.ifttt.com/trigger/tagopen/with/key/dkA6CLpfLT3CL4wO64893f", stdout=subprocess.PIPE,shell=True)
#								p = subprocess.Popen("exec epiphany-browser https://maker.ifttt.com/trigger/tagopen/with/key/dkA6CLpfLT3CL4wO64893f", stdout=subprocess.PIPE,shell=True)
#								webbrowser.open('https://maker.ifttt.com/trigger/tagopen/with/key/dkA6CLpfLT3CL4wO64893f')
#								webbrowser.open('http://google.com')
#								time.sleep(30)
#								print ("passou comando de abrir browser")
							else:
								lock()
#								print ("Open web browser to lock")
#								webbrowser.get('chromium-browser').open_new("https://www.google.com")
#								p = subprocess.Popen("exec chromium-browser http://google.com", stdout=subprocess.PIPE,shell=True)
#								p = subprocess.Popen("exec chromium-browser https://maker.ifttt.com/trigger/tagclose/with/key/dkA6CLpfLT3CL4wO64893f", stdout=subprocess.PIPE,shell=True)
#								p = subprocess.Popen("exec epiphany-browser https://maker.ifttt.com/trigger/tagclose/with/key/dkA6CLpfLT3CL4wO64893f", stdout=subprocess.PIPE,shell=True)
#								webbrowser.open('https://maker.ifttt.com/trigger/tagclose/with/key/dkA6CLpfLT3CL4wO64893f')
#								webbrowser.open('http://google.com')
#								time.sleep(30)
#								print ("passou comando de abrir browser")

#							time.sleep(30)
#							print ("\nClose web browser.\n")
#							os.system("pkill chromium")
						else:
							continue
							print "Unauthorized Tag detected!"

					time.sleep(1)

#				p.kill()
				print("\nWaiting for RFID tag.\n")


#end of tag reading

except KeyboardInterrupt:
#	if ctrl+C is pressed program is interrupted
#	ends program
#	GPIO.cleanup()
	print('nProgram closed.')
