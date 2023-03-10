import sys
# Needed when running on Linux to find imports in lib directory
sys.path.append('./lib')
import ujson as json
import os
from aes import aes_decrypt
from atclient import atClient

import logging
logging.basicConfig(level = logging.INFO)
log=logging.getLogger(__name__)


def read_settings():
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
    atRoot='root.atsign.org'
    atRecipient='cpswan'
    ssid, password, atSign, privateKey = read_settings()
    aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey, aesPkamPublicKey, selfEncryptionKey = read_key(atSign)
    pkamPrivateKey = aes_decrypt(aesPkamPrivateKey, selfEncryptionKey)
    encryptPrivateKey = aes_decrypt(aesEncryptPrivateKey, selfEncryptionKey)

    if sys.platform != 'linux':
        wlan = network.WLAN(network.STA_IF)  # type: ignore
        wlan.active(True)
        wlan.connect(ssid, password)
    
    ssl_params= { 'server_hostname':atRoot}
    atc = atClient(rootserver=atRoot, atsign=atSign, pkam=pkamPrivateKey,
        encryptpriv=encryptPrivateKey, recipient=atRecipient, ssl_params=ssl_params)
    atc.connect()
    atc.authenticate()
    atc.getsharedkey()
    atc.attalk(msg=b'Hello World!')

if __name__ == '__main__':
    main()