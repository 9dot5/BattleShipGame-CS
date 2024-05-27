'''import socket

def main():
    host = '127.0.0.1'
    port = 65432

    join_input = input("Type 'join' to join the server: ")
    if join_input.lower().strip() == 'join':
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            server_address = (host, port)
            s.sendto("join".encode(), server_address)
            print("Joined the communication.")
            while True:
                data, _ = s.recvfrom(1024)  # Receive message from the server
                print("Server:", data.decode())
                reply = input("Enter your reply: ")  # Get reply from the user
                s.sendto(reply.encode(), server_address)  # Send the reply back to the server

if __name__ == '__main__':
    main()'''

import socket

def main():
    host = '127.0.0.1'
    port = 65432

    join_input = input("Type 'join <username>' to join the server: ")
    if join_input.lower().startswith('join '):
        username = join_input.split()[1]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            server_address = (host, port)
            join_message = f"join {username}"
            s.sendto(join_message.encode(), server_address)
            print("Joined the communication.")
            while True:
                data, _ = s.recvfrom(1024)  # Receive message from the server
                print("Server:", data.decode())
                reply = input("Enter your reply: ")  # Get reply from the user
                s.sendto(reply.encode(), server_address)  # Send the reply back to the server

if __name__ == '__main__':
    main()

