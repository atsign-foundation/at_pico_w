

def main():

    sk = '***' # selfEncryptionKey
    encryptedEncryptPublicKey = '***' # aesEncryptPublicKey

    from lib import aes
    from lib.pem_service import get_public_n_e

    n, e = get_public_n_e(aes.aes_decrypt(encryptedEncryptPublicKey, sk))
    print(n, e)


if __name__ == '__main__':
    main()