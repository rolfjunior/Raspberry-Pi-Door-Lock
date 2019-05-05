import threading
import sys
import BlynkLib
import RPi.GPIO as GPIO
import time
import datetime
import cPickle as pickle

pickle_filepath = "/home/pi/lockstate.pickle"

BLYNK_AUTH = '6bdbb3cd244945fc8ba4f7e15b734ddf'

if __name__ == "__main__":
	#Initialize Blynk
	blynk = BlynkLib.Blynk(BLYNK_AUTH)

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(8, GPIO.OUT) #servo
	GPIO.setup(3, GPIO.OUT) #red led
	GPIO.setup(11, GPIO.OUT) #grenn led
	GPIO.setup(7, GPIO.IN) #lock button
	GPIO.setup(13, GPIO.IN) #unlock button
	GPIO.setup(5, GPIO.IN) #sensor

	with open(pickle_filepath, "rb") as pickle_handle:
		doorstatus = pickle.load(pickle_handle)
		lockstatus = pickle.load(pickle_handle)
		pickle_handle.close()
	if lockstatus == 'Locked':
		GPIO.output(11,GPIO.LOW)
		GPIO.output(3,GPIO.HIGH)
	else:
		GPIO.output(3,GPIO.LOW)
		GPIO.output(11,GPIO.HIGH)

	# Register Virtual Pins
	@blynk.VIRTUAL_WRITE(1)

	def my_write_handler(value):
		print('Current Virtual Pin 1 value: {}'.format(value))
		lockcommand = '{}'.format(value)
		if lockcommand == '1' or lockcommand == '1.0':
			print "The App Lock was pressed!\n"
			lock(8)
		elif lockcommand == '0'or lockcommand == '0.0':
			print "The App UnLock was Pressed!\n"
			unlock(8)

	def lock(channel):
		print("Servo Lock initialized")
		with open(pickle_filepath, "rb") as pickle_handle:
			doorstatus = pickle.load(pickle_handle)
			lockstatus = pickle.load(pickle_handle)
			pickle_handle.close()
		if doorstatus == "Closed":
			if lockstatus == "UnLocked":
				print "Door is closed and unlocked. Locking the door!"
				p = GPIO.PWM(8, 50)
				p.start(0)
				p.ChangeDutyCycle(2.5)  # turn towards 0 degree
				time.sleep(2.9) # sleep 1 second
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(11,GPIO.LOW)
				doorstatus = "Closed"
				lockstatus = "Locked"
				print("Writing pickle")
				with open(pickle_filepath, "wb") as pickle_handle:
					pickle.dump(doorstatus, pickle_handle)
					pickle.dump(lockstatus, pickle_handle)
					pickle_handle.close()
				print "Door Locked!\n"
				blynk.notify("Door Locked!")
				blynk.virtual_write(1, 1)
				p.stop()
			else:
				print "Door closed and already Locked, do nothing!\n"
				blynk.virtual_write(1, 1)
		elif doorstatus == "Open":
			print "Door is open, can not lock it! Do nothing!\n"
			blynk.notify("Cannot Lock door, door is open!")
			blynk.virtual_write(1, 0)
		else:
			print "Unrecognized door state. Error Here!\n"

	def unlock(channel):
		print("entrou no servo UnLock")
		with open(pickle_filepath, "rb") as pickle_handle:
			doorstatus = pickle.load(pickle_handle)
			lockstatus = pickle.load(pickle_handle)
			pickle_handle.close()
		if lockstatus == 'Locked':
			print "UnLocking the door!"
			p = GPIO.PWM(8, 50)
			p.start(0)
			p.ChangeDutyCycle(12.5) # turn towards 180 degree
			time.sleep(3.1) # stop servo after 3 seconds
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)
			doorstatus = "Closed"
			lockstatus = "UnLocked"
			print("writing pickle")
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			print "Door UnLocked!\n"
			blynk.notify("Door UnLocked!")
			blynk.virtual_write(1, 0)
			p.stop()
		elif lockstatus == "UnLocked":
			print "Door already UnLocked, do nothing!\n"
			blynk.notify("Door Already UnLocked!")
		else:
			print "Unrecognized lockstatus, Error here!\n"

	def sensor(channel):
		if (GPIO.input(5) == 1):
			print "Door open detected"
			doorstatus = "Open"
			lockstatus = "UnLocked"
			print "Writing status to pickle"
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)
			blynk.notify("Door Open!")
		elif (GPIO.input(5) != 1):
#			global time_stamp
#			time_stamp = time.time()
			print "Door closed detected"
			doorstatus = "Closed"
			lockstatus = "UnLocked"
			print "Writing status to pickle"
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			print "Debounce. Led blinking."
#			time_now = time.time()
#			if (time_now - time_stamp) >= 5:
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)
			time.sleep(1.2)
			GPIO.output(3,GPIO.HIGH)
			GPIO.output(11,GPIO.LOW)
			time.sleep(1.2)
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)
			time.sleep(1.2)
			GPIO.output(3,GPIO.HIGH)
			GPIO.output(11,GPIO.LOW)
			time.sleep(1.2)
			
			if (GPIO.input(5) != 1):
				print "Sensor change detected, deativated GPIO event detect for sensor"
				GPIO.remove_event_detect(5)
				print "Door still closed, locking automatically"
				lock(8)
				time.sleep(3.2)
				print "Door locked. Reactivating sensor pin read\n"
				GPIO.add_event_detect(5, GPIO.BOTH, callback=sensor, bouncetime=1000)
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(11,GPIO.LOW)
				time.sleep(0.2)
				GPIO.output(3,GPIO.LOW)
				GPIO.output(11,GPIO.HIGH)
				time.sleep(0.2)
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(11,GPIO.LOW)
				print "Sensor pin reactivated\n"
				MyDateTime = datetime.datetime.now()
				print MyDateTime.strftime("Time: %H:%M:%S")
			else:
				print "Door not closed anymore! Adjusting status and led"
				doorstatus = "Open"
				lockstatus = "UnLocked"
				print "Writing status to pickle"
				with open(pickle_filepath, "wb") as pickle_handle:
					pickle.dump(doorstatus, pickle_handle)
					pickle.dump(lockstatus, pickle_handle)
					pickle_handle.close()
				GPIO.output(3,GPIO.LOW)
				GPIO.output(11,GPIO.HIGH)

		else:
			print "Door status unknown. Do nothing!\n"



	GPIO.add_event_detect(7, GPIO.RISING, callback=lock, bouncetime=200)
	GPIO.add_event_detect(13, GPIO.RISING, callback=unlock, bouncetime=200)
	GPIO.add_event_detect(5, GPIO.BOTH, callback=sensor, bouncetime=1000)

	#@blynk.VIRTUAL_READ(0)
	#def my_read_handler():
	#    # this widget will show some time in seconds..
	#    blynk.virtual_write(0, time.ticks_ms() // 1000)

	# Start Blynk (this call should never return)
	blynk.run()
