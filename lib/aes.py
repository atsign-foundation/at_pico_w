import ubinascii
import ucryptolib

def aes_decrypt(encryptedText: str, aes256Base64Key: str) -> str:
    key = ubinascii.a2b_base64(aes256Base64Key)
    iv = hex_str_to_bytes("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
    aes = ucryptolib.aes(key, 6, iv)
    decrypted = aes.decrypt(bytearray(ubinascii.a2b_base64(encryptedText)))
    return decrypted.decode('utf-8').rstrip("\x10")

def aes_encrypt(plain_text: str, aes256Base64Key: str) -> str:
    key = ubinascii.a2b_base64(aes256Base64Key)
    iv = hex_str_to_bytes("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
    aes = ucryptolib.aes(key, 6, iv)
    encrypted = aes.encrypt(bytearray(ubinascii.a2b_base64(plain_text)))
    return encrypted.decode('utf-8').rstrip("\x10")

def hex_str_to_bytes(hex_str):
    parts = hex_str.split(' ')
    together = "".join(parts)
    return bytes.fromhex(together)
    
def str_to_bytes(s: str) -> bytes:
    return ubinascii.a2b_base64(s)

def str_to_bytearray(s: str) -> bytearray:
    return bytearray(str_to_bytes(s))

def bytearray_to_str(b: bytearray) -> str:
    return str(b)

def bytes_to_str(b: bytes) -> str:
    return str(ubinascii.b2a_base64(b))