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
	
	print "Starting pins"
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(8, GPIO.OUT) #servo
	GPIO.setup(3, GPIO.OUT) #red led
	GPIO.setup(5, GPIO.OUT) #grenn led
	GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #lock button
	GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #sensor

	print "adjusting leds  and virtual pin according to piclke"
	with open(pickle_filepath, "rb") as pickle_handle:
		doorstatus = pickle.load(pickle_handle)
		lockstatus = pickle.load(pickle_handle)
		pickle_handle.close()
	if lockstatus == 'Locked':
		GPIO.output(5,GPIO.LOW) #apaga led verde
		GPIO.output(3,GPIO.HIGH) #acende led vermelho
	else:
		GPIO.output(3,GPIO.LOW) #apaga led vermelho
		GPIO.output(5,GPIO.HIGH) #acende led verde

	# Register Virtual Pins
	@blynk.VIRTUAL_WRITE(1)

	def my_write_handler(value):
		print "App command received"
		print('Current Virtual Pin 1 value: {}'.format(value))
		lockcommand = '{}'.format(value)
		if lockcommand == '1' or lockcommand == '1.0':
			print "The App Lock was pressed, calling lock command!\n"
			lock(8)
		elif lockcommand == '0'or lockcommand == '0.0':
			print "The App UnLock was Pressed, calling unlock command!\n"
			unlock(8)
	
	print "butao code start"
	def butao(channel):
		if (GPIO.input(7) == 1):
			print "Buton pressed"
			with open(pickle_filepath, "rb") as pickle_handle:
				doorstatus = pickle.load(pickle_handle)
				lockstatus = pickle.load(pickle_handle)
				pickle_handle.close()
			if lockstatus == 'Locked':
				print "Door is locked calling unlock!"
				unlock(8)
			else:
				print "Door is unlocked calling lock!"
				lock(8)

	print "sensor code start"
	def sensor(channel):

		if (GPIO.input(13) != 1):
#			global time_stamp
#			time_stamp = time.time()
			print "Door open detected"
			doorstatus = "Open"
			lockstatus = "UnLocked"
			print "Writing status to pickle"
			with open(pickle_filepath, "wb") as pickle_handle:
				pickle.dump(doorstatus, pickle_handle)
				pickle.dump(lockstatus, pickle_handle)
				pickle_handle.close()
			print "Adjusting leds to unlocked"
			GPIO.output(3,GPIO.LOW)
			print "apaga led vermelho"
			GPIO.output(5,GPIO.HIGH)
			print "acende led verde\n"
			blynk.notify("Door Open!")

		elif (GPIO.input(13) == 1):
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
			print "blink leds"
#			time_now = time.time()
#			if (time_now - time_stamp) >= 5:
			GPIO.output(3,GPIO.HIGH)
			print "acende led vermelho"
			GPIO.output(5,GPIO.LOW)
			print "apaga led verde"
			GPIO.output(3,GPIO.LOW)
			GPIO.output(5,GPIO.HIGH)
			time.sleep(1.2)
			GPIO.output(3,GPIO.HIGH)
			GPIO.output(5,GPIO.LOW)
			time.sleep(1.2)
			GPIO.output(3,GPIO.LOW)
			GPIO.output(5,GPIO.HIGH)
			time.sleep(1.2)
			GPIO.output(3,GPIO.HIGH)
			GPIO.output(5,GPIO.LOW)
			time.sleep(1.2)
			print "dorme 1,2 segundo"

			if (GPIO.input(13) == 1):
				print "Door still closed, deativating GPIO event detect for sensor to lock the door"
				GPIO.remove_event_detect(13)
				print "Door still closed, locking automatically"
				lock(8)
				time.sleep(3.2)
				print "Door locked. reactivating sensor pin read\n"
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(5,GPIO.LOW)
				time.sleep(0.2)
				GPIO.output(3,GPIO.LOW)
				GPIO.output(5,GPIO.HIGH)
				time.sleep(0.2)
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(5,GPIO.LOW)
				print "Reactivating sensor pin\n"
				GPIO.add_event_detect(13, GPIO.BOTH, callback=sensor, bouncetime=1000)
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
				print "Adjusting leds to Unlocked"
				GPIO.output(3,GPIO.LOW)
				GPIO.output(5,GPIO.HIGH)

		else:
			print "Door status unknown. Do nothing!\n"

	print "lock code start"
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
				print "Adjusting leds"
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(5,GPIO.LOW)

			else:
				print "Door closed and already Locked, do nothing!\n"
				blynk.virtual_write(1, 1)
		elif doorstatus == "Open":
			print "Door is open, can not lock it! Do nothing!\n"
			blynk.notify("Cannot Lock door, door is open!")
			blynk.virtual_write(1, 0)
		else:
			print "Unrecognized door state. Error Here!\n"

	print "unlock code start"
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
			print "ajustando leds"
			GPIO.output(3,GPIO.LOW)
			GPIO.output(5,GPIO.HIGH)

		elif lockstatus == "UnLocked":
			print "Door already UnLocked, do nothing!\n"
			blynk.notify("Door Already UnLocked!")
		else:
			print "Unrecognized lockstatus, Error here!\n"


	print "liga pino do botao"
	GPIO.add_event_detect(7, GPIO.RISING, callback=butao, bouncetime=200)
	print "liga pino do sensor"
	GPIO.add_event_detect(13, GPIO.BOTH, callback=sensor, bouncetime=1000)
#	GPIO.add_event_detect(13, GPIO.RISING, callback=sensor, bouncetime=1000)

	#@blynk.VIRTUAL_READ(0)
	#def my_read_handler():
	#    # this widget will show some time in seconds..
	#    blynk.virtual_write(0, time.ticks_ms() // 1000)

	# Start Blynk (this call should never return)
	blynk.run()
