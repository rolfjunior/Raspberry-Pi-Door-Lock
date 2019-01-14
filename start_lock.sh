#!/bin/sh

sleep 10
#screen -m -d -S fechadura
#screen -S fechadura -X stuff "sudo python /home/pi/lockerv2.py & $(echo '\r')"


screen -m -d -S blynk
screen -S blynk -X stuff "python /home/pi/blynk.py & $(echo '\r')"
