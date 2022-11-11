from lib.at_client.io_util import read_key
from lib.aes import aes_decrypt
from lib.at_client.at_utils import without_prefix
from lib.pem_service import get_pem_parameters, get_pem_key
import os

# initializes /keys/@alice/ with RSA keys in their pem form
# e.g. /keys/@alice/aesEncryptPrivateKey_pem.json
def initialize_keys(atSign: str) -> None:
    aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey, aesPkamPublicKey, selfEncryptionKey = read_key(atSign)

    try:
        os.mkdir('/keys/@%s' % without_prefix(atSign))
    except:
        pass

    # aesEncryptPrivateKey_pem_parameters = get_pem_parameters(get_pem_key(aes_decrypt(aesEncryptPrivateKey, selfEncryptionKey), 'private'), 'private')
    # with open('/keys/@%s/aesEncryptPrivateKey_pem.json' % without_prefix(atSign), 'w') as w:
    #     w.write("{\n\"aesEncryptPrivateKey\": [\n" + str(aesEncryptPrivateKey_pem_parameters[0]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[1]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[2]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[3]) + ",\n" + str(aesEncryptPrivateKey_pem_parameters[4]) + "\n]\n}")
    # del aesEncryptPrivateKey_pem_parameters, aesEncryptPrivateKey

    # aesEncryptPublicKey_pem_parameters = get_pem_parameters(get_pem_key(aes_decrypt(aesEncryptPublicKey, selfEncryptionKey), 'public'), 'public')
    # with open('/keys/@%s/aesEncryptPublicKey_pem.json' % without_prefix(atSign), 'w') as w:
    #     w.write("{\n\"aesEncryptPublicKey\": [\n" + str(aesEncryptPublicKey_pem_parameters[0]) + ",\n" + str(aesEncryptPublicKey_pem_parameters[1]) + ",\n" + str(aesEncryptPublicKey_pem_parameters[2]) + ",\n" + str(aesEncryptPublicKey_pem_parameters[3]) + ",\n" + str(aesEncryptPublicKey_pem_parameters[4]) + "\n]\n}")
    # del aesEncryptPublicKey_pem_parameters, aesEncryptPublicKey

    aesPkamPrivateKey_pem_parameters = get_pem_parameters(get_pem_key(aes_decrypt(aesPkamPrivateKey, selfEncryptionKey), 'private'), 'private')
    with open('/keys/@%s/aesPkamPrivateKey_pem.json' % without_prefix(atSign), 'w') as w:
        w.write("{\n\"aesPkamPrivateKey\": [\n" + str(aesPkamPrivateKey_pem_parameters[0]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[1]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[2]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[3]) + ",\n" + str(aesPkamPrivateKey_pem_parameters[4]) + "\n]\n}")
    del aesPkamPrivateKey_pem_parameters, aesPkamPrivateKey

    # aesPkamPublicKey_pem_parameters = get_pem_parameters(get_pem_key(aes_decrypt(aesPkamPublicKey, selfEncryptionKey)))
    # with open('/keys/@%s/aesPkamPublicKey_pem.json' % without_prefix(atSign), 'w') as w:
    #     w.write("{\n\"aesPkamPublicKey\": [\n" + str(aesPkamPublicKey_pem_parameters[0]) + ",\n" + str(aesPkamPublicKey_pem_parameters[1]) + ",\n" + str(aesPkamPublicKey_pem_parameters[2]) + ",\n" + str(aesPkamPublicKey_pem_parameters[3]) + ",\n" + str(aesPkamPublicKey_pem_parameters[4]) + "\n]\n}")
    # del aesPkamPublicKey_pem_parameters, aesPkamPublicKey

    del selfEncryptionKey

def get_pem_pkam_private_key_from_file(atSign: str):
    import ujson
    with open('/keys/@%s/aesPkamPrivateKey_pem.json' %without_prefix(atSign), 'r') as f:
        info = ujson.loads(f.read())
        return info["aesPkamPrivateKey"]