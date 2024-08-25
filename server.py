from binance import Client
import socket
from cryptography.fernet import Fernet

# Load the key and create the cipher suite
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

# Create a standard socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 1234))
server.listen(5)

client = Client()


def search_crypto_price(symbol):
    prices = client.get_all_tickers()
    for price in prices:
        if price['symbol'] == symbol.upper():
            return f"{price['symbol']}: {float(price['price']):.2f}"
    return "Cryptocurrency pair not found!"

while True:
    # accept connection
    clientsocket, address = server.accept()
    print(f"Connection from {address} has been established!")

    while True:
        try:
            message = clientsocket.recv(1024)
            print(f"Received message: {message}")
            decrypted_message = cipher_suite.decrypt(message).decode("utf-8")
            if not decrypted_message or decrypted_message in ["2", "2."]:
                print(f"Exited by client {address}")
                break

            response = search_crypto_price(decrypted_message)
            clientsocket.send(cipher_suite.encrypt(response.encode("utf-8")))
        except Exception as e:
            print(f"Error: {e}")
            break

    clientsocket.close()