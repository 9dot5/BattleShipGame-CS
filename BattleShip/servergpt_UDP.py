import socket
import threading
import hashlib
import hmac

SECRET_KEY = b'secret'
clients = {}

def sign_message(message):
    return hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()

def verify_message(message, signature):
    expected_signature = hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def handle_client(addr, message):
    if addr not in clients:
        clients[addr] = addr
        print(f'New client joined: {addr}')
    print(f'Received from {addr}: {message}')

def send_message_to_client(addr, message):
    if addr in clients:
        message_signature = sign_message(message)
        server_socket.sendto(f"{message}|{message_signature}".encode(), addr)
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
        addr_str = addr_str.strip('() ')
        host, port = addr_str.split(',')
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
    print(f'Server started at {host}:{port}')

    threading.Thread(target=server_input_handler, daemon=True).start()

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            message, signature = data.decode().rsplit('|', 1)
            if verify_message(message, signature):
                handle_client(addr, message)
            else:
                print("Invalid message signature from", addr)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    start_server()
