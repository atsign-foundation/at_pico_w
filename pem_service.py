import io
import sys
import ubinascii
import uasn1

def read_pem(input_data):
    """Read PEM formatted input."""
    data = []
    state = 0
    for line in input_data:
        # print(line)
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
    data = ubinascii.a2b_base64(data)
    return data

def strid(id):
    """Return a string representation of a ASN.1 id."""
    if id == uasn1.Boolean:
        s = 'BOOLEAN'
    elif id == uasn1.Integer:
        s = 'INTEGER'
    elif id == uasn1.BitString:
        s = 'BIT STRING'
    elif id == uasn1.OctetString:
        s = 'OCTET STRING'
    elif id == uasn1.Null:
        s = 'NULL'
    elif id == uasn1.ObjectIdentifier:
        s = 'OBJECT IDENTIFIER'
    elif id == uasn1.Enumerated:
        s = 'ENUMERATED'
    elif id == uasn1.Sequence:
        s = 'SEQUENCE'
    elif id == uasn1.Set:
        s = 'SET'
    else:
        s = '%#02x' % id
    return s

def strclass(id):
    """Return a string representation of an ASN.1 class."""
    if id == uasn1.ClassUniversal:
        s = 'UNIVERSAL'
    elif id == uasn1.ClassApplication:
        s = 'APPLICATION'
    elif id == uasn1.ClassContext:
        s = 'CONTEXT'
    elif id == uasn1.ClassPrivate:
        s = 'PRIVATE'
    else:
        raise ValueError('Illegal class: %#02x' % id)
    return s

def strtag(tag):
    """Return a string represenation of an ASN.1 tag."""
    return '[%s] %s' % (strid(tag[0]), strclass(tag[2]))

def prettyprint(input_data, output, indent=0):
    """Pretty print ASN.1 data."""
    while not input_data.eof():
        tag = input_data.peek()
        if tag[1] == uasn1.TypePrimitive:
            tag, value = input_data.read()
            output.write(' ' * indent)
            output.write('[%s] %s (value %s)' %
                         (strclass(tag[2]), strid(tag[0]), repr(value)))
            output.write('\n')
        elif tag[1] == uasn1.TypeConstructed:
            output.write(' ' * indent)
            output.write('[%s] %s:\n' % (strclass(tag[2]), strid(tag[0])))
            input_data.enter()
            prettyprint(input_data, output, indent+2)
            input_data.leave()
            
def get_pem_parameters(pem):
    formatted_pem = format_pem(pem)
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

    dec = uasn1.Decoder()
    dec.start(data)

    s = io.StringIO()
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

def get_pub_parameters(pkcs1):
    formatted_pkcs1 = format_pub(pkcs1)
    input_data = read_pem(formatted_pkcs1)
    data = []
    for line in input_data:
        data.append(line)
    if isinstance(data[0], str):
        data = b''.join(data)
    elif isinstance(data[0], int):
        data = bytes(data)
    else:
        print('invalid data')

    dec = uasn1.Decoder()
    dec.start(data)

    s = io.StringIO()
    prettyprint(dec, s)
    #print(s.getvalue())
    value = s.getvalue().split('\n')[4] # bit string encoding integers
    value = value.replace('  [UNIVERSAL] BIT STRING (value ', '')
    value = value.replace(')', '')
    # remove spurious null byte at start of sequence from bit string
    trunc = ubinascii.a2b_base64(value)[1:271]
    dec.start(trunc)
    ss = io.StringIO()
    prettyprint(dec, ss)
    #print(ss.getvalue())
    values = ss.getvalue().split('\n')[1:3] # rsa integer and exponent
    #print(values)
    result = []
    for i in values:
        i = i.replace('  [UNIVERSAL] INTEGER (value ', '')
        i = i.replace(')', '')
        result.append(int(i))
    return result

def get_pem_key(pkcs8):
    formatted_pkcs8 = format_pem(pkcs8)
    input_data = read_pem(formatted_pkcs8)
    data = []
    for line in input_data:
        data.append(line)
    if isinstance(data[0], str):
        data = b''.join(data)
    elif isinstance(data[0], int):
        data = bytes(data)
    else:
        print('invalid data')

    dec = uasn1.Decoder()
    dec.start(data)

    s = io.StringIO()
    prettyprint(dec, s)
    # print(s.getvalue())
    value = s.getvalue().split('\n')[5] # octet string encoding integers
    value = value.replace('  [UNIVERSAL] OCTET STRING (value ', '')
    value = value.replace(')', '')
    # print(value)
    return value

def format_pem(pem):
    pem_list = []
    for i in range(0, len(pem), 64):
        pem_list.append(pem[i:i+64])
    pem_list.insert(0, "-----BEGIN RSA PRIVATE KEY-----")
    pem_list.append("-----END RSA PRIVATE KEY-----")
    
    return pem_list

def format_pub(pub):
    pub_list = []
    for i in range(0, len(pub), 64):
        pub_list.append(pub[i:i+64])
    pub_list.insert(0, "-----BEGIN RSA PUBLIC KEY-----")
    pub_list.append("-----END RSA PUBLIC KEY-----")
    
    return pub_list
