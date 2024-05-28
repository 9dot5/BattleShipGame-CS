import socket
import hashlib
import hmac

SECRET_KEY = b'secret'

def sign_message(message):
    return hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()

def verify_message(message, signature):
    expected_signature = hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def main():
    host = '127.0.0.1'
    port = 65432

    join_input = input("Type 'join <username>' to join the server: ")
    if join_input.lower().startswith('join '):
        username = join_input.split()[1]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            server_address = (host, port)
            join_message = f"join {username}"
            join_signature = sign_message(join_message)
            s.sendto(f"{join_message}|{join_signature}".encode(), server_address)
            print("Joined the communication.")
            handle_communication(s, server_address)

def handle_communication(socket, server_address):
    while True:
        try:
            data, _ = socket.recvfrom(1024)
            message, signature = data.decode().rsplit('|', 1)
            if verify_message(message, signature):
                print("Server:", message)
                reply = input("Enter your reply: ")
                reply_signature = sign_message(reply)
                socket.sendto(f"{reply}|{reply_signature}".encode(), server_address)
            else:
                print("Invalid message signature.")
        except Exception as e:
            print(f"Communication error: {e}")
            break

if __name__ == '__main__':
    main()
