
def without_prefix(atSign: str):
    if atSign.startswith('@'):
        return atSign[1:]
    return atSign

def format_atSign(atSign: str):
    if not atSign.startswith('@'):
        return '@' + atSign
    return atSign

def str_to_bytes(s: str) -> bytes:
    import ubinascii
    return ubinascii.a2b_base64(s)

def str_to_bytearray(s: str) -> bytearray:
    return bytearray(str_to_bytes(s))

def bytearray_to_str(b: bytearray) -> str:
    return str(b)

def bytes_to_str(b: bytes) -> str:
    import ubinascii
    return str(ubinascii.b2a_base64(b))