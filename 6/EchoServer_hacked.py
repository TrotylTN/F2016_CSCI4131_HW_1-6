#!/usr/bin/env python3
# See https://docs.python.org/3.2/library/socket.html
# for a decscription of python socket and its parameters
import socket
import os
import sys

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
cur_pwd = os.getcwd()

#You might find it useful to define variables similiar to the one above
#for each kind of response message

#Outline for processing a request - indicated by the call to processreq below
#the outline below is for a GET request, though the others should be similar (but not the same)
#remember, you have an HTTP Message that you are parsing
#so, you want to parse the message to get the first word on the first line
#of the message (the HTTP command GET, HEAD, ????) if the HTTP command is not known you should respond with an error
#then get the    resource (file path and name) - python strip and split should help
#Next,    does the resource have a legal name (no % character)
#            if false    - construct an error message for the response and return
#                     if true - check to see if the resource exists
#                if false - construct an error message for the response and return
#                if true - check to see if the permissions on the resource for others are ok
#                    if false - construct an error message for the response and resturn
#                    if true - Success!!!
#                                                            open the resource (file)
#                                                            read the resource into a buffer
#                                                            create a response message by concatenating the OK message above with
#                                                            the string you read in from the file
#                                                            return the response
#
def processreq(req):
    req_by_word = req.split(' ')
    req_type = req_by_word[0]
    req_end = req_by_word[-1]
    req_path = ' '.join(req_by_word[1:-1])

    OK = '{} 200 OK{}{}{}'.format(req_end,CRLF,CRLF,CRLF)
    ERROR_403 = '{} 403 Forbidden{}{}{}'.format(req_end,CRLF,CRLF,CRLF)
    ERROR_404 = '{} 404 Not Found{}{}{}'.format(req_end,CRLF,CRLF,CRLF)
    ERROR_405 = '{} 405 Method Not Allowed{}{}{}'.format(req_end,CRLF,CRLF,CRLF)
    ERROR_406 = '{} 406 Not Acceptable Response{}{}{}'.format(req_end,CRLF,CRLF,CRLF)
    REDIR_301 = '{} 301 Move Permanently{}{}{}'.format(req_end,CRLF,CRLF,CRLF)

    if not req_type in ['GET', 'HEAD']:
        return ERROR_405
    req_path = req_path.lstrip('/')
    if req_path == "csumn":
        return REDIR_301 + "https://www.cs.umn.edu/"
    if '%' in req_path:
        return ERROR_404 + add_content_after_head("404.html")
    if not os.path.isfile(req_path):
        return ERROR_404 + add_content_after_head("404.html")
    req_file_info = os.stat(req_path)
    req_file_perm = bin(req_file_info.st_mode)[-9:]
    if (req_file_perm[6] == '1'):
        return OK + add_content_after_head(req_path)
    else:
        return ERROR_403 + add_content_after_head("403.html")

def add_content_after_head(filename):
    fd = open(filename, "r")
    msg = fd.read()
    fd.close()
    return msg


def client_talk(client_sock, client_addr):
    print('talking to {}'.format(client_addr))
    data = client_sock.recv(BUFSIZE)
    # note, here is where you decode the data and process the request
    req = data.decode('utf-8')
    # then, you'll need a routine to process the data, and formulate a response
    response = processreq(req)
    print(response)
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
    parser.add_argument('--host', type=str, default='localhost',
                        help='specify a host to operate on (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=9001,
                        help='specify a port to operate on (default: 9001)')
    args = parser.parse_args()
    return (args.host, args.port)


if __name__ == '__main__':
    (host, port) = parse_args()
    EchoServer(host, port)
