# TODO move imports inside functions to delete later
import ujson
from lib.at_client import at_utils

def read_settings():
    with open('settings.json') as f:
        info = ujson.loads(f.read())
        return info['ssid'], info['password'], info['atSign'].replace('@', '')
    
def read_key(atSign: str):
    atSign = at_utils.without_prefix(atSign)
    path = '/keys/@' + atSign + '_key.atKeys'
    with open(path) as f:
        info = ujson.loads(f.read())
        return info['aesEncryptPrivateKey'], info['aesEncryptPublicKey'], info['aesPkamPrivateKey'], info['aesPkamPublicKey'], info['selfEncryptionKey']