
from socket import *

def udp_bind(address, port):
	s = None
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.bind((address, port))
	except:
		print "Error creating and binding socket to %s:%d" % (address, port)
	return s
