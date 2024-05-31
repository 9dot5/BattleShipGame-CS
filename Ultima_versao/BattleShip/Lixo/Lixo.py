'''    first_file = "out"
    second_file = "proving.key"

    server_socket.sendto("Files 1".encode(),addr)

    time.sleep(1)

    server_socket.sendto(first_file.encode(),addr)

    f=open(first_file,"rb")
    data = f.read(1024)
    print("Sending...")
    while (data):
        if(server_socket.sendto(data,addr)):

            data = f.read(1024)

    response,addr = server_socket.recvfrom(1024)
    print(response.decode())

    f.close()

    server_socket.sendto(second_file.encode(),addr)

    f=open(second_file,"rb")
    data = f.read(1024)
    print("Sending...")
    while (data):
        if(server_socket.sendto(data,addr)):

            data = f.read(1024)

    response,addr = server_socket.recvfrom(1024)
    print(response.decode())



  

    End = "End"

    server_socket.sendto(End.encode(),addr)
    f.close()'''



'''if aux[0] == "Files":
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
                    s.sendto(response.encode(),addr)'''