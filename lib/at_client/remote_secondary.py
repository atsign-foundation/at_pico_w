import time
import usocket
import ussl as ssl # type: ignore
from lib.at_client import at_utils

class RemoteSecondary:

    # rootUrl e.g. root.atsign.org:64
    # atSign e.g. "alice" or "@alice"
    def __init__(self, rootUrl: str, atSign: str, wlan=None):
        self.rootUrl = rootUrl 
        self.atSign = at_utils.format_atSign(atSign)
        self.wlan = wlan



    def is_connected(self) -> bool:
        return self.ss is not None

    # returns two variables: response, command
    # executes verb on secondary
    def send_verb(self, verb: str):
        self.ss.write((verb + "\r\n").encode())
        response = b''
        time.sleep(2)
        data = self.ss.read()
        time.sleep(2)
        print('data from verb: %s' % data)
        if data is not None:
            response += data
            parts = response.decode().split('\n')
        else:
            parts = ['', '']
            
        return parts[0], parts[1]

    def get_secondary_address(self):
        return self.secondary_address

    # initializes self.ss (usocket.socket object), secondary_address nullable
    def connect_to_secondary(self, secondary_address=None) -> None:
        # print('Connecting to secondary... ', end="")

        if(secondary_address == None):
            rootHost = self.rootUrl.split(':')[0]
            # rootPort = int(self.rootUrl.split(':')[1])
            rootPort = 64
            # print('Finding secondary...')
            self.secondary_address = self.find_secondary(self.atSign, rootHost, rootPort)
            time.sleep(2)
        else:
            self.secondary_address = secondary_address

        ss_split = self.secondary_address.split(":")
        print(ss_split)
        address = ss_split[0]
        port = ss_split[1]

        a = usocket.getaddrinfo(address, int(port))[0][-1]
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) 

        try:
            s.connect(a)
        except OSError as e:
            if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e
            
        s.setblocking(False)
        ss = ssl.wrap_socket(s, do_handshake = True)
        self.ss = ss
        
    # returns the secondary address (as a string) of a given atSign, rootHost, and rootPort
    def find_secondary(self, atSign: str, rootHost: str, rootPort: int) -> str:
        atSign = at_utils.without_prefix(atSign)
        # print('Finding secondary for @' + atSign + '...')
        a = usocket.getaddrinfo(rootHost, rootPort)[0][-1]
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) 

        try:
            s.connect(a)
        except OSError as e:
            if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e
            
        s.setblocking(False)
        time.sleep(1)
        ss = ssl.wrap_socket(s, do_handshake = True)
        time.sleep(1)

        ss.write((atSign + "\r\n").encode())
        time.sleep(1)

        response = b''
        data = ss.read()
        time.sleep(0.5)
        response += data
        secondary = response.decode().replace('@', '')
        secondary = secondary.replace('\r\n', '')
    
        ss.close()
        # print('Address found: %s' % secondary)
        return secondary
    