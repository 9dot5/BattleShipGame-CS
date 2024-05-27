#!/usr/bin/env python

from socket import *
import sys
import select

while(True):

    host="0.0.0.0"
    port = 9999
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind((host,port))

    addr = (host,port)
    buf=1024*10



    data,addr = s.recvfrom(buf)
    if(data.decode() == "End"):
        break
    print ("Received File:"),data.strip()
    f = open(data.strip(),'wb')

    data,addr = s.recvfrom(buf)
    try:
        while(data):
            f.write(data)
            s.settimeout(2)
            data,addr = s.recvfrom(buf)
    except timeout:
        f.close()
        response = "File Downloaded"
        s.sendto(response.encode(),addr)
        s.close()
        print("File Downloaded")


       