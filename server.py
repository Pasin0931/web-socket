from binance import Client
import socket
from cryptography.fernet import Fernet

# Load the key and create the cipher suite
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

# Create a standard socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket type
server.bind((socket.gethostname(), 1234))                   # Run to server with local name ---> port = 1234
server.listen(5)                                            # Maximun number of clients is 5

client = Client()                                           # Initialize all of binance object to client var


def search_crypto_price(symbol):
    prices = client.get_all_tickers()                       # Get all pair prices
    for price in prices:
        if price['symbol'] == symbol.upper():               # Check symbol for prices
            return f"{price['symbol']}: {float(price['price']):.2f}"         
    return "Cryptocurrency pair not found!"

while True:
    # accept connection
    clientsocket, address = server.accept()
    print(f"Connection from {address} has been established!")

    while True:
        try:
            message = clientsocket.recv(1024)                                    # Recieve data from client
            print(f"Received message: {message}")            
            decrypted_message = cipher_suite.decrypt(message).decode("utf-8")    # Decrypt data from client
            if not decrypted_message or decrypted_message in ["2", "2."]:
                print(f"Exited by client {address}")
                break

            response = search_crypto_price(decrypted_message)                     # Send dectypted message to search price
            clientsocket.send(cipher_suite.encrypt(response.encode("utf-8")))     # Send encrypt data to client
        except Exception as e:
            print(f"Error: {e}")
            break

    clientsocket.close()