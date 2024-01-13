import binascii
import ucryptolib

def aes_decrypt(encryptedText, selfEncryptionKey):
    ciphertext = binascii.a2b_base64(encryptedText)
    key = binascii.a2b_base64(selfEncryptionKey)
    iv = hex_str_to_bytes("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
    aes = ucryptolib.aes(key, 6, iv)
    decrypted = aes.decrypt(bytearray(ciphertext))
    return decrypted.decode('utf-8').rstrip("\x10") # .decode('utf-8')

def hex_str_to_bytes(hex_str):
    parts = hex_str.split(' ')
    together = "".join(parts)
    return bytes.fromhex(together)
