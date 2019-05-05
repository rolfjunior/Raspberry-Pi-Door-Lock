import threading
import sys
import BlynkLib
import RPi.GPIO as GPIO
import time
import cPickle as pickle

GPIO.setwarnings(False)

pickle_filepath = "/home/pi/lockstate.pickle"

BLYNK_AUTH = '6bdbb3cd244945fc8ba4f7e15b734ddf'

#Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)

def my_write_handler(value):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(8, GPIO.OUT) #servo
	GPIO.setup(3, GPIO.OUT) #red led
	GPIO.setup(11, GPIO.OUT) #grenn led

	p = GPIO.PWM(8, 50)
	p.start(0)

	with open(pickle_filepath, "rb") as pickle_handle:
		doorstatus = pickle.load(pickle_handle)
		lockstatus = pickle.load(pickle_handle)
		print (doorstatus)
		print (lockstatus)
		print "Fim da verificacao do status."

	print('Current Virtual Pin 1 value: {}'.format(value))
	lockcommand = '{}'.format(value)
	if lockcommand == '1':
		print "The App Lock was pressed!\n"
		if doorstatus == "Closed":
			if lockstatus == "UnLocked":
				print "Door is closed and unlocked. Locking the door!"
				p.ChangeDutyCycle(2.5)  # turn towards 0 degree
				time.sleep(2.9) # sleep 1 second
				doorstatus = "Closed"
				lockstatus = "Locked"
				GPIO.output(3,GPIO.HIGH)
				GPIO.output(11,GPIO.LOW)
				print "Door Locked!\n"
				blynk.notify("Door Locked!")
			else:
				print "Door closed and already Locked, do nothing!\n"
		elif doorstatus == "Open":
			print "Door is open, can not lock it! Do nothing!\n"
			blynk.notify("Cannot Lock door, door is open!")
		else:
			print "Unrecognized door state. Error Here!\n"
		
		
	else:
		print "The App UnLock was Pressed!\n"
		if lockstatus == 'Locked':
			print "UnLocking the door!"
			p.ChangeDutyCycle(12.5) # turn towards 180 degree
			time.sleep(3) # sleep 3 second
			doorstatus = "Closed"
			lockstatus = "UnLocked"
			GPIO.output(3,GPIO.LOW)
			GPIO.output(11,GPIO.HIGH)
			print "Door UnLocked!\n"
			blynk.notify("Door UnLocked!")
		elif lockstatus == "UnLocked":
			print "Door already UnLocked, do nothing!\n"
			blynk.notify("Door Already UnLocked!")
		else:
			print "Unrecognized lockstatus, Error here!\n"
	
	p.stop()
	with open(pickle_filepath, "wb") as pickle_handle:
		pickle.dump(doorstatus, pickle_handle)
		pickle.dump(lockstatus, pickle_handle)
		pickle_handle.close()
	
	
#@blynk.VIRTUAL_READ(0)
#def my_read_handler():
#    # this widget will show some time in seconds..
#    blynk.virtual_write(0, time.ticks_ms() // 1000)

# Start Blynk (this call should never return)
blynk.run()
