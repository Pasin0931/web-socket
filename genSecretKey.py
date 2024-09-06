from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Print the key
print(f"Encryption Key: {key.decode()}")

# Optionally, save the key to a file or secure storage
with open("secret.key", "wb") as key_file:
    key_file.write(key) # write file