#Verifies the door and lock status and locks or unlocks the door
import RPi.GPIO as GPIO
import time
import threading
import sys
import os
import cPickle as pickle

pickle_filepath = "/home/pi/lockstate.pickle"

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT) #servo
GPIO.setup(3, GPIO.OUT) #red led
GPIO.setup(5, GPIO.OUT) #grenn led

p = GPIO.PWM(8, 50)
p.start(0)

with open(pickle_filepath, "rb") as pickle_handle:
	doorstatus = pickle.load(pickle_handle)
	lockstatus = pickle.load(pickle_handle)
	print (doorstatus)
	print (lockstatus)
	print "Fim da verificacao do status."

if (str(sys.argv[1]) == "L"):
	if doorstatus == "Closed":
		if lockstatus == "UnLocked":
			print "Door is closed and unlocked. Locking the door!"
			p.ChangeDutyCycle(2.5)  # turn towards 0 degree
			time.sleep(2.9) # sleep 1 second
			doorstatus = "Closed"
			lockstatus = "Locked"
			GPIO.output(3,GPIO.HIGH)
			GPIO.output(5,GPIO.LOW)
			print "Door Locked!\n"
		else:
			print "Door closed and already Locked, do nothing!\n"
	elif doorstatus == "Open":
		print "Door is open, can not lock it! Do nothing!\n"
	else:
		print "Unrecognized door state. Error Here!\n"

elif(str(sys.argv[1]) == "U"):
	if lockstatus == 'Locked':
		print "UnLocking the door!"
		p.ChangeDutyCycle(12.5) # turn towards 180 degree
		time.sleep(3) # sleep 3 second
		doorstatus = "Closed"
		lockstatus = "UnLocked"
		GPIO.output(3,GPIO.LOW)
		GPIO.output(5,GPIO.HIGH)
		print "Door UnLocked!\n"
        elif lockstatus == "UnLocked":
		print "Door already UnLocked, do nothing!\n"
	else:
		print "Unrecognized lockstatus, Error here!\n"
		
		
p.stop()
with open(pickle_filepath, "wb") as pickle_handle:
	pickle.dump(doorstatus, pickle_handle)
	pickle.dump(lockstatus, pickle_handle)
	pickle_handle.close()
