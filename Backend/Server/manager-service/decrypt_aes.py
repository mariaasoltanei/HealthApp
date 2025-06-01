import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


with open("/app/aes-key", "rb") as f:
    base64_key = f.read().strip()

AES_KEY = base64.b64decode(base64_key)

def decrypt_value(encrypted_b64, iv_b64):
    encrypted = base64.b64decode(encrypted_b64)
    iv = base64.b64decode(iv_b64)
    aesgcm = AESGCM(AES_KEY)
    decrypted_bytes = aesgcm.decrypt(iv, encrypted, None)
    return float(decrypted_bytes.decode("utf-8"))