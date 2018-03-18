# Raspberry-Pi-Google-Assistant-Blynk-RFID---Door-Lock
Control a door lock using Blynk app, Google Assistant, RFID  tags or buttons.
1. Able to Read RFID cards for Authentication and will unlock and lock the Door
2. Able to Read Button inputs for unlocking and locking the Door
3. Use blynk app to control the door lock, control blynk app using google assistant
4. Blink leds to show door status

#HOW TO INSTALL

1. Use the interactive menu to enable the SPI Interface and VNC server.
	1.1 - sudo raspi-config

2. Install pirc522 from this link 
https://github.com/ondryaso/pi-rc522
	2.1 - git clone https://github.com/ondryaso/pi-rc522.git
	2.2 - cd pi-rc522
	2.3 - sudo python setup.py install

3.Clone the code from git and copy all the files in your raspberry pi under /home/pi
	3.1 - sudo git clone https://github.com/rolfjunior/Raspberry-Pi-Door-Lock
  
4.A Raspberry-Pi-Door-Lock folder will be created with the files inside of it, move the files to /home/pi/
Using file manager do copy and paste or
	4.1 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/locker.py /home/pi/
	4.2 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/start_lock.sh /home/pi/
	4.3 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/card_data.json /home/pi/
	4.4 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/door_lock.py /home/pi/
	4.5 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/servolock.py /home/pi/
	4.6 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/blynk.py /home/pi/
	4.7 - sudo cp /home/pi//Raspberry-Pi-Door-Lock/lockstate.pickle /home/pi/

5.Delete the files on the original folder
	5.1 - to delete all sudo rm /home/pi//Raspberry-Pi-Door-Lock/*
	5.2 - to delete one file sudo rm /home/pi//Raspberry-Pi-Door-Lock/door_lock.py

6.Give Executable Access to locker.py
	6.1 - sudo chmod -x /home/pi/locker.py or sudo chmod 777 /home/pi/locker.py
	
7. Read tags number and add them to the autorized tags list. Scan the RFID key fobs and Edit the key data in card_data.json,
Whenever you scan a new key Fob it will print some card data such as [82,101,194,16,220] copy that from the output screen and update the card_data.json dictionary value or add a new value as you see fit.
	7.1 - python locker.py
	7.2 - sudo nano card_data.json

8.Start the program under /home/pi as python locker.py
	8.1 - sudo python locker.py

9.use the command line "python door_lock.py L" to Move the Servo to Lock Position for the first time For installation
	9.1 - python door_lock.py L

10.Edit crontab to autostart the program on boot
	10.1 - crontab -e
	10.2 - add the line at the end of the file	@reboot /bin/sh /home/pi/start_lock.sh

11.Install Blynk, follow instructions from this link: http://help.blynk.cc/how-to-connect-different-hardware-with-blynk/raspberry-pi/how-to-install-nodejs-library-on-linux
	11.1 - sudo apt-get purge node nodejs node.js -y
	11.2 - sudo apt-get autoremove
	11.3 - curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
	11.4 - sudo apt-get install build-essential nodejs -y
	11.5 - sudo npm install blynk-library -g
	11.6 - sudo npm install onoff -g

12.Install Blynk app on the smartphone
	12.1 - Create new project with one virtual button
	12.2 - Update the blynk.py file with the blynk autentication code
	12.3 - sudo nano blynk.py
	
12.Edit /etc/rc.local
	11.1 - sudo nano etc/rc.local
	11.2 - add the line at the end of the file	su - pi -c '/usr/bin/vncserver :1' &

12.Reboot the Pi and the software will start working.
	12.1 - sudo reboot
