#!/bin/sh

sleep 15
screen -m -d -S fechadura
screen -S fechadura -X stuff "sudo python /home/pi/locker.py & $(echo '\r')"


screen -m -d -S blynk
screen -S blynk -X stuff "python /home/pi/blynk.py & $(echo '\r')"
