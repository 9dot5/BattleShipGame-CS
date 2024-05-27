'''import socket
import threading

clients = {}

def handle_client(addr, message):
    if addr not in clients:
        clients[addr] = addr
        print(f'New client joined: {addr}')
    print(f'Received from {addr}: {message}')

def send_message_to_client(addr, message):
    if addr in clients:
        server_socket.sendto(message.encode(), addr)
    else:
        print(f'No client with address {addr} connected.')

def list_clients():
    if clients:
        print("Connected clients:")
        for addr in clients.keys():
            print(addr)
    else:
        print("No clients connected.")

def parse_address(addr_str):
    try:
        # Remove parentheses and spaces
        addr_str = addr_str.strip('() ')
        # Split the string by comma
        host, port = addr_str.split(',')
        # Remove extra spaces and quotes
        host = host.strip().strip('\'"')
        port = port.strip()
        return (host, int(port))
    except Exception as e:
        print(f"Invalid address format: {e}")
        return None

def server_input_handler():
    while True:
        try:
            command = input('Enter command (list | send <addr> <message>): ')
            if command.startswith('list'):
                list_clients()
            elif command.startswith('send'):
                parts = command.split(' ')
                if len(parts) >= 4:
                    addr_str = ' '.join(parts[1:3])
                    message = ' '.join(parts[3:])
                    addr = parse_address(addr_str)
                    if addr:
                        send_message_to_client(addr, message)
                else:
                    print("Invalid send command format. Use 'send <addr> <message>'.")
            else:
                print("Invalid command. Use 'list' or 'send <addr> <message>'.")
        except Exception as e:
            print(f'Error: {e}')

def start_server(host='127.0.0.1', port=65432):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f'Server listening on {host}:{port}')
    
    threading.Thread(target=server_input_handler, daemon=True).start()

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        client_thread = threading.Thread(target=handle_client, args=(addr, message))
        client_thread.start()

if __name__ == '__main__':
    start_server()'''

import socket
import threading

clients = {}

def handle_client(addr, message):
    if addr not in clients:
        username = message.split()[1]  # Assume the join message is "join <username>"
        clients[addr] = username
        print(f'New client joined: {username} ({addr})')
    else:
        print(f'Received from {clients[addr]}: {message}')

def send_message_to_client(username, message):
    addr = None
    for client_addr, client_username in clients.items():
        if client_username == username:
            addr = client_addr
            break
    if addr:
        server_socket.sendto(message.encode(), addr)
    else:
        print(f'No client with username {username} connected.')

def list_clients():
    if clients:
        print("Connected clients:")
        for addr, username in clients.items():
            print(f'{username} ({addr})')
    else:
        print("No clients connected.")

def server_input_handler():
    while True:
        try:
            command = input('Enter command (list | send <username> <message>): ')
            if command.startswith('list'):
                list_clients()
            elif command.startswith('send'):
                parts = command.split(' ', 2)
                if len(parts) >= 3:
                    username = parts[1]
                    message = parts[2]
                    send_message_to_client(username, message)
                else:
                    print("Invalid send command format. Use 'send <username> <message>'.")
            else:
                print("Invalid command. Use 'list' or 'send <username> <message>'.")
        except Exception as e:
            print(f'Error: {e}')
            
def start_server(host='127.0.0.1', port=65432):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f'Server listening on {host}:{port}')
    
    threading.Thread(target=server_input_handler, daemon=True).start()

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        client_thread = threading.Thread(target=handle_client, args=(addr, message))
        client_thread.start()

if __name__ == '__main__':
    start_server()
