
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import io
from PIL import Image
import hashlib

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_image(image: Image.Image, password: str):
    key = hashlib.sha256(password.encode()).digest()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    buf = io.BytesIO()
    image.save(buf, format='PNG')
    plaintext = pad(buf.getvalue())
    ciphertext = cipher.encrypt(plaintext)
    return iv + ciphertext

def decrypt_image(data: bytes, password: str):
    key = hashlib.sha256(password.encode()).digest()
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext))
    return Image.open(io.BytesIO(decrypted))
