import gc
import ujson as json
import os
import time
import usocket as socket # type: ignore
import ussl as ssl # type: ignore
from aes import aes_decrypt
from pem_service import get_pem_parameters, get_pem_key, get_pub_parameters

import logging
log=logging.getLogger(__name__)

def b42_urlsafe_encode(payload):
        return string.translate(b2a_base64(payload)[:-1].decode('utf-8'),{ ord('+'):'-', ord('/'):'_' })

def pkcs7pad(text):
    return text+chr(16-len(text)%16)*(16-len(text)%16)

def send_verb(skt, verb):
    skt.write((verb + "\r\n").encode())
    time.sleep(1)
    response = b''
    data = skt.readline()
    response += data
    parts = response.decode().split('\n') 
    return parts[0], parts[1]

def read_settings():
    cwd = os.getcwd()
    localroot=""        
    if cwd=="/":
        # Looks like we're running on a devboard with our code in /
        localroot="/"
    else:
        # Running somewhere else, let's go to parent directory
        cwds=cwd.split("/")
        for dir in cwds[1:-1]:
            localroot=localroot+"/"+dir
        localroot=localroot+"/"
    with open(localroot + 'settings.json') as f:
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

class atException(Exception):
    pass

class atClient:

    def __init__(self, rootserver:str, rootport:int=64, atsign:str=None, pkam:str=None, 
                encryptpriv:str=None, recipient:str=None, keepalive:int=0, ssl_params={}):
        self.sock = None
        self.rootserver = rootserver
        self.rootport = rootport
        self.server = None
        self.port = 0
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        if atsign is None or pkam is None:
            raise atException("Must provide atsign name and atsign pkam key")
        self.atsign = atsign
        self.recipient = recipient
        pkamKey = get_pem_parameters(get_pem_key(ubinascii.unhexlify(pkam).decode()))
        self.pkamkey = rsa.PrivateKey(pkamKey[0], pkamKey[1], pkamKey[2], pkamKey[3], pkamKey[4])
        privKey = get_pem_parameters(get_pem_key(ubinascii.unhexlify(encryptpriv).decode()))
        self.encryptpriv = rsa.PrivateKey(privKey[0], privKey[1], privKey[2], privKey[3], privKey[4])
        # Take advantage of the fact that the public key parameters are in the private key :)
        self.encryptpub = rsa.PublicKey(privKey[0], privKey[1])
        # Key wrangling creates lots of temp objects that can now be cleaned up
        gc.collect()
        self.receivepub = None
        self.sharedkey = None

    # connect or throw exception
    def connect(self, timeout=5.0)->None:
        log.info("Connect to atRoot server {}:{}", self.rootserver, self.rootport)
        self.sock = None    # by definition
        # if caller gives me an already connected socket like object, we'll use that...
        try:
            rootsock = socket.socket()
            addr = socket.getaddrinfo(self.rootserver, self.rootport)[0][-1]
            rootsock.settimeout(timeout)       # timeout for connect
            rootsock.connect(addr)
            rootsock = ssl.wrap_socket(rootsock, **self.ssl_params)
            rootsock.do_handshake()
            mb= "{}\n".format(self.atsign).encode("utf-8")
            log.info("sending root request {}", mb)
            rootsock.write(mb)
            rootsock.settimeout(timeout)       # timeout for read
            resp = rootsock.readline()
            if resp is None or len(resp)<4:
                raise atException("timeout")
            ret=resp.decode("utf-8")
            log.info("root response : {}", ret)
        except Exception as err:
            log.exc(err, "during root server {}:{} cnx", self.rootserver, self.rootport)
            raise err
        # parse response to get atServer to connect to
        # response may be 'null' -> no such atsign or something like:
        # 779c7c26-f7e2-5e98-a228-cd2ffe9f976d.swarm0002.atsign.zone:5243
        # this is a server fqdn and a port for a TLS socket connection
        asl = ret[1:].split(":")
        if len(asl)<2:
            log.warning("Bad root response for {}, got {}", self.atsign, ret)
            raise atException("bad root response")
        self.server = asl[0]
        self.port = int(asl[1])
        try:
            log.info("Connecting to atServer for {} -  {}:{}", self.atsign, self.server, self.port)
            self.sock = socket.socket()
            addr = socket.getaddrinfo(self.server, self.port)[0][-1]
            self.sock.settimeout(timeout)       # timeout for connect
            self.sock.connect(addr)
            self.sock = ssl.wrap_socket(self.sock, **self.ssl_params)
            self.sock.do_handshake()
            log.info("Connected OK to atServer {}:{}, info request...", self.server, self.port)
            response, command = send_verb(self.sock, 'info:brief')
            log.info("atSign info response : {}", response)
        except Exception as err:
            log.exc(err, "During atSign server {}:{} cnx", self.server, self.port)
            self.sock.close()
            self.sock = None
            raise err

def main():

    ssid, password, atSign, privateKey = read_settings()
    print(ssid,password,atSign,privateKey)
    aesEncryptPrivateKey, aesEncryptPublicKey, aesPkamPrivateKey, aesPkamPublicKey, selfEncryptionKey = read_key(atSign)
    pkamPrivateKey = aes_decrypt(aesPkamPrivateKey, selfEncryptionKey)
    encryptPrivateKey = aes_decrypt(aesEncryptPrivateKey, selfEncryptionKey)
    print(pkamPrivateKey)
    print(encryptPrivateKey)

if __name__ == '__main__':
    main()