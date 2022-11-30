
def read_settings():
    with open('settings.json') as f:
        from ujson import loads
        info = loads(f.read())
        del loads
        return info['ssid'], info['password'], info['atSign'].replace('@', '')
    
def read_key(atSign: str):
    from lib.at_client.at_utils import without_prefix
    atSign = without_prefix(atSign)
    del without_prefix
    path = '/keys/@' + atSign + '_key.atKeys'
    with open(path) as f:
        from ujson import loads
        info = loads(f.read())
        del loads
        return info['aesEncryptPrivateKey'], info['aesEncryptPublicKey'], info['aesPkamPrivateKey'], info['aesPkamPublicKey'], info['selfEncryptionKey']