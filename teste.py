import webbrowser
import time


def lock():
	print ("passou comando de abrir browser")
	webbrowser.open('https://maker.ifttt.com/trigger/tagclose/with/key/dkA6CLpfLT3CL4wO64893f')
	time.sleep(10)
	print ("\nClose web browser.\n")
	os.system("pkill chromium")

def unlock():
	print ("passou comando de abrir browser")
	webbrowser.open('https://maker.ifttt.com/trigger/tagopen/with/key/dkA6CLpfLT3CL4wO64893f')
	time.sleep(10)
	print ("\nClose web browser.\n")
	os.system("pkill chromium")
