import sys
import webbrowser
import time
import os
import subprocess

print ("iniciar")
#p = subprocess.Popen("exec chromium-browser http://google.com", stdout=subprocess.PIPE,shell=True)

#webbrowser.open('https://maker.ifttt.com/trigger/tagopen/with/key/dkA6CLpfLT3CL4wO64893f')
os.system("start /wait cmd /c {command}")
webbrowser.open('http://google.com')
#print ("Sleep 5")
time.sleep(15)
print ("Fechar browser")
#
os.system("pkill chromium")

