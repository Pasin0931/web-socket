import socket
from cryptography.fernet import Fernet

# Load the key and create the cipher suite
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((socket.gethostname(), 1234))

try:
    while True:
        choice = input("Choose an option:\n1. Trade Cryptocurrency\n2. Exit\n")
        if choice in ["2", "2."]:
            encrypted_choice = cipher_suite.encrypt(choice.encode("utf-8"))
            server.send(encrypted_choice)
            server.close()
            break
        elif choice in ["1", "1."]:
            crypto_pair = input("Enter cryptocurrency pair (e.g., BTCUSDT): ")
            encrypted_pair = cipher_suite.encrypt(crypto_pair.encode("utf-8"))
            server.send(encrypted_pair)

            encrypted_price = server.recv(1024)
            response = cipher_suite.decrypt(encrypted_price).decode("utf-8")
            print(f"[Server] {response}\n")
except KeyboardInterrupt:
    print("\nExited by user")
finally:
    server.close()

