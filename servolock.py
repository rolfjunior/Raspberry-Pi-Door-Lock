import RPi.GPIO as GPIO
import threading
import time
import sys
import os
import cPickle as pickle

pickle_filepath = "/home/pi/lockstate.pickle"

class servolock:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		self.time_stamp = time.time()
		GPIO.setup(11, GPIO.IN)
		GPIO.setup(13, GPIO.IN)
		GPIO.setup(5, GPIO.IN)
		GPIO.setup(10, GPIO.OUT)
		GPIO.setup(12, GPIO.OUT)
		GPIO.add_event_detect(11, GPIO.RISING, callback=self.lock)
		GPIO.add_event_detect(13, GPIO.RISING, callback=self.unlock)
		GPIO.add_event_detect(5, GPIO.BOTH, callback=self.sensor)
				
	def lock(self,channel):
		self.time_now = time.time()
		if(self.time_now - self.time_stamp) >= 0.3:	
			print "The Button for Lock is Pressed!\n"
			os.system("python door_lock.py L")
		self.time_stamp = self.time_now
	def unlock(self,channel):
		self.time_now = time.time()
		if(self.time_now - self.time_stamp) >= 0.3:
			print "The Button for Unlock is Pressed!\n"
			os.system("python door_lock.py U")
		self.time_stamp = self.time_now
		
	def lockit(self):
		print "Locking with authorized RFID tag!\n"
		os.system("python door_lock.py L")
	def unlockit(self):
		print "Unlocking with authorized RFID tag!\n"
		os.system("python door_lock.py U")

	def sensor (self, channel):
		if (GPIO.input(5) != 1):
			time.sleep(6)
#			self.time_now = time.time()
#			if(self.time_now - self.time_stamp) >= 5.1:
			if (GPIO.input(5) != 1):
				print "Door Closed"
				doorstatus = "Closed"
				lockstatus = "UnLocked"
				with open(pickle_filepath, "wb") as pickle_handle:
					pickle.dump(doorstatus, pickle_handle)
					pickle.dump(lockstatus, pickle_handle)
					pickle_handle.close()
				print "The door is closed! Automatically Locking door\n"
				os.system("python door_lock.py L")
				GPIO.output(10,GPIO.HIGH)
				GPIO.output(12,GPIO.LOW)
#			self.time_stamp = self.time_now

		else:
			print "Door open"
			doorstatus = "Open"
			lockstatus = "UnLocked"
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			print "The door is open, making sure it has the correct status\n"			  
			GPIO.output(10,GPIO.LOW)
			GPIO.output(12,GPIO.HIGH)
