from socket import *
import sys
import time
import random
import os

nonce = random.randint(0,255)
board = [[0 for _ in range(10)] for _ in range(10)] 

def Generate_Board():

    

    counter = 0

    carrier = []
    battleship = []
    destroyer = []
    cruiser1 = []
    cruiser2 = []
    sub1 = []
    sub2 = []

    for x in [5, 4, 3, 2, 2, 1, 1]:

        invalid_move = 1

        while invalid_move:
            invalid_move = 0

            if x == 5:
                print("Carrier position:")
            if x == 4:
                print("Battleship position:")
            if x == 3:
                print("Destroyer position:")
            if x == 2:
                if counter == 3:
                    print("First cruiser position:")
                if counter == 4:
                    print("Second cruiser position:")
            if x == 1:
                if counter == 5:
                    print("First submarine position:")
                if counter == 6:
                    print("Second submarine position:")
            linha= input("linha:")
            
            while int(linha) > 10 or int(linha) < 1:
                print("posicao invalida\n")
                linha= input("linha:")
                continue

            coluna= input("coluna:")

            while int(coluna) > 10 or int(coluna) < 1:
                print("posicao invalida\n")
                coluna= input("coluna:")
                continue

            linhas = int(linha) - 1
            colunas = int(coluna) - 1



            orientacao = input("orientação (u, d, l, r)")

            
            

            while orientacao not in ['u', 'd', 'l', 'r']:
                print("direcção invalida\n")
                orientacao = input("orientação (u, d, l, r)")
                continue
            
            if orientacao == 'u':
                direcao = 1
            if orientacao == 'r':
                direcao = 2
            if orientacao == 'd':
                direcao == 3
            if orientacao == 'l':
                direcao == 4

                
            if x == 5:
                carrier.append(linhas)
                carrier.append(colunas)
                carrier.append(direcao)
            if x == 4:
                battleship.append(linhas)
                battleship.append(colunas)
                battleship.append(direcao)
            if x == 3:
                destroyer.append(linhas)
                destroyer.append(colunas)
                destroyer.append(direcao)
            if x == 2:
                if counter == 3:
                    cruiser1.append(linhas)
                    cruiser1.append(colunas)
                    cruiser1.append(direcao)
                if counter == 4:
                    cruiser2.append(linhas)
                    cruiser2.append(colunas)
                    cruiser2.append(direcao)
            if x == 1:
                if counter == 5:
                    sub1.append(linhas)
                    sub1.append(colunas)
                    sub1.append(direcao)
                if counter == 6:
                    sub2.append(linhas)
                    sub2.append(colunas)
                    sub2.append(direcao)
            
            if orientacao == 'u' and int(linhas) < x-1:
                print("posicao invalida\n")
                invalid_move=1
                continue


            if orientacao == 'd' and int(linhas) > 10-x:
                print("posicao invalida\n")
                invalid_move=1
                continue


            if orientacao == 'l' and int(colunas) < x-1:
                print("posicao invalida\n")
                invalid_move=1
                continue


            if orientacao == 'r' and int(colunas) > 10-x:
                print("posicao invalida\n")
                invalid_move=1
                continue
            
            for y in range(x):
                if orientacao == 'u':
                    if board[int(linhas) - y][int(colunas)] == 1:
                        print("posicao invalida\n")
                        invalid_move=1
                        break

                if orientacao == 'd':
                    if board[int(linhas)+ y][int(colunas) ] == 1:
                        print("posicao invalida\n")
                        invalid_move=1
                        break

                if orientacao == 'l':
                    if board[int(linhas)][int(colunas) - y ] == 1:
                        print("posicao invalida\n")
                        invalid_move=1
                        break

                if orientacao == 'r':
                    if board[int(linhas)][int(colunas) + y] == 1:
                        print("posicao invalida\n")
                        invalid_move=1
                        break

        for y in range(x):
            if orientacao == 'u':
                board[int(linhas) - y][int(colunas)] = 1
            if orientacao == 'd':
                board[int(linhas)+ y][int(colunas) ] = 1
            if orientacao == 'l':
                board[int(linhas) ][int(colunas) - y] = 1
            if orientacao == 'r':
                board[int(linhas)][int(colunas) +y ] = 1

        if invalid_move == 0:
            counter = counter + 1

    return carrier,battleship,destroyer,cruiser1,cruiser2,sub1,sub2

def Report(x,y,board):

    if board[y][x] == 1:
        hit = 1
    elif board[y][x] == 0:
        hit = 0

    
    
    return hit





def main():
    host = '127.0.0.1'
    port = 65432
    main_path = os.getcwd()
    command = "0 0 0"

    s = socket(AF_INET, SOCK_DGRAM)
    server_address = (host, port)
    print("Joined the communication.")
    s.sendto("Hello".encode(),server_address)
    valid = 1

    while True:

        os.chdir(main_path)
        if valid == 1:
            data,server_address = s.recvfrom(1024)
            print(data.decode())

        command = input("Enter your reply: ")  # Get reply from the user
        
        

        if command.split()[0].lower() == "create" or command.split()[0].lower() == "join":
            valid = 1
            params = []
            carrier,battleship,destroyer,cruiser1,cruiser2,sub1,sub2 = Generate_Board()
            witness = ""
            params.append(nonce)

            for x in carrier:
                params.append(x)
            for x in battleship:
                params.append(x)
            for x in destroyer:
                params.append(x)
            for x in cruiser1:
                params.append(x)
            for x in cruiser2:
                params.append(x)
            for x in sub1:
                params.append(x)
            for x in sub2:
                params.append(x)

            for x in params:
                witness = witness + f" {x}"

            os.chdir("1")
            os.system("export PATH=$PATH:/home/joaosantos/.zokrates/bin")
            witness = os.system(f"zokrates compute-witness -a {witness}")
            if witness == 0:
                os.system("zokrates generate-proof")

                s.sendto(f"{command}".encode(),server_address)

                proof = open("proof.json",'rb')

                data = proof.read(1024)
                print("sending ...")
                while (data):
                    if(s.sendto(data,server_address)):
                        data = proof.read(1024)

                response,addr = s.recvfrom(1024)
                print(response.decode())
            else:
                print("Witness not generated, did not pass proof!")

            proof.close()
            continue
        
        if command.split()[0].lower() == "list":
            valid = 1
            s.sendto(f"{command}".encode(),server_address)
            response,addr = s.recvfrom(1024)
            print(response.decode())
            continue

        if command.split()[0].lower() == "report":
            os.chdir("2")
            valid = 1
            hit = Report(int(command.split()[1]),int(command.split()[2]),board)

            params = []

            params.append(hit)
            params.append(nonce)

            for i in range(10):
                for j in range(10):
                    params.append(board[i][j])
            params.append(command.split()[1])
            params.append(command.split()[2])

            witness2 = ""

            for x in params:
                witness2 = witness2 + f" {x}"
            
            os.system(f"zokrates compute-witness -a {witness2}")
            os.system("zokrates generate-proof")

            s.sendto(f"{command}".encode(),server_address)

            proof = open("proof.json",'rb')

            data = proof.read(1024)
            print("sending ...")
            while (data):
                if(s.sendto(data,server_address)):
                    data = proof.read(1024)

            response,addr = s.recvfrom(1024)
            print(f"{response.decode()}")

            if response.decode() == "Shot Reported Successfuly":
                board[int(command.split()[2])][int(command.split()[1])] = 0


            proof.close()
            continue

        if command.split()[0].lower() == "shoot":
            os.chdir("3")
            valid = 1
            params = []
            witness3 = ""

            for i in range(10):
                for j in range(10):
                    params.append(board[i][j])
            params.append(nonce)

            for x in params:
                witness3 = witness3 + f" {x}"
            
            os.system(f"zokrates compute-witness -a {witness3}")
            os.system("zokrates generate-proof")

            s.sendto(f"{command}".encode(),server_address)
            proof = open("proof.json",'rb')

            data = proof.read(1024)
            print("sending ...")
            while (data):
                if(s.sendto(data,server_address)):
                    data = proof.read(1024)

            response,addr = s.recvfrom(1024)
            print(response.decode())

            hit_or_miss,addr = s.recvfrom(1024)
            print(hit_or_miss.decode())

            proof.close()
            continue
            
        if command.split()[0].lower() == "wave":
            s.sendto(f"{command}".encode(),server_address)

            response,addr = s.recvfrom(1024)
            print(response.decode())
        
        if command.split()[0].lower() == "claim":
            os.chdir("3")
            valid = 1
            params = []
            witness3 = ""

            for i in range(10):
                for j in range(10):
                    params.append(board[i][j])
            params.append(nonce)

            for x in params:
                witness3 = witness3 + f" {x}"
            
            os.system(f"zokrates compute-witness -a {witness3}")
            os.system("zokrates generate-proof")

            s.sendto(f"{command}".encode(),server_address)
            proof = open("proof.json",'rb')

            data = proof.read(1024)
            print("sending ...")
            while (data):
                if(s.sendto(data,server_address)):
                    data = proof.read(1024)

            response,addr = s.recvfrom(1024)
            print(response.decode())

            proof.close()
            continue

        if command.split()[0].lower() == "objection":
            os.chdir("3")
            valid = 1
            params = []
            witness3 = ""

            for i in range(10):
                for j in range(10):
                    params.append(board[i][j])
            params.append(nonce)

            for x in params:
                witness3 = witness3 + f" {x}"
            
            os.system(f"zokrates compute-witness -a {witness3}")
            os.system("zokrates generate-proof")

            s.sendto(f"{command}".encode(),server_address)
            proof = open("proof.json",'rb')

            data = proof.read(1024)
            print("sending ...")
            while (data):
                if(s.sendto(data,server_address)):
                    data = proof.read(1024)

            response,addr = s.recvfrom(1024)
            print(response.decode())

            proof.close()
            continue

        if command.split()[0].lower() == "start":
            s.sendto(f"{command}".encode(),server_address)

            response,addr = s.recvfrom(1024)
            print(response.decode())


        else:
            print("Invalid Command")
            valid = 0


            
            
            





        

        

if __name__ == '__main__':
    main()