from socket import *
import sys
import time
import random
import os

nonce = random.randint(0,255)

def Generate_Board():

    board = [[0 for _ in range(10)] for _ in range(10)] 

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
        if invalid_move == 0:
            counter = counter + 1

    return carrier,battleship,destroyer,cruiser1,cruiser2,sub1,sub2

def main():
    host = '127.0.0.1'
    port = 65432

    s = socket(AF_INET, SOCK_DGRAM)
    server_address = (host, port)
    print("Joined the communication.")
    while True:
        
        command = input("Enter your reply: ")  # Get reply from the user
        s.sendto(command.encode(), server_address)  # Send the reply back to the server

        if command.split()[0] == "create":
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
            os.system(f"zokrates compute-witness -a {witness}")
            os.system("zokrates generate-proof")

            s.sendto("Proof 1".encode(),server_address)

            proof = open("1/proof.json")

            
            
            





        data, _ = s.recvfrom(1024)  # Receive message from the server
        print("Server:", data.decode())
        aux = data.decode().split( )

        

if __name__ == '__main__':
    main()