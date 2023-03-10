import sys
# Needed when running on Linux to find imports in lib directory
if sys.platform == 'linux':
    sys.path.append('./lib')
import gc
import ujson as json
import os
import time
from atclient import atClient

import logging
logging.basicConfig(level = logging.INFO)
log=logging.getLogger(__name__)

def read_settings():
    with open(os.getcwd() + '/settings.json') as f:
        settings = json.loads(f.read())
        return (settings['ssid'], settings['password'],
            settings['atSign'].replace('@', ''), settings['pkamKey'],
            settings['encryptKey'])

def read_keys(atSign):
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
        return (info['aesEncryptPrivateKey'], info['aesEncryptPublicKey'],
            info['aesPkamPrivateKey'], info['aesPkamPublicKey'],
            info['selfEncryptionKey'])

def write_keys(ssid, password, atSign):
    log.info("Writing keys")
    from aes import aes_decrypt
    from pem_service import get_pem_parameters, get_pem_key
    (aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey,
            aesPkamPublicKey, selfEncryptionKey) = read_keys(atSign)
    pkamPrivateKey = aes_decrypt(aesPkamPrivateKey, selfEncryptionKey)
    encryptPrivateKey = aes_decrypt(aesEncryptPrivateKey, selfEncryptionKey)
    pkamKey = get_pem_parameters(get_pem_key(pkamPrivateKey))
    encryptKey = get_pem_parameters(get_pem_key(encryptPrivateKey))
    with open(os.getcwd() + '/settings.json', 'w') as w:
        w.write("{\n\t\"ssid\": \"" + ssid + "\",\n\t\"password\": \"" + password + "\",\n\t\"atSign\": \"" + atSign +
            "\",\n\t\"pkamKey\": [\n\t\t\t\t\t" + str(pkamKey[0]) + ",\n\t\t\t\t\t" + str(pkamKey[1]) + ",\n\t\t\t\t\t" + str(pkamKey[2]) +
            ",\n\t\t\t\t\t" + str(pkamKey[3]) + ",\n\t\t\t\t\t" + str(pkamKey[4]) + "\n\t\t\t\t  ],\n" +
            "\t\"encryptKey\": [\n\t\t\t\t\t" + str(encryptKey[0]) + ",\n\t\t\t\t\t" + str(encryptKey[1]) + ",\n\t\t\t\t\t" + str(encryptKey[2]) +
            ",\n\t\t\t\t\t" + str(encryptKey[3]) + ",\n\t\t\t\t\t" + str(encryptKey[4]) + "\n\t\t\t\t  ]\n}")
    sys.exit()

def main():
    print(gc.mem_free())
    atRoot='root.atsign.org'
    atRecipient='cpswan'
    ssid, password, atSign, pkamKey, encryptKey = read_settings()
    if pkamKey==[]:
        # Transfer keys from atKeys file to settings
        write_keys(ssid,password,atSign)
    if sys.platform != 'linux':
        import network # type: ignore
        from ntp_client import sync_time
        wlan = network.WLAN(network.STA_IF)  # type: ignore
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected() and wlan.status() >= 0:
            time.sleep(1)
            log.info("Wi-Fi .. Connecting")
        log.info("Wi-Fi Connected")
        sync_time()
    
    ssl_params= { 'server_hostname':atRoot }
    print(gc.mem_free())
    atc = atClient(recipient=atRecipient, atsign=atSign, ssl_params=ssl_params)
    print(gc.mem_free())
    atServer,atPort=atc.discover(rootserver=atRoot)
    atc.connect(atServer,atPort)
    print(gc.mem_free())
    atc.authenticate(pkamKey)
    print(gc.mem_free())
    atc.getsharedkey(encryptKey)
    print(gc.mem_free())
    atc.attalk(msg=b'Hello World!')
    print(gc.mem_free())

if __name__ == '__main__':
    main()