import gc
import time
import ubinascii
import ucryptolib
import usocket as socket # type: ignore
import ussl as ssl # type: ignore
from pem_service import get_pub_parameters
from third_party import rsa
from third_party import string

import logging
#logging.basicConfig(level = logging.INFO)
log=logging.getLogger(__name__)

def b42_urlsafe_encode(payload):
        return string.translate(ubinascii.b2a_base64(payload)[:-1].decode('utf-8'),{ ord('+'):'-', ord('/'):'_' })

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


class atException(Exception):
    pass

class atClient:

    def __init__(self, atsign:str=None, recipient:str=None, ssl_params={}):
        self.sock = None
        self.server = None
        self.port = 0
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.atsign = atsign
        self.recipient = recipient
        self.receivepub = None
        self.sharedkey = None

    def discover(self, rootserver:str, rootport:int=64, timeout=5.0)->None:
        log.info("Connect to atRoot server {}:{}", rootserver, rootport)
        # if caller gives me an already connected socket like object, we'll use that...
        try:
            rootsock = socket.socket()
            addr = socket.getaddrinfo(rootserver, rootport)[0][-1]
            rootsock.settimeout(timeout)       # timeout for connect
            rootsock.connect(addr)
            print(gc.mem_free())
            roottls = ssl.wrap_socket(rootsock, **self.ssl_params)
            #rootsock.do_handshake()
            mb= "{}\n".format(self.atsign).encode("utf-8")
            log.info("sending root request {}", mb)
            roottls.write(mb)
            #rootsock.settimeout(timeout)       # timeout for read
            resp = roottls.readline()
            if resp is None or len(resp)<4:
                raise atException("timeout")
            ret=resp.decode("utf-8")
            log.info("root response : {}", ret)
        except Exception as err:
            log.exc(err, "during root server {}:{} cnx", rootserver, rootport)
            raise err
        # parse response to get atServer to connect to
        # response may be 'null' -> no such atsign or something like:
        # 779c7c26-f7e2-5e98-a228-cd2ffe9f976d.swarm0002.atsign.zone:5243
        # this is a server fqdn and a port for a TLS socket connection
        asl = ret[1:].split(":")
        if len(asl)<2:
            log.warning("Bad root response for {}, got {}", self.atsign, ret)
            raise atException("bad root response")
        rootsock.close()
        return(asl[0],int(asl[1]))

    def connect(self, atserver, atport, timeout=5.0):
        try:
            log.info("Connecting to atServer for {} -  {}:{}", self.atsign, atserver, atport)
            self.sock = socket.socket()
            addr = socket.getaddrinfo(atserver, atport)[0][-1]
            self.sock.settimeout(timeout)       # timeout for connect
            self.sock.connect(addr)
            self.sock = ssl.wrap_socket(self.sock, **self.ssl_params)
            #self.sock.do_handshake()
            log.info("Connected OK to atServer {}:{}, info request...", atserver, atport)
            response, command = send_verb(self.sock, 'info:brief')
            log.info("atSign info response : {}", response)
        except Exception as err:
            log.exc(err, "During atSign server {}:{} cnx", atserver, atport)
            self.sock.close()
            self.sock = None
            raise err

    def authenticate(self, pkamKey):
        try:
            log.info("Doing PKAM authentication to {}", self.atsign)
            response, command = send_verb(self.sock, 'from:' + self.atsign)
            if response is None or len(response)<4:
                raise ATException("timeout")
            challenge = response.replace('@data:', '')
            log.info("atsign pkam challenge : {}", challenge)
            pkamrsa=rsa.PrivateKey(pkamKey[0], pkamKey[1], pkamKey[2], pkamKey[3], pkamKey[4])
            signature = b42_urlsafe_encode(rsa.sign(challenge, pkamrsa, 'SHA-256'))
            # Key manipulation creates a lot of garbage, so let's clear that up now the signature is ready
            gc.collect()
            log.info("atsign pkam signature : {}", signature)
            response, command = send_verb(self.sock, 'pkam:' + signature)
            log.info("atsign pkam authenticated : {}", response)
        except Exception as err:
            log.exc(err, "during atsign server {}:{} cnx", self.server, self.port)
            self.sock.close()
            self.sock = None
            raise err

    def getsharedkey(self, privKey):
        try:
            log.info("Fetching sharedAESKey for {}", self.recipient)
            response, command = send_verb(self.sock, 'llookup:shared_key.' + self.recipient +'@' + self.atsign)
            log.info("Got this response for llookup: {}", response)
            if response is None or len(response)<4:
                raise ATException("timeout")
            if response.startswith('@' + self.atsign + '@'):
                response=response.replace('@' + self.atsign + '@','')
                log.info("Truncated response is: {}", response)
            # does my atSign already have the recipient's shared key?
            if response.startswith('data:'):
                privrsa=rsa.PrivateKey(privKey[0], privKey[1], privKey[2], privKey[3], privKey[4])
                shared_key = rsa.decrypt(ubinascii.a2b_base64(response.replace('data:','')), privrsa)
                self.sharedkey=ubinascii.a2b_base64(shared_key)
                log.info("Got shared key from atServer: {}", shared_key)
                gc.collect()
            # or do I need to create, store and share a new shared key?
            elif response.startswith('error:AT0015-key not found'):
                log.info("No local copy of the key, so we need to make one")
                # Generate an AES256 key and base64 encode it
                self.sharedkey=ucrypto.getrandbits(256)
                shared_key = ubinascii.b2a_base64(self.sharedkey).rstrip()
                log.info("Generated shared key {}", shared_key)
                # Take advantage of the fact that the public key parameters are in the private key :)
                encryptpub = rsa.PublicKey(self.encryptpriv[0], self.encryptpriv[1])
                # Encrypt the shared_key with our RSA public key
                encrypted_shared_key = ubinascii.b2a_base64(rsa.encrypt(shared_key, encryptpub)).rstrip().decode()
                log.info("Encrypted shared key {}", encrypted_shared_key)
                # Store the shared key
                response, command = send_verb(self.sock, 'update:shared_key.' + self.recipient +'@' + self.atsign + ' ' + encrypted_shared_key)
                log.info("Got this response for update: {}", response)
                # Get public key for recipient
                response, command = send_verb(self.sock, 'plookup:publickey@' + self.recipient)
                log.info("Got this public key: {}", response)
                rpubkey=response.replace('@' + self.atsign + '@data:','')
                log.info("Trimmed public key down to: {}", rpubkey)
                # Use their public key to encrypt the shared key
                rxKey = get_pub_parameters(rpubkey)
                self.receivepub = rsa.PublicKey(rxKey[0], rxKey[1])
                rencrypted_shared_key = ubinascii.b2a_base64(rsa.encrypt(shared_key, self.receivepub)).rstrip().decode()
                # Send the shared key
                response, command = send_verb(self.sock, 'update:ttr:86400:@' + self.recipient + ':shared_key@' + self.atsign + ' ' + rencrypted_shared_key)
                log.info("Got this response for sharing: {}", response)
            else:
                # Something has gone wrong and we don't have a shared key to work with
                log.warning("No shared key found or created during atsign server {}:{} cnx", self.server, self.port)
                self.sock.close()
                self.sock = None
                raise Exception("Shared key not found or created")
        except Exception as err:
            log.exc(err, "during atsign server {}:{} cnx", self.server, self.port)
            self.sock.close()
            self.sock = None
            raise err

    def attalk(self, msg:bytes):
        try:
            log.info("publish message to astign: {}",msg)
            #TODO ivs should not be zeroes, and should be shared in metadata
            iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            aes = ucryptolib.aes(self.sharedkey, 6, iv)
            b64encrypted_msg = ubinascii.b2a_base64(aes.encrypt(pkcs7pad(msg))).rstrip().decode()
            #encrypted_msg = ucrypto.AES(self.sharedkey, mode=ucrypto.AES.MODE_CTR, counter=iv).encrypt(pkcs7pad(msg))
            #b64encrypted_msg = ubinascii.b2a_base64(encrypted_msg).rstrip().decode()
            shared_key = ubinascii.b2a_base64(self.sharedkey).rstrip().decode()
            response, command = send_verb(self.sock,
                'notify:update:ttr:-1:@'+self.recipient+':message.infrafon@'+self.atsign+':'+b64encrypted_msg)
            log.info("Got this response for publishing: {}", response)
        except Exception as err:
            log.exc(err, "during info publish to atsign server {}:{} cnx", self.server, self.port)
            self.disconnect()