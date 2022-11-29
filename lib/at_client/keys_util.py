# initializes /keys/@alice/ with RSA keys in their pem form
# e.g. /keys/@alice/aesEncryptPrivateKey_pem.json
def initialize_keys(atSign: str) -> None:

    from lib.at_client.io_util import read_key
    aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey, aesPkamPublicKey, selfEncryptionKey = read_key(atSign)
    del read_key

    from lib.at_client.at_utils import without_prefix
    without_prefix_atSign = without_prefix(atSign)
    del without_prefix
    
    from os import mkdir
    try:
        mkdir('/keys/@%s' % without_prefix_atSign)
    except:
        pass
    del mkdir

    from lib.aes import aes_decrypt
    from lib.pem_service import get_pem_parameters, get_pem_key, get_public_n_e
    aesEncryptPrivateKey_pem_parameters = get_pem_parameters(get_pem_key(aes_decrypt(aesEncryptPrivateKey, selfEncryptionKey), 'private'), 'private')
    with open('/keys/@%s/aesEncryptPrivateKey_pem.json' % without_prefix_atSign, 'w') as w:
        w.write("{\n\"aesEncryptPrivateKey\": [\n" + str(aesEncryptPrivateKey_pem_parameters[0]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[1]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[2]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[3]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[4]) + "\n]\n}")
    del aesEncryptPrivateKey_pem_parameters, aesEncryptPrivateKey
    print('Wrote /keys/@%s/aesEncryptPrivateKey_pem.json' % without_prefix_atSign)

    aesEncryptPublicKey_pem_parameters = get_public_n_e(aes_decrypt(aesEncryptPublicKey, selfEncryptionKey))
    with open('/keys/@%s/aesEncryptPublicKey_pem.json' % without_prefix_atSign, 'w') as w:
        w.write("{\n\"aesEncryptPublicKey\": [\n" + str(aesEncryptPublicKey_pem_parameters[0]) + ",\n" + str(aesEncryptPublicKey_pem_parameters[1]) + "\n]\n}")
    del aesEncryptPublicKey_pem_parameters, aesEncryptPublicKey
    print('Wrote /keys/@%s/aesEncryptPublicKey_pem.json' % without_prefix_atSign)

    aesPkamPrivateKey_pem_parameters = get_pem_parameters(get_pem_key(aes_decrypt(aesPkamPrivateKey, selfEncryptionKey), 'private'), 'private')
    with open('/keys/@%s/aesPkamPrivateKey_pem.json' % without_prefix_atSign, 'w') as w:
        w.write("{\n\"aesPkamPrivateKey\": [\n" + str(aesPkamPrivateKey_pem_parameters[0]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[1]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[2]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[3]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[4]) + "\n]\n}")
    del aesPkamPrivateKey_pem_parameters, aesPkamPrivateKey
    print('Wrote /keys/@%s/aesPkamPrivateKey_pem.json' % without_prefix_atSign)

    aesPkamPublicKey_pem_parameters = get_public_n_e(aes_decrypt(aesPkamPublicKey, selfEncryptionKey))
    with open('/keys/@%s/aesPkamPublicKey_pem.json' % without_prefix_atSign, 'w') as w:
        w.write("{\n\"aesPkamPublicKey\": [\n" + str(aesPkamPublicKey_pem_parameters[0]) + ",\n" + str(aesPkamPublicKey_pem_parameters[1]) + "\n]\n}")
    del aesPkamPublicKey_pem_parameters, aesPkamPublicKey
    print('Wrote /keys/@%s/aesPkamPublicKey_pem.json' % without_prefix_atSign)

    del selfEncryptionKey, without_prefix_atSign

def get_pem_encrypt_private_key_from_file(atSign: str):
    from ujson import loads
    from lib.at_client.at_utils import without_prefix
    with open('/keys/@%s/aesEncryptPrivateKey_pem.json' %without_prefix(atSign), 'r') as f:
        info = loads(f.read())
        return info["aesEncryptPrivateKey"]

def get_pem_encrypt_public_key_from_file(atSign: str):
    from ujson import loads
    from lib.at_client.at_utils import without_prefix
    with open('/keys/@%s/aesEncryptPublicKey_pem.json' %without_prefix(atSign), 'r') as f:
        info = loads(f.read())
        return info["aesEncryptPublicKey"] # n, e

def get_pem_pkam_public_key_from_file(atSign: str):
    from ujson import loads
    from lib.at_client.at_utils import without_prefix
    with open('/keys/@%s/aesPkamPublicKey_pem.json' %without_prefix(atSign), 'r') as f:
        info = loads(f.read())
        return info["aesPkamPublicKey"]

def get_pem_pkam_private_key_from_file(atSign: str):
    from ujson import loads
    from lib.at_client.at_utils import without_prefix
    with open('/keys/@%s/aesPkamPrivateKey_pem.json' %without_prefix(atSign), 'r') as f:
        info = loads(f.read())
        return info["aesPkamPrivateKey"]