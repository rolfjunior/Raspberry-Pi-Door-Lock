import requests
import threading
import time
import sys
sys.path.insert(0, "/home/pi/pi-rc522/ChipReader")
from pirc522 import RFID
from servolock import servolock
import signal
import os
import json
from pprint import pprint
import cPickle as pickle

pickle_filepath = "/home/pi/lockstate.pickle"

#doorstatus = "Closed"
#lockstatus = "Locked"
#
#with open(pickle_filepath, "wb") as pickle_handle:
#	pickle.dump(doorstatus, pickle_handle)
#	pickle.dump(lockstatus, pickle_handle)
#	pickle_handle.close()


with open('card_data.json') as data_file:
	extract = json.load(data_file)

#start tags reading, waiting for tags
srv = servolock()
       
try:
	rdr = RFID()
        print ("Waiting for tag\n")
        
	util = rdr.util()

	util.debug = False
	door_locked = 1


	while True:
		#Request tag
		(error, data) = rdr.request()
		if not error:
			print ("Tag Detected")

        	(error, uid) = rdr.anticoll()
        	if not error:

           		#Print UID
           		print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4]))
#				print uid
			for i in xrange (len(extract["data"])):
			    for value in extract["data"][i].itervalues():
	    				  
					if uid == value:
						print "Authorized Tag detected"
						if (door_locked):
							srv.lockit()
							door_locked = 0	
						else:
							srv.unlockit()
							door_locked = 1
					else:
						print "Unauthorized Tag detected!"
						continue
                        	
					time.sleep(1)
					print("Waiting for RFID tag.\n")
#end of tag reading	

except KeyboardInterrupt:
    # ic ctrl+C is pressed program is interrupted
    #ends program
    GPIO.cleanup()
    print('nProgram closed.')
