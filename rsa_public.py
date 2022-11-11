from lib.pem_service import *
from lib.aes import *
from lib.at_client.io_util import *


def main():

    atSign = '@fascinatingsnow'

    aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey, aesPkamPublicKey, selfEncryptionKey = read_key(atSign)


    decrypted = aes_decrypt(aesEncryptPrivateKey, selfEncryptionKey)
    # decrypted = aes_decrypt(aesPkamPrivateKey, selfEncryptionKey)
    pem_key = get_pem_key(decrypted, 'PRIVATE')
    pem_parameters = get_pem_parameters(pem_key, 'PRIVATE') # n, e, d, p, q

    # print(str(pem_parameters))
    # pem_key = get_pem_key(decrypted, 'PRIVATE')
    # pem_parameters = get_pem_parameters(pem_key, 'PUBLIC')
    # print(pem_parameters)

    # n, e
    from lib.third_party import rsa
    n = pem_parameters[0]
    e = pem_parameters[1]
    d = pem_parameters[2]
    p = pem_parameters[3]
    q = pem_parameters[4]
    publicRsa = rsa.PublicKey(n, e) # n, e
    privateRsa = rsa.PrivateKey(n, e, d, p, q) # n, e, d, p, q
    crypto = rsa.encrypt(b'test', publicRsa)
    print('Encrypted:')
    print(str(crypto))

    print('Decrypting...')
    decrypto = rsa.decrypt(crypto, privateRsa)
    print('Decrypted:')
    print(str(decrypto))

    

    # private q, e, d, p n
    # public e, n

    
if __name__ == '__main__':
    main()