from cryptography.fernet import Fernet
import hashlib

# Generate a key and save it securely; only load it when you need to encrypt/decrypt
key = Fernet.generate_key()

def encrypt_field(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_field(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()