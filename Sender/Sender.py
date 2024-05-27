#!/usr/bin/env python

from socket import *
import sys

s = socket(AF_INET,SOCK_DGRAM)
host =sys.argv[1]
port = 9999
buf =1024*10
addr = (host,port)

first_file = "out"
second_file = "proving.key"

s.sendto(first_file.encode(),addr)

f=open(first_file,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        print("sending ...")
        data = f.read(buf)

response,addr = s.recvfrom(buf)
print(response.decode())

f.close()

s.sendto(second_file.encode(),addr)

f=open(second_file,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        print("sending ...")
        data = f.read(buf)

response,addr = s.recvfrom(buf)
print(response.decode())

End = "End"

s.sendto(End.encode(),addr)

f.close()
s.close()