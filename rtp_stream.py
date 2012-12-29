"""
Functionality for streaming data over RTP
"""

import random
from rtp import *
import select
from socket import *
from socket_util import *
import threading
import time

FRAMES_PER_PACKET = 800

class RTPStream(threading.Thread):
	"""
	Streams PCM audio over RTP to a list of recipients
	"""
	def __init__(self, recipients, stream_data):
		threading.Thread.__init__(self)
		self.recipients = list(recipients) # copy
		self.stream_data = stream_data
		self.ssrc = random.randint(0, 2**32 - 1)
		self.sequence_number = random.randint(0, 2**16 - 1) # initial value + number of frames sent
		self.timestamp = random.randint(0, 2**32 - 1)
		self.counter = 0 # number of frames sent

		while True:
			rtp_port = random.randint(1024, 2**15 * 2 - 2) # Even port. 2**16 is not usable and 2**16 - 1 might be needed for RTCP.
			rtcp_port = rtp_port + 1
			self.rtp_socket = udp_bind("0.0.0.0", rtp_port)
			self.rtcp_socket = udp_bind("0.0.0.0", rtcp_port)
			if not self.rtp_socket or not self.rtcp_socket:
				print "Could not bind both RTP and RCTP ports, retrying..."
				continue
			break

	def stop(self):
		self.running = False

	def run(self):
		print "Started RTP streaming to %s." % ", ".join([addr+":"+str(port) for addr, port in self.recipients])

		self.running = True
		packet = RTPPacket() # We'll reuse this for efficiency.
		self.starttime = time.time()
		while self.running:

			# rtp timing
			next_packet = self.starttime + float(self.counter) / 8000.0
			delay = max(0.0, next_packet - time.time())
			time.sleep(delay)

			# check for any incoming rtcp messages
			ready_in, _, _ = select.select([self.rtp_socket], [], [], 0)
			if self.rtp_socket in ready_in:
				data = rtcp_socket.recvfrom(1500)
				print "Received RTCP packet:", data

			# create rtp packet and send it to all recipients
			packet.ssrc = self.ssrc
			packet.timestamp = self.timestamp
			packet.sequence_number = self.sequence_number
			packet.payload_type = PAYLOAD_MULAW
			packet.payload = self.stream_data[self.counter : self.counter + FRAMES_PER_PACKET]
			for recipient in self.recipients:
				rtp_payload = packet.serialize()
				self.rtp_socket.sendto(rtp_payload, recipient)

			# increment counters for next packet
			self.counter += FRAMES_PER_PACKET
			self.timestamp += FRAMES_PER_PACKET
			self.sequence_number += 1
			if self.counter > len(self.stream_data) or 0 == len(self.recipients):
				running = False

		print "Stopped RTP streaming to %s." % ", ".join([addr+":"+str(port) for addr, port in self.recipients])




if __name__ == "__main__":

	wav_file = open("cache/merrygo.wav", "rb")
	wav_data = wav_file.read()[44:]
	wav_file.close()
	stream = RTPStream([("localhost", 6000)], wav_data)
	stream.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print "\nReceived ^C, shutting down"
		stream.running = False
		stream.join()