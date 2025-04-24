from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from os import urandom

# N-TEA Functions
def ntea_encrypt_block(data, key, num_rounds=32):
    v0, v1 = int.from_bytes(data[:4], 'little'), int.from_bytes(data[4:], 'little')
    k = [int.from_bytes(key[i:i + 4], 'little') for i in range(0, 16, 4)]
    delta = 0x9E3779B9
    sum = 0
    for _ in range(num_rounds):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
    return v0.to_bytes(4, 'little') + v1.to_bytes(4, 'little')

def ntea_decrypt_block(data, key, num_rounds=32):
    v0, v1 = int.from_bytes(data[:4], 'little'), int.from_bytes(data[4:], 'little')
    k = [int.from_bytes(key[i:i + 4], 'little') for i in range(0, 16, 4)]
    delta = 0x9E3779B9
    sum = (delta * num_rounds) & 0xFFFFFFFF
    for _ in range(num_rounds):
        v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        sum = (sum - delta) & 0xFFFFFFFF
    return v0.to_bytes(4, 'little') + v1.to_bytes(4, 'little')

def ntea_encrypt(plaintext, key):
    if len(key) != 16:
        raise ValueError("Key must be exactly 16 characters long")
    padding_length = (8 - (len(plaintext) % 8)) % 8
    plaintext += b'\x00' * padding_length
    ciphertext = b""
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i + 8]
        ciphertext += ntea_encrypt_block(block, key)
    return ciphertext, padding_length

def ntea_decrypt(ciphertext, key, padding_length):
    if len(key) != 16:
        raise ValueError("Key must be exactly 16 characters long")
    plaintext = b""
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i + 8]
        plaintext += ntea_decrypt_block(block, key)
    return plaintext[:-padding_length] if padding_length else plaintext

# AES Functions
def aes_encrypt(plaintext, key):
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return plaintext

# Dual Encryption
def dual_encrypt(plaintext, ntea_key, aes_key):
    intermediate_ciphertext, padding_length = ntea_encrypt(plaintext, ntea_key)
    final_ciphertext = aes_encrypt(intermediate_ciphertext, aes_key)
    return final_ciphertext, padding_length

def dual_decrypt(ciphertext, ntea_key, aes_key, padding_length):
    intermediate_ciphertext = aes_decrypt(ciphertext, aes_key)
    plaintext = ntea_decrypt(intermediate_ciphertext, ntea_key, padding_length)
    return plaintext
