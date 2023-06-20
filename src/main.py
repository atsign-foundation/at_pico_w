import sys
# Needed when running on Linux to find imports in lib directory
if sys.platform == 'linux':
    sys.path.append('./lib')
import ujson as json
import os
import time
from atclient import *

import logging
log=logging.getLogger(__name__)
import _thread

loading = False

def read_settings():
    """Read settings from settings.json file
    
    ssid: The SSID of the WiFi network to be connected to
    password: The password of the WiFi network to be connect to
    atSign: The atSign being used to send
    pkamKey: The atSign's PKAM authentication key (as integers)
    encryptKey: The atSign's encryption key (as integers)
    """
    with open(os.getcwd() + '/settings.json') as f:
        settings = json.loads(f.read())
        return (settings['ssid'], settings['password'],
            settings['atSign'].replace('@', ''), 
            settings['recipientAtSign'].replace('@', ''), 
            settings['pkamKey'], settings['encryptKey'])

def read_keys(atSign):
    """Reads keys from the atKeys file

    Reads keys associated with the atSign found in the settings.json
    """
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

def write_keys(ssid, password, atSign, atRecipient):
    """Write extracted keys into settings.json"""
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
            "\",\n\t\"recipientAtSign\": \"" + atRecipient +
            "\",\n\t\"pkamKey\": [\n\t\t\t\t\t" + str(pkamKey[0]) + ",\n\t\t\t\t\t" + str(pkamKey[1]) + ",\n\t\t\t\t\t" + str(pkamKey[2]) +
            ",\n\t\t\t\t\t" + str(pkamKey[3]) + ",\n\t\t\t\t\t" + str(pkamKey[4]) + "\n\t\t\t\t  ],\n" +
            "\t\"encryptKey\": [\n\t\t\t\t\t" + str(encryptKey[0]) + ",\n\t\t\t\t\t" + str(encryptKey[1]) + ",\n\t\t\t\t\t" + str(encryptKey[2]) +
            ",\n\t\t\t\t\t" + str(encryptKey[3]) + ",\n\t\t\t\t\t" + str(encryptKey[4]) + "\n\t\t\t\t  ]\n}")
    sys.exit()

def main():
    # logging.basicConfig(level = logging.INFO)
    ssid, password, atSign, atRecipient, pkamKey, encryptKey = read_settings()
    if atRecipient == '':
        atRecipient='NOT SET'
    if pkamKey==[]:
        # Transfer keys from atKeys file to settings
        write_keys(ssid,password,atSign,atRecipient)
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

    connected = False

    while True:
        global lock
        print("Welcome! What would you like to do?\n"
            "\t1) Change recipient atSign (presently " + atRecipient + ")\n"
            "\t2) Connect to " + atSign + "\n"
            "\t3) Send at atTalk message to " + atRecipient + "\n"
            "\t4) Exit")
        opt=input("> ")
        if int(opt) == 1:
            atRecipient=input("atSign:")
            connected = False
        elif int(opt) == 2:
            if atRecipient != '' and atRecipient != 'NOT SET':
                print('Connecting to ' + atSign + "...")
                atc = atClient(atsign=atSign, recipient=atRecipient)
                atServer,atPort=atc.discover()
                atc.connect(atServer,atPort)
                atc.authenticate(pkamKey)
                atc.getsharedkey(encryptKey)
                atc.getrecipientsharedkey(encryptKey)
                connected = True
                print("Connected")
            else:
                print("You must set recipient atSign before continuing")
        elif int(opt) == 3:
            if connected:
                # init second thread to read from socket (monitor)
                global monitoring
                monitoring = True
                read_thread = _thread.start_new_thread(atc.attalk_recv, ())
                print('To return to menu type: /exit\n')
                while True:
                    # print(atSign+":",end='\r')
                    # print(">",end='\r')
                    msg=input("").encode()
                    if msg == b'/exit':
                        break
                    atc.attalk_send(msg=msg)
                # stop second thread
                lock.acquire(1)
                monitoring = False
                lock.release()
                # join method does not exist in _thread
            else:
                print("You must connect to " + atSign + " before continuing")
        elif int(opt) == 4:
            sys.exit(0)
        else:
            print('Invalid option. Please enter a number in the range [1-4]')

if __name__ == '__main__':
    main()
