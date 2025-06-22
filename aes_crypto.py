from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

# Panjang blok AES
BLOCK_SIZE = 16
# Salt acak untuk turunan kunci
SALT = b'steganografi_salt'

# Padding (agar panjang teks kelipatan 16)
def pad(text):
    pad_len = BLOCK_SIZE - len(text) % BLOCK_SIZE
    return text + bytes([pad_len] * pad_len)

def unpad(text):
    pad_len = text[-1]
    return text[:-pad_len]

# Fungsi enkripsi teks menjadi bytes terenkripsi (AES)
def encrypt_image(plaintext_bytes, password):
    key = PBKDF2(password, SALT, dkLen=32)  # 256-bit key
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext_bytes)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext  # simpan IV di depan

# Fungsi dekripsi bytes menjadi teks
def decrypt_image(encrypted_data, password):
    key = PBKDF2(password, SALT, dkLen=32)
    iv = encrypted_data[:BLOCK_SIZE]
    ciphertext = encrypted_data[BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ciphertext)
    return unpad(padded)