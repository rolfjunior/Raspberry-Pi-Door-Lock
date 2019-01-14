import threading
import sys
import os
import time
import cPickle as pickle

pickle_filepath = "/home/pi/lockstate.pickle"

doorstatus = "Closed"
lockstatus = "Locked"


with open(pickle_filepath, "wb") as pickle_handle:
	pickle.dump(doorstatus, pickle_handle)
	pickle.dump(lockstatus, pickle_handle)
	pickle_handle.close()

