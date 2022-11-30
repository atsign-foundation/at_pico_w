def aes_decrypt(encryptedText: str, aes256Base64Key: str) -> str:
    from ubinascii import a2b_base64
    key = a2b_base64(aes256Base64Key)
    iv = hex_str_to_bytes("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
    from ucryptolib import aes as uaes
    aes = uaes(key, 6, iv)
    del uaes
    decrypted = aes.decrypt(bytearray(a2b_base64(encryptedText)))
    del a2b_base64
    return decrypted.decode('utf-8').rstrip("\x10")

def aes_encrypt(plain_text: str, aes256Base64Key: str) -> str:
    from ubinascii import a2b_base64
    key = a2b_base64(aes256Base64Key)
    iv = hex_str_to_bytes("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
    from ucryptolib import aes as uaes
    aes = uaes(key, 6, iv)
    del uaes
    encrypted = aes.encrypt(bytearray(a2b_base64(plain_text)))
    del a2b_base64
    return encrypted.decode('utf-8').rstrip("\x10")

def hex_str_to_bytes(hex_str):
    parts = hex_str.split(' ')
    together = "".join(parts)
    return bytes.fromhex(together)
    
def str_to_bytes(s: str) -> bytes:
    from ubinascii import a2b_base64
    return a2b_base64(s)

def str_to_bytearray(s: str) -> bytearray:
    return bytearray(str_to_bytes(s))

def bytearray_to_str(b: bytearray) -> str:
    return str(b)

def bytes_to_str(b: bytes) -> str:
    from ubinascii import b2a_base64
    return str(b2a_base64(b))