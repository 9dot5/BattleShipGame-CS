from socket import *
import threading
import subprocess
import os
import time
import json

clients = {}
games = []
main_path = os.getcwd()



class Game():
    def __init__(self,id, host):
        self.id = id
        self.host = host
        self.players = []
        self.hash = {}
        self.last_shot=[]




def Join(game_nr,addr,username):
    f = open(f"proof.json","wb")
    data,addr = server_socket.recvfrom(1024)

    try:
        while(data):
            f.write(data)
            server_socket.settimeout(2)
            data,addr = server_socket.recvfrom(1024)
    except timeout:
        f.close()
        
        print("File Downloaded")

    verifier = os.system("zokrates verify")
    if verifier == 0:

        for g in games:
            if g.id == game_nr:
                json_file = open(f"proof.json")
                json_data = json.load(json_file)
                g.hash[f"{username}"] = json_data["inputs"]
                g.players.append(username)

                print(g.hash[f"{username}"])
                print(g.players)
                server_socket.sendto("Game joined successfuly".encode(),addr)
                server_socket.sendto("Play".encode(),addr)

                clients[f"{username}"] = addr
                return
        
        server_socket.sendto("Game does not exist".encode(),addr)
        return
    
    server_socket.sendto("Proof not accepted.".encode(),addr)

        

def Create(game_nr,addr,username):


    f = open(f"proof.json","wb")
    data,addr = server_socket.recvfrom(1024)

    try:
        while(data):
            f.write(data)
            server_socket.settimeout(2)
            data,addr = server_socket.recvfrom(1024)
    except timeout:
        f.close()
        
        print("File Downloaded")

    verifier = os.system("zokrates verify")
    if verifier == 0:

        for g in games:
            if g.id == game_nr:
                print("Game already exists.")
                server_socket.sendto("Game already exists".encode(),addr)
                return

        json_file = open(f"proof.json")
        json_data = json.load(json_file)

        new_game = Game(game_nr,username)
        new_game.players.append(username)
        new_game.hash[f"{username}"] = json_data["inputs"]
        games.append(new_game)

        print(new_game.hash[f"{username}"])
        server_socket.sendto("Game created successfuly".encode(),addr)

        clients[f"{username}"] = addr
        print(clients)
        return
    
    server_socket.sendto("Proof not accepted.".encode(),addr)

    

    

    return

def List(game_nr,addr):
    for g in games:
        if g.id == game_nr:
            response = f"Host: {g.host}. Players: {g.players}"
            server_socket.sendto(response.encode(),addr)
    return

def Report(addr,x,y):

    x_ = f"0x000000000000000000000000000000000000000000000000000000000000000{x}"
    y_ = f"0x000000000000000000000000000000000000000000000000000000000000000{y}"

    for name,address in clients.items():
        if address == addr:
            username = name
    
    for g in games:
        for player in g.players:
            if player == username or g.host == username:


                f = open(f"proof.json","wb")
                data,addr = server_socket.recvfrom(1024)

                try:
                    while(data):
                        f.write(data)
                        server_socket.settimeout(2)
                        data,addr = server_socket.recvfrom(1024)
                except timeout:
                    f.close()
                    
                    print("File Downloaded")

                verifier = os.system("zokrates verify")
                if verifier == 0:

                    json_file = open(f"proof.json")
                    json_data = json.load(json_file)

                    print(json_data["inputs"][2:10])

                    if json_data["inputs"][2:10] == g.hash[f"{username}"] and json_data["inputs"][0] == g.last_shot[0] and json_data["inputs"][1] == g.last_shot[1] :


                        g.hash[f"{username}"] = json_data["inputs"][10:]

                        print(g.hash[f"{username}"])
                        server_socket.sendto("Shot Reported Successfuly".encode(),addr)
                        server_socket.sendto("Your Turn!".encode(),addr)

                        return
                
                server_socket.sendto("Proof not accepted.".encode(),addr)
                server_socket.sendto("Try again:".encode(),addr)
                return
    server_socket.sendto("Player not in a game".encode(),addr) 
    server_socket.sendto("Try again:".encode(),addr)

    return

def Shoot(addr,x,y,target):
    for name,address in clients.items():
        if address == addr:
            username = name
    
    for g in games:
        for player in g.players:
            if player == username:
                for target_ in g.players:
                    if target_ == target:

                        for name2,address2 in clients.items():
                            if name2 == target:
                                target_addr = address2
                        
                        f = open(f"proof.json","wb")
                        data,addr = server_socket.recvfrom(1024)

                        try:
                            while(data):
                                f.write(data)
                                server_socket.settimeout(2)
                                data,addr = server_socket.recvfrom(1024)
                        except timeout:
                            f.close()
                            
                            print("File Downloaded")

                        verifier = os.system("zokrates verify")

                        if verifier == 0:

                            json_file = open(f"proof.json")
                            json_data = json.load(json_file)

                            print(json_data["inputs"])

                            if json_data["inputs"] == g.hash[f"{username}"]:


                                print(g.hash[f"{username}"])
                                server_socket.sendto("Shot Sent successfuly".encode(),addr)
                                server_socket.sendto(f"Recieved Shot: {x} {y}".encode(),target_addr)
                                g.last_shot = [f"0x000000000000000000000000000000000000000000000000000000000000000{x}",f"0x000000000000000000000000000000000000000000000000000000000000000{y}"]
                                return
                            else:
                                print("HASH GO BRR")
                        else:
                            print(f"Verifier go BR? Verifier {verifier}")

                        server_socket.sendto("Failed Proof".encode(),addr)
                        server_socket.sendto("Try again:".encode(),addr)

                        return
                    
                server_socket.sendto("Target not in game".encode(),addr)
                server_socket.sendto("Try again:".encode(),addr)
                return
        server_socket.sendto("Player not in a game".encode(),addr)
        server_socket.sendto("Try again:".encode(),addr)
        return






def start_server(host='127.0.0.1', port=65432):
    global server_socket
    server_socket = socket(AF_INET,SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f'Server listening on {host}:{port}')

    


    while True:
        server_socket.settimeout(None)
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        aux = message.split()
        os.chdir(main_path)


        if aux[0].lower() == "hello":
            server_socket.sendto("Hello".encode(),addr)        

        if aux[0].lower() == "create":
            if len(aux) == 3:
                os.chdir("zokrates_test")
                Create(aux[1],addr,aux[2])
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)

        if aux[0].lower() == "join":
            if len(aux) == 3:
                os.chdir("zokrates_test")
                Join(aux[1],addr,aux[2])
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)

        if aux[0].lower() == "list":
            if len(aux) == 2:
                List(aux[1],addr)
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)
        
        if aux[0].lower() == "report":
            if len(aux) == 3:
                os.chdir("proof2")
                Report(addr,aux[1],aux[2])

        if aux[0].lower() == "shoot":
            if len(aux) == 4:
                os.chdir("proof3")
                Shoot(addr,aux[1],aux[2],aux[3])




if __name__ == '__main__':
    start_server()