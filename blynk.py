import threading
import sys
import os
import BlynkLib

BLYNK_AUTH = '6bdbb3cd244945fc8ba4f7e15b734ddf'

#Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)

def my_write_handler(value):
	print('Current V1 value: {}'.format(value))
	lockcommand = '{}'.format(value)
	if lockcommand == '1':
		print "The App Lock was pressed!\n"
		os.system("python door_lock.py L")
	else:
		print "The App UnLock was Pressed!\n"
		os.system("python door_lock.py U")
	
#@blynk.VIRTUAL_READ(0)
#def my_read_handler():
#    # this widget will show some time in seconds..
#    blynk.virtual_write(0, time.ticks_ms() // 1000)

# Start Blynk (this call should never return)
blynk.run()

