
from socket import *

TCP_BACKLOG = 5

def udp_bind(address, port):
	"""Return an UDP socket that has been bound to a local address"""
	s = None
	try:
		s = socket(AF_INET, SOCK_DGRAM)
		s.bind((address, port))
	except:
		print "Error binding to UDP/%s:%d" % (address, port)
	return s

def tcp_listen(address, port):
	"""Return a TCP socket that is bound to local address and port and can be selected and accepted"""
	s = None
	try:
		s = socket(AF_INET, SOCK_STREAM)
		s.bind((address, port))
		s.listen(TCP_BACKLOG)
	except:
		print "Error binding to TCP/%s:%d" & (address, port)
	return s

def tcp_connect(address, port):
	"""Return a TCP socket that has been connected to remote address and port"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((address, port))
	except:
		print "Error connecting to TCP/%s:%d" & (address, port)
	return s

	