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
        self.last_play=["",""]
        self.last_player=[]
        self.current_player=[]
        self.winner = []



def Start(addr):
    for name,address in clients.items():
        if address == addr:
            username = name

    for g in games:
        if g.host == username:
            server_socket.sendto("Starting Game...".encode(),addr)
            g.current_player = addr
            g.last_play = [addr,"start"]
            server_socket.sendto("Your Turn".encode(),addr)


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

    for name,address in clients.items():
        if name == username or address == addr:
            server_socket.sendto("Username or address already exist".encode(),addr)
            server_socket.sendto("Try again".encode(),addr)
            return

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

    for name,address in clients.items():
        if name == username or address == addr:
            server_socket.sendto("Username or address already exist".encode(),addr)
            server_socket.sendto("Try again".encode(),addr)
            return

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

        server_socket.sendto("Game created successfuly".encode(),addr)
        server_socket.sendto("Start when ready".encode(),addr)

        clients[f"{username}"] = addr
        
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

                if addr != g.current_player:
                    server_socket.sendto("Not your turn".encode(),addr)
                    server_socket.sendto(" ".encode(),addr)
                    return

                if g.last_play[1] != "shoot":
                    server_socket.sendto("No shot to Report".encode(),addr)
                    server_socket.sendto("Try again".encode(),addr)
                    return

                

                verifier = os.system("zokrates verify")
                if verifier == 0:

                    json_file = open(f"proof.json")
                    json_data = json.load(json_file)


                    if json_data["inputs"][3:11] == g.hash[f"{username}"] and json_data["inputs"][1] == g.last_shot[0] and json_data["inputs"][2] == g.last_shot[1] :


                        g.hash[f"{username}"] = json_data["inputs"][11:]
                        if json_data["inputs"][0] == "0x0000000000000000000000000000000000000000000000000000000000000001":
                            hit_or_miss = "Hit!"
                        else:
                            hit_or_miss = "Miss"

                        g.last_play=[addr,"report"]
                        server_socket.sendto("Shot Reported Successfuly".encode(),addr)
                        server_socket.sendto(f"{hit_or_miss}".encode(),g.last_player)
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

                        if addr != g.current_player:
                            server_socket.sendto("Not your turn".encode(),addr)
                            server_socket.sendto(" ".encode(),addr)
                            server_socket.sendto(" ".encode(),addr)
                            return

                        if g.last_play[1] == "shoot":
                            server_socket.sendto("Report your shot first".encode(),addr)
                            server_socket.sendto("Try again".encode(),addr)
                            server_socket.sendto("  ".encode(),addr)
                            return

                        verifier = os.system("zokrates verify")

                        if verifier == 0:

                            json_file = open(f"proof.json")
                            json_data = json.load(json_file)



                            if json_data["inputs"] == g.hash[f"{username}"]:


                                print(g.hash[f"{username}"])
                                server_socket.sendto("Shot Sent successfuly".encode(),addr)
                                server_socket.sendto(f"Recieved Shot: {x} {y}".encode(),target_addr)
                                g.last_shot = [f"0x000000000000000000000000000000000000000000000000000000000000000{x}",f"0x000000000000000000000000000000000000000000000000000000000000000{y}"]
                                g.last_play = [addr,"shoot"]
                                g.last_player = addr
                                g.current_player = target_addr
                                return



                        server_socket.sendto("Failed Proof".encode(),addr)
                        server_socket.sendto("Try again:".encode(),addr)
                        server_socket.sendto(" ".encode(),addr)

                        return
                    
                server_socket.sendto("Target not in game".encode(),addr)
                server_socket.sendto("Try again:".encode(),addr)
                server_socket.sendto(" ".encode(),addr)
                return
    server_socket.sendto("Player not in a game".encode(),addr)
    server_socket.sendto("Try again:".encode(),addr)
    server_socket.sendto(" ".encode(),addr)
    return

def Wave(addr):
    for name,address in clients.items():
        if address == addr:
            username = name

    for g in games:
        for player in g.players:
            if player == username:
                addr2 = g.last_player
                server_socket.sendto(f"Player {username} wave their turn! Your Turn".encode(),addr2)
                server_socket.sendto(f"Turn Waved".encode(),addr)
                g.last_player = addr
                g.current_player = addr2

def Victory(addr):
    
    for name,address in clients.items():
        if address == addr:
            username = name

   
    for g in games:
        for player in g.players:
            if player == username:


                                
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

                if addr != g.current_player:
                    server_socket.sendto("Not your turn".encode(),addr)
                    server_socket.sendto(" ".encode(),addr)
                    return

                if g.last_play[1] == "shoot":
                    server_socket.sendto("Report your shot first".encode(),addr)
                    server_socket.sendto("Try again".encode(),addr)
                    return

                verifier = os.system("zokrates verify")

                if verifier == 0:

                    json_file = open(f"proof.json")
                    json_data = json.load(json_file)


                    if json_data["inputs"] == g.hash[f"{username}"]:

                        g.winner = [username,addr]
                        for other in g.players:
                            if other != username:
                                for name,address in clients.items():
                                    if name == other:
                                        server_socket.sendto(f"Player {username} has claimed victory!".encode(),address)
                                        g.last_play = [addr,"victory"]
                                        

                        
                        return


                server_socket.sendto("Failed Proof".encode(),addr)
                server_socket.sendto("Try again:".encode(),addr)

                return
                    
                
    server_socket.sendto("Player not in a game".encode(),addr)
    server_socket.sendto("Try again:".encode(),addr)
    return
                
def Objection(addr):               
    for name,address in clients.items():
        if address == addr:
            username = name

   
    for g in games:
        for player in g.players:
            if player == username:
                                
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


                    if json_data["inputs"] == g.hash[f"{username}"]:

                        
                        if g.last_play[1] == "victory":
                            server_socket.sendto(f"Player {username} has objected!".encode(),g.last_play[0])
                            server_socket.sendto("Objection Successful!".encode(),addr)
                            server_socket.sendto("Your Turn!".encode(),addr)
                            g.last_play = [addr,"objected"]
                            g.last_player = g.current_player
                            g.current_player = addr
                        else:
                            server_socket.sendto("Victory has not been claimed or already objected".encode(),addr)
                                        
                        
                        return


                server_socket.sendto("Failed Proof".encode(),addr)
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
                os.chdir("proof1")
                Create(aux[1],addr,aux[2])
            else:
                server_socket.sendto("Comando Inválido!".encode(),addr)

        if aux[0].lower() == "join":
            if len(aux) == 3:
                os.chdir("proof1")
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

        if aux[0].lower() == "wave":
            if len(aux) == 1:
                Wave(addr)
            
        if aux[0].lower() == "claim":
            if len(aux) == 1:
                os.chdir("proof3")
                Victory(addr)
        
        if aux[0].lower() == "objection":
            if len(aux) == 1:
                os.chdir("proof3")
                Objection(addr)

        if aux[0].lower() == "start":
            if len(aux) == 1:
                Start(addr)

if __name__ == '__main__':
    start_server()