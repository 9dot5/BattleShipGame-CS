import socket
import threading
import subprocess
import os
import time

clients = {}
games = []



class Game():
    def __init__(self,id, host):
        self.id = id
        self.host = host
        self.players = []




def Join(game_nr,addr,username):
    for g in games:
        if g.id == game_nr:
            g.players.append(username)
            clients[f"{username}"] = addr
            server_socket.sendto("Joined Game".encode(),addr)
        else:
            print("Game doesn't exist.")
    return

def Create(game_nr,addr,username):

    for g in games:
        if g.id == game_nr:
            print("Game already exists.")
            return
    
    first_file = "out"
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

    game = Game(game_nr,username)
    games.append(game)
    clients[f"{username}"] = addr

    End = "End"

    server_socket.sendto(End.encode(),addr)

    f.close()

    

    return

def List(game_nr,addr):
    for g in games:
        if g.id == game_nr:
            response = f"Host: {g.host}. Players: {g.players}"
            server_socket.sendto(response.encode(),addr)
    return



def start_server(host='127.0.0.1', port=65432):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f'Server listening on {host}:{port}')
    


    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        aux = message.split()

        

        if aux[0].lower() == "create":
            if len(aux) == 3:
                os.chdir("zokrates_test")
                Create(aux[1],addr,aux[2])
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)

        if aux[0].lower() == "join":
            if len(aux) == 3:
                Join(aux[1],addr,aux[2])
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)

        if aux[0].lower() == "list":
            if len(aux) == 2:
                List(aux[1],addr)
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)




if __name__ == '__main__':
    start_server()