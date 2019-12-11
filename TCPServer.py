#!/usr/bin/python

# Import socket module
from socket import *
import socket as sk
import sys
import re
from os import path

#regular expression for file path
absoluteFilePath = re.compile('^/[\w./]*$')
#regular expression for HTTP version
httpVersion = re.compile('^HTTP/\d[.]\d$')
try:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverPort = int(sys.argv[1])
        serverSocket.bind(("", serverPort))
        serverSocket.listen(1)
        while True:
                connectionSocket, addr = serverSocket.accept()
                s = connectionSocket.makefile("rw")
                processedInput = [s.readline()]
                validInput = False
                for item in processedInput:
                        item = re.sub(" +", " ", item)
                        ParsedInput = item.split(" ")
                        if ParsedInput[0] != 'GET':
                                messageOut = "ERROR -- Invalid Method token.\n"
                                s.write(messageOut)
                        elif len(ParsedInput) < 2 or (not absoluteFilePath.match(ParsedInput[1])):
                                messageOut = "ERROR -- Invalid Absolute-Path token.\n"
                                s.write(messageOut)
                        elif len(ParsedInput) < 3 or (not httpVersion.match(ParsedInput[2].rstrip("\r\n"))):
                                messageOut = "ERROR -- Invalid HTTP-Version token.\n"
                                s.write(messageOut)
                        elif len(ParsedInput) > 3 and not(len(ParsedInput)==4 and ParsedInput[3]==""):
                                messageOut = "ERROR -- Spurious token before CRLF.\n"
                                s.write(messageOut)
                        else:
                                messageOut = "Method = " + ParsedInput[0] + "\n" + "Request-URL = " + ParsedInput[1] + "\n" + "HTTP-Version = " + ParsedInput[2].rstrip('\r\n')+'\n'
                                s.write(messageOut)
                                validInput = True
                        if validInput:
                                #parse file extension
                                localDirectoryPath = ParsedInput[1][1:]
                                splitPathForExtension = ParsedInput[1].split(".")
                                extension = splitPathForExtension[len(splitPathForExtension)-1]
                                extension = extension.lower()
                                if not (extension == "txt" or extension == "htm" or extension == "html"):
                                        s.write("501 Not Implemented: "+ParsedInput[1]+"\n")
                                elif not path.exists(localDirectoryPath):
                                        s.write("404 Not Found: "+ParsedInput[1]+"\n")
                                else:
                                        f = open(localDirectoryPath, "r")
                                        try:
                                                data = f.read()
                                        except IOError as error:
                                                s.write("ERROR:",str(error))
                                        s.write(data)
                                        f.close()
                s.flush()
                s.close()
                connectionSocket.close()
        serverSocket.close()
        sys.exit()#Terminate the program after sending the corresponding data
except sk.error:
        print("Connection Error")
