def read_pem(input_data):
    """Read PEM formatted input."""
    data = []
    state = 0
    for line in input_data:
        if state == 0:
            if line.startswith('-----BEGIN'):
                state = 1
        elif state == 1:
            if line.startswith('-----END'):
                state = 2
            else:
                data.append(line)
        elif state == 2:
            break
    if state != 2:
        raise ValueError('No PEM encoded input found')
    data = ''.join(data)
    from ubinascii import a2b_base64
    data = a2b_base64(data)
    return data

def strid(id):
    """Return a string representation of a ASN.1 id."""
    from uasn1 import Boolean, Integer, OctetString, Null, BitString, ObjectIdentifier, Enumerated, Sequence, Set, Null
    if id == Boolean:
        s = 'BOOLEAN'
    elif id == Integer:
        s = 'INTEGER'
    elif id == OctetString:
        s = 'OCTET STRING'
    elif id == Null:
        s = 'NULL'
    elif id == BitString:
        s = 'BIT STRING'
    elif id == ObjectIdentifier:
        s = 'OBJECT IDENTIFIER'
    elif id == Enumerated:
        s = 'ENUMERATED'
    elif id == Sequence:
        s = 'SEQUENCE'
    elif id == Set:
        s = 'SET'
    elif id == Null:
        s = 'NULL'
    else:
        s = '%#02x' % id
    return s
 
def strclass(id):
    """Return a string representation of an ASN.1 class."""
    from uasn1 import ClassUniversal, ClassApplication, BitString, ClassContext, ClassPrivate
    if id == ClassUniversal:
        s = 'UNIVERSAL'
    elif id == ClassApplication:
        s = 'APPLICATION'
    elif id == BitString:
        s = 'BIT STRING'
    elif id == ClassContext:
        s = 'CONTEXT'
    elif id == ClassPrivate:
        s = 'PRIVATE'
    else:
        raise ValueError('Illegal class: %#02x' % id)
    return s

def strtag(tag):
    """Return a string represenation of an ASN.1 tag."""
    return '[%s] %s' % (strid(tag[0]), strclass(tag[2]))

def prettyprint(input_data, output, indent=0):
    """Pretty print ASN.1 data."""
    from uasn1 import TypePrimitive, TypeConstructed
    while not input_data.eof():
        tag = input_data.peek()
        # print(output.getvalue())
        if tag[1] == TypePrimitive:
            tag, value = input_data.read()
            output.write(' ' * indent)
            output.write('[%s] %s (value %s)' %
                         (strclass(tag[2]), strid(tag[0]), repr(value)))
            output.write('\n')
        elif tag[1] == TypeConstructed:
            output.write(' ' * indent)
            output.write('[%s] %s:\n' % (strclass(tag[2]), strid(tag[0])))
            input_data.enter()
            prettyprint(input_data, output, indent+2)
            input_data.leave()
            
def get_pem_parameters(pem, type: str):
    formatted_pem = format_pem(pem, type)
    input_data = read_pem(formatted_pem)
    data = []
    for line in input_data:
        data.append(line)
    if isinstance(data[0], str):
        data = b''.join(data)
    elif isinstance(data[0], int):
        data = bytes(data)
    else:
        print('invalid data')

    from uasn1 import Decoder
    dec = Decoder()
    dec.start(data)

    from io import StringIO
    s = StringIO()
    prettyprint(dec, s)
    # print(s.getvalue())
    values = s.getvalue().split('\n')[2:7] # get the indexes [2 -> 6]
    # print(values)
    result = []
    # text = []
    for i in values:
        i = i.replace('  [UNIVERSAL] INTEGER (value ', '')
        i = i.replace(')', '')
        # print(i)
        result.append(int(i))
        # text.append(str(i))
    return result #, text

def get_pem_key(pkcs8, type: str):
    # print('formatted_pkcs8')
    formatted_pkcs8 = format_pem(pkcs8, type)
    # print(formatted_pkcs8)

    # print('input_data')
    input_data = read_pem(formatted_pkcs8)
    # print(input_data)

    data = []
    for line in input_data:
        data.append(line)
        
    if isinstance(data[0], str):
        data = b''.join(data)
    elif isinstance(data[0], int):
        data = bytes(data)
    else:
        print('invalid data')

    # print('data')
    # print(data)

    from uasn1 import Decoder
    dec = Decoder()
    dec.start(data)

    from io import StringIO
    s = StringIO()
    prettyprint(dec, s)
    # print(s.getvalue())
    value = s.getvalue().split('\n')[5] # get the indexes [2 -> 6]
    value = value.replace('  [UNIVERSAL] OCTET STRING (value ', '')
    value = value.replace(')', '')
    # print(value)
    return value

# type == "public" or "private"
def format_pem(pem, type: str):
    pem_list = []
    for i in range(0, len(pem), 64):
        pem_list.append(pem[i:i+64])
    pem_list.insert(0, "-----BEGIN RSA %s KEY-----" %type.upper())
    pem_list.append("-----END RSA %s KEY-----" %type.upper())
    
    return pem_list

def get_public_n_e(publicRsaKeyDecrypted: str):
    """
    get the n and e value of a public rsa key (decrypted, base 64, pkcs1 e.g.: 'MIIBIjANBgkqhkiG9w0BAQE...')

    Example:

    sk = '***' # selfEncryptionKey
    encryptedEncryptPublicKey = '***' # aesEncryptPublicKey

    from lib import aes
    from lib.pem_service import get_public_n_e

    n, e = get_public_n_e(aes.aes_decrypt(encryptedEncryptPublicKey, sk))
    print(n, e) # e.g. : '17722134712468768015452030444478829164426015687915321737937997713634046043898347302696251047824063488994... 65537'

    """
    formatted_pem = format_pem(publicRsaKeyDecrypted, "public")
    input_data = read_pem(formatted_pem)

    from uasn1 import Decoder
    dec = Decoder()
    dec.start(input_data)

    from io import StringIO
    s = StringIO()

    prettyprint(dec, s)

    # print(s.getvalue())

    incorrect_ascii = s.getvalue().split('\n')[4].replace('  [UNIVERSAL] BIT STRING (value \'', '').replace('\')', '') 
    # print('incorrect_ascii %s' %incorrect_ascii)
    from ubinascii import hexlify, a2b_base64, unhexlify
    hex_str = hexlify(a2b_base64(incorrect_ascii), ' ').decode() # '00 30 82...'
    # print('hex_str %s' %hex_str)
    correct_hex_str = hex_str[3:]
    # print('hex_str removed %s' %correct_hex_str)
    # convert back to ascii
    correct_ascii = unhexlify(correct_hex_str.replace(' ', ''))
    # print(correct_ascii)
    del hexlify, a2b_base64, unhexlify

    input_data = correct_ascii
    dec = Decoder()
    dec.start(input_data)
    del Decoder

    s = StringIO()
    del StringIO
    prettyprint(dec, s) 
    # print(s.getvalue())

    n_e_array = s.getvalue().split('\n')[1:3]
    # print('n_e_array %s' %n_e_array)
    numbers = []
    for value in n_e_array:
        value = value.replace('  [UNIVERSAL] INTEGER (value ', '').replace(')', '')
        # print(value)
        numbers.append(int(value))
    
    # print('n: %s' %numbers[0])
    # print('e: %s' %numbers[1])
    return numbers[0], numbers[1]

def b42_urlsafe_encode(payload):
    from lib.third_party import string
    from ubinascii import b2a_base64
    return string.translate(b2a_base64(payload)[:-1].decode('utf-8'),{ ord('+'):'-', ord('/'):'_' })