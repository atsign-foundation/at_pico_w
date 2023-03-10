import ujson as json
import os
from aes import aes_decrypt


def read_settings():
    print(os.getcwd())
    with open(os.getcwd() + '/settings.json') as f:
        settings = json.loads(f.read())
        return settings['ssid'], settings['password'], settings['atSign'].replace('@', ''), settings['privateKey']

def read_key(atSign):
    cwd = os.getcwd()
    if cwd=="/":
        # Looks like we're running on a devboard with our code in /
        homeroot="/"
    else:
        # Running somewhere else, let's try to get the home directory
        cwds=cwd.split("/")
        homeroot="/"+cwds[1]+"/"+cwds[2]+"/"
    with open(homeroot + '.atsign/keys/@' + atSign + '_key.atKeys') as f:
        info = json.loads(f.read())
        return info['aesEncryptPrivateKey'], info['aesEncryptPublicKey'], info['aesPkamPrivateKey'], info['aesPkamPublicKey'], info['selfEncryptionKey']

def main():

    ssid, password, atSign, privateKey = read_settings()
    print(ssid,password,atSign,privateKey)
    aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey, aesPkamPublicKey, selfEncryptionKey = read_key(atSign)
    pkamPrivateKey = aes_decrypt(aesPkamPrivateKey, selfEncryptionKey)
    print(pkamPrivateKey)

if __name__ == '__main__':
    main()