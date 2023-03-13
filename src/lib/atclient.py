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
log=logging.getLogger(__name__)

def b42_urlsafe_encode(payload):
    """URL safe Base64 encoding

    Returns a Base64 encoded string with substituitions that can safely be
    passed in URLs
    """
    return string.translate(ubinascii.b2a_base64(payload)[:-1].decode('utf-8'),{ ord('+'):'-', ord('/'):'_' })

def pkcs7pad(text):
    """Pads text according to the PCKS7 specification
    """
    return text+chr(16-len(text)%16)*(16-len(text)%16)

def send_verb(skt, verb):
    """Send an atProtocol verb
    """
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
    """A class for interacting with an atServer using the atProtocol
    """

    def __init__(self, atsign:str=None, recipient:str=None):
        self.sock = None
        self.server = None
        self.port = 0
        self.cb = None
        self.atsign = atsign
        self.recipient = recipient
        self.receivepub = None
        self.sharedkey = b''

    def discover(self, rootserver:str="root.atsign.org",
        rootport:int=64, timeout=5.0):
        """Discover the FQDN and port of an atServer for an atSign

        Find the location for atServer using the specified atRoot
        directory (normally root.atsign.org:64)

        Parameters
        ----------
        rootserver : str, optional
        The atRoot to be used for directory lookups (default is
        root.atsign.org)
        rootport : int, optional
        The port of the atRoot server (default is 64)
        timeout : float, optional
        Timeout (in seconds) for socket operations (default is 5.0)

        Returns
        -------
        atServer : str
        The FQDN of the atServer
        atServer Port : int
        The port of the atServer
        """
        log.info("Connect to atRoot server {}:{}", rootserver, rootport)
        try:
            rootsock = socket.socket()
            rootaddr = socket.getaddrinfo(rootserver, rootport)[0][-1]
            rootsock.settimeout(timeout)       # timeout for connect
            rootsock.connect(rootaddr)
            roottls = ssl.wrap_socket(rootsock)
            #rootsock.do_handshake()
            mb= "{}\n".format(self.atsign).encode("utf-8")
            log.info("sending root request {}", mb)
            roottls.write(mb)
            resp = roottls.readline()
            if resp is None or len(resp)<4:
                raise atException("Short response")
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
        """Connect to an atServer

        Parameters
        ----------
        attserver : str
        The FQDN of the atServer e.g.
        779c7c26-f7e2-5e98-a228-cd2ffe9f976d.swarm0002.atsign.zone
        rootport : int
        The port of the atServer e.g. 5243
        timeout : float, optional
        Timeout (in seconds) for socket operations (default is 5.0)
        """
        try:
            log.info("Connecting to atServer for {} -  {}:{}", self.atsign, atserver, atport)
            self.server=atserver
            self.port=atport
            self.sock = socket.socket()
            addr = socket.getaddrinfo(atserver, atport)[0][-1]
            self.sock.settimeout(timeout)       # timeout for connect
            self.sock.connect(addr)
            self.sock = ssl.wrap_socket(self.sock)
            log.info("Connected OK to atServer {}:{}, info request...", atserver, atport)
            response, command = send_verb(self.sock, 'info:brief')
            log.info("atSign info response : {}", response)
        except Exception as err:
            log.exc(err, "During atSign server {}:{} cnx", atserver, atport)
            self.sock.close()
            self.sock = None
            raise err

    def authenticate(self, pkamKey):
        """Authenticate with an atServer using a PKAM key

        Parameters
        ----------
        pkamKey : list
        The integers for an RSA private key extracted from a .pem encoded key
        """
        try:
            log.info("Doing PKAM authentication to {}", self.atsign)
            response, command = send_verb(self.sock, 'from:' + self.atsign)
            if response is None or len(response)<4:
                raise ATException("Short response")
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
        """Get the AES shared key to communicate with a recipient atSign

        Parameters
        ----------
        privKey : list
        The integers for an RSA private key extracted from a .pem encoded key
        """
        try:
            log.info("Fetching sharedAESKey for {}", self.recipient)
            response, command = send_verb(self.sock, 'llookup:shared_key.' + self.recipient +'@' + self.atsign)
            log.info("Got this response for llookup: {}", response)
            if response is None or len(response)<4:
                raise ATException("Short response")
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
                import urandom
                for n in range(8):
                    self.sharedkey+=urandom.getrandbits(32).to_bytes(4,'little')
                shared_key = ubinascii.b2a_base64(self.sharedkey).rstrip()
                log.info("Generated shared key {}", shared_key)
                # Take advantage of the fact that the public key parameters are in the private key :)
                encryptpub = rsa.PublicKey(privKey[0], privKey[1])
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
                gc.collect()
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

    def attalk(self, msg:bytes, topic:str="attalk", namespace:str="ai6bh"):
        """Send a notification to an atTalk client
        
        Parameters
        ----------
        msg : bytes
        The message to be sent
        topic : str, optional
        The topic key being used by the atTalk client (default 'attalk')
        namespace : str, optional
        The namespace being used by the atTalk client (default 'atpicow')
        """
        try:
            log.info("publish message to astign: {}",msg)
            #TODO ivs should not be zeroes, and should be shared in metadata
            iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            aes = ucryptolib.aes(self.sharedkey, 6, iv)
            b64encrypted_msg = ubinascii.b2a_base64(aes.encrypt(pkcs7pad(msg))).rstrip().decode()
            response, command = send_verb(self.sock,
                'notify:update:ttr:-1:@'+self.recipient+':'+topic+'.'+
                namespace+'@'+self.atsign+':'+b64encrypted_msg)
            log.info("Got this response for publishing: {}", response)
        except Exception as err:
            log.exc(err, "during info publish to atsign server {}:{} cnx", self.server, self.port)
            self.disconnect()
