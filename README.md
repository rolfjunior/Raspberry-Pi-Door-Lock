# Raspberry-Pi-Google-Assistant-Blynk-RFID---Door-Lock
Control a door lock using Blynk app, Google Assistant, RFID  tags or buttons.
1. Able to Read RFID cards for Authentication and will unlock and lock the Door
2. Able to Read Button inputs for unlocking and locking the Door
3. Use blynk app to control the door lock, control blynk app using google assistant
4. Blink leds to show door status

#HOW TO INSTALL

1.  Folow the steps on this link
http://www.instructables.com/id/Raspberry-Pi-3-Model-B-MIFARE-RC522-RFID-Tag-Readi/
	1.1 - sudo apt-get install python2.7-dev
	1.2 - git clone https://github.com/lthiery/SPI-Py.git
	1.3 - cd SPI-Py
	1.4 - sudo python setup.py install
	1.5 - git clone https://github.com/mxgxw/MFRC522-python.git
	1.6 - cd MFRC522-python
	1.7 - python Read.py

2. Install pirc522 from this link 
https://github.com/ondryaso/pi-rc522
	2.1 - git clone https://github.com/ondryaso/pi-rc522.git
	2.2 - cd pi-rc522
	2.3 - python setup.py install

3.Clone the code from git and copy all the files in your raspberry pi under /home/pi
	3.1 - sudo git clone https://github.com
  
4.A door_lock_pi folder will be created with the files inside of it move the files to /home/pi
Using file manager do copy and paste or
	4.1 - sudo cp /home/pi/door_lock_pi/locker.py /home/pi/
	4.2 - sudo cp /home/pi/door_lock_pi/start_lock.sh /home/pi/
	4.3 - sudo cp /home/pi/door_lock_pi/card_data.json /home/pi/
	4.4 - sudo cp /home/pi/door_lock_pi/door_lock.py /home/pi/
	4.5 - sudo cp /home/pi/door_lock_pi/servolock.py /home/pi/


5.Delete the files on the original folder
	5.1 - to delete all sudo rm /home/pi/door_lock_pi/*
	5.2 - to delete one file sudo rm /home/pi/door_lock_pi/door_lock.py

6. Edit crontab
	6.1 - crontab -e
	6.2 - add the line at the endo of the file @reboot /bin/sh /home/pi/start_lock.sh

7.Give Executable Access to locker.py
	7.1 - sudo chmod -x /home/pi/locker.py or sudo chmod 777 /home/pi/locker.py


8.use the command line "python door_lock.py L" to Move the Servo to Lock Position for the first time For installation
	8.1 - python door_lock.py L

9.Start the program under /home/pi as python locker.py
	9.1 - sudo python locker.py

10.Scan the RFID key fobs and Edit the key data in card_data.json,
Whenever you scan a new key Fob it will print some card data such as
[82,101,194,16,220] copy that from the output screen and update the card_data.json dictionary
value or add a new value as you see fit.
Reboot the Pi and the software will start working.
