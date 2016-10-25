#!/usr/bin/env python3
# See https://docs.python.org/3.2/library/socket.html
# for a decscription of python socket and its parameters
import socket

from threading import Thread
from argparse import ArgumentParser

# for the server you may find the following python libraries useful:
#import os - check to see if a file exists in python -
# e.g., os.path.isfile, os.path.exists

#import stat
#check if a file has others permissions set, os.stat

#import sys - enables you to get the argument vector (argv) from command line and use
# values passed in from the command line


#other defintions that will come in handy for getting data and
#constructing a response
BUFSIZE = 4096
CRLF = '\r\n'
OK = 'HTTP/1.0 200 OK{}{}{}'.format(CRLF,CRLF,CRLF)
#You might find it useful to define variables similiar to the one above
#for each kind of response message

#Outline for processing a request - indicated by the call to processreq below
#the outline below is for a GET request, though the others should be similar (but not the same)
#remember, you have an HTTP Message that you are parsing
#so, you want to parse the message to get the first word on the first line
#of the message (the HTTP command GET, HEAD, ????) if the HTTP command is not known you should respond with an error
#then get the	resource (file path and name) - python strip and split should help
#Next,	does the resource have a legal name (no % character)
#			if false	- construct an error message for the response and return
#					 if true - check to see if the resource exists
#				if false - construct an error message for the response and return
#				if true - check to see if the permissions on the resource for others are ok
#					if false - construct an error message for the response and resturn
#					if true - Success!!!
#															open the resource (file)
#															read the resource into a buffer
#															create a response message by concatenating the OK message above with
#															the string you read in from the file
#															return the response
#


def client_talk(client_sock, client_addr):
	print('talking to {}'.format(client_addr))
	data = client_sock.recv(BUFSIZE)
    # note, here is where you decode the data and process the request
	req = data.decode('utf-8')
	# then, you'll need a routine to process the data, and formulate a response
	# response = processreq(req)
	#once have the response, you send it
	client_sock.send(bytes(response, 'utf-8'))

	# clean up
	client_sock.shutdown(1)
	client_sock.close()
	print('connection closed.')

class EchoServer:
	def __init__(self, host, port):
		print('listening on port {}'.format(port))
		self.host = host
		self.port = port

		self.setup_socket()

		self.accept()

		self.sock.shutdown()
		self.sock.close()

	def setup_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.sock.listen(128)

	def accept(self):
		while True:
			(client, address) = self.sock.accept()
			th = Thread(target=client_talk, args=(client, address))
			th.start()

def parse_args():
	parser = ArgumentParser()
	parser.add_argument('--host', type=str, default='localhost', help='specify a host to operate on (default: localhost)')
	parser.add_argument('-p', '--port', type=int, default=9001, help='specify a port to operate on (default: 9001)')
	args = parser.parse_args()
	return (args.host, args.port)


if __name__ == '__main__':
	(host, port) = parse_args()
	EchoServer(host, port)
