from socket import *
import sys
import time

def main():
    host = '127.0.0.1'
    port = 65432

    s = socket(AF_INET, SOCK_DGRAM)
    server_address = (host, port)
    print("Joined the communication.")
    while True:
        
        reply = input("Enter your reply: ")  # Get reply from the user
        s.sendto(reply.encode(), server_address)  # Send the reply back to the server
        data, _ = s.recvfrom(1024)  # Receive message from the server
        print("Server:", data.decode())
        aux = data.decode().split( )

        if aux[0] == "Files":
            proof_nr = aux[1]
            time.sleep(1)
            while(True):
                data,addr = s.recvfrom(1024)
                if(data.decode() == "End"):
                    print("Game Created!")
                    break
                print ("Received File:")
                
                f = open(f"{proof_nr}/{data.decode()}",'wb')

                data,addr = s.recvfrom(1024)
                try:
                    while(data):
                        f.write(data)
                        s.settimeout(2)
                        data,addr = s.recvfrom(1024)
                except timeout:
                    f.close()
                    response = "File Downloaded"
                    s.sendto(response.encode(),addr)

if __name__ == '__main__':
    main()