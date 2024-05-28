import random
import hashlib

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
        linha = input("linha:")
        while int(linha) > 10 or int(linha) < 1:
            print("posicao invalida\n")
            linha = input("linha:")
            continue
        coluna = input("coluna:")
        while int(coluna) > 10 or int(coluna) < 1:
            print("posicao invalida\n")
            coluna = input("coluna:")
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
            direcao = 3
        if orientacao == 'l':
            direcao = 4
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
        counter += 1

# Combine all positions into a single fleet dictionary
fleet = {
    'carrier': carrier,
    'battleship': battleship,
    'destroyer': destroyer,
    'cruiser1': cruiser1,
    'cruiser2': cruiser2,
    'sub1': sub1,
    'sub2': sub2
}

# Commit the fleet positions
nonce = random.randint(0, int(1e9))
fleet_str = str(fleet) + str(nonce)
positions_hash = hashlib.sha256(fleet_str.encode()).hexdigest()
print(f"Fleet committed with nonce {nonce} and hash {positions_hash}")

# Save the fleet positions to use them in zkproof.py
with open("fleet_positions.txt", "w") as file:
    file.write(str(fleet))
    file.write("\n")
    file.write(str(nonce))
