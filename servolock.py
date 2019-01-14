#Reads Input from butons ans sensor ans writes comands to leds
import RPi.GPIO as GPIO
import threading
import time
import sys
import os
import cPickle as pickle

pickle_filepath = "/home/pi/lockstate.pickle"

with open(pickle_filepath, "rb") as pickle_handle:
	doorstatus = pickle.load(pickle_handle)
	lockstatus = pickle.load(pickle_handle)

print "servolock initiated"

GPIO.setwarnings(False)

class servolock:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		self.time_stamp = time.time()

		GPIO.setup(7, GPIO.IN) #lock button
		GPIO.setup(13, GPIO.IN) #unlock button
		GPIO.setup(5, GPIO.IN) #sensor
		GPIO.setup(3, GPIO.OUT) #red led
		GPIO.setup(11, GPIO.OUT) #green led

		GPIO.add_event_detect(7, GPIO.RISING, callback=self.lock)
		GPIO.add_event_detect(13, GPIO.RISING, callback=self.unlock)
		GPIO.add_event_detect(5, GPIO.BOTH, callback=self.sensor)

		if lockstatus == "Locked":
			GPIO.output(3,GPIO.HIGH)
			GPIO.output(11,GPIO.LOW)
		else:
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)

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
		GPIO.remove_event_detect(5)
		print "Sensor change detected, deativated GPIO evente detect for sensor"
		if (GPIO.input(5) == 1):
			print "Door open detected"
			doorstatus = "Open"
			lockstatus = "UnLocked"
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)
		elif (GPIO.input(5) != 1):
			print "Door closed detected"
			doorstatus = "Closed"
			lockstatus = "UnLocked"
			print "Writing status to pickle"
			print doorstatus
			print lockstatus
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			print "Debounce"
			time.sleep(5)
			if (GPIO.input(5) != 1):
				print "Door still closed, locking automatically"
				os.system("python door_lock.py L")
			else:
				print "Door not closed anymore! Adjusting status and led"
				doorstatus = "Open"
				lockstatus = "UnLocked"
				print "Writing status to pickle"
				print doorstatus
				print lockstatus
				with open(pickle_filepath, "wb") as pickle_handle:
					pickle.dump(doorstatus, pickle_handle)
					pickle.dump(lockstatus, pickle_handle)
					pickle_handle.close()
				GPIO.output(3,GPIO.LOW)
				GPIO.output(11,GPIO.HIGH)
		else:
			print "Door status unknown. Do nothing!\n"

		print "end of sensor read command. Reactivating sensor pin read\n"
		GPIO.add_event_detect(5, GPIO.BOTH, callback=self.sensor)
