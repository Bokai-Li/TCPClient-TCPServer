#!/usr/bin/python

import sys
from socket import *
import socket as sk
try:
    for line in sys.stdin:
            if len(line) == 0: break
            sys.stdout.write(line)
            clientSocket=socket(AF_INET, SOCK_STREAM)
            hostPort=int(sys.argv[1])
            host_name = "comp431afa19"
            clientSocket.connect((host_name,hostPort))
            s = clientSocket.makefile("rw")
            s.write(line)
            s.flush()
            sys.stdout.write(s.read())
            s.close()
            clientSocket.close()
    sys.exit
except sk.error:
    print("Connection Error")