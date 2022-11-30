class RemoteSecondary:

    # rootUrl e.g. root.atsign.org:64
    # atSign e.g. "alice" or "@alice"
    def __init__(self, atSign: str, rootUrl='root.atsign.org:64', ss_address=None, wlan=None):
        self.rootUrl = rootUrl 
        from lib.at_client.at_utils import format_atSign
        self.atSign = format_atSign(atSign)
        del format_atSign
        self.secondary_address = ss_address
        # self.wlan = wlan not needed atm

    def is_connected(self) -> bool:
        return self.ss is not None

    # TODO add verbose option
    def send_verb(self, verb: str):
        """
        Returns a Tuple (response, command)
        """
        from utime import sleep
        self.ss.write((verb + "\r\n").encode())
        response = b''
        sleep(2)
        data = self.ss.read()
        sleep(2)
        if data is not None:
            response += data
            parts = response.decode().split('\n')
        else:
            parts = ['', '']
        sleep(1)
            
        return parts[0], parts[1]

    def get_secondary_address(self):
        return self.secondary_address

    # initializes self.ss (usocket.socket object), secondary_address nullable
    def connect_to_secondary(self, secondary_address=None) -> None:
        # print('Connecting to secondary... ', end="")
        from utime import sleep
        if(secondary_address == None):
            rootHost = self.rootUrl.split(':')[0]
            # rootPort = int(self.rootUrl.split(':')[1])
            rootPort = 64
            # print('Finding secondary...')
            sleep(1)
            self.secondary_address = self.find_secondary(self.atSign, rootHost, rootPort)
            sleep(2)
        else:
            self.secondary_address = secondary_address

        ss_split = self.secondary_address.split(":")
        if len(ss_split) != 2:
            raise Exception("Invalid secondary address: " + self.secondary_address)
        print(ss_split)
        address = ss_split[0]
        port = ss_split[1]
        del ss_split

        sleep(1)
        from usocket import getaddrinfo, socket, AF_INET, SOCK_STREAM
        a = getaddrinfo(address, int(port))[0][-1]
        s = socket(AF_INET, SOCK_STREAM) 
        del getaddrinfo, socket, AF_INET, SOCK_STREAM

        sleep(1)
        try:
            s.connect(a)
        except OSError as e:
            if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e
        
        sleep(1)
        del sleep
        s.setblocking(False)
        from ussl import wrap_socket
        ss = wrap_socket(s, do_handshake = True)
        del wrap_socket
        self.ss = ss
        
    # returns the secondary address (as a string) of a given atSign, rootHost, and rootPort
    def find_secondary(self, atSign: str, rootHost: str = 'root.atsign.org', rootPort: int = 64) -> str:
        from lib.at_client.at_utils import without_prefix
        atSign = without_prefix(atSign)
        del without_prefix
        # print('Finding secondary for @' + atSign + '...')
        from usocket import getaddrinfo, socket, AF_INET, SOCK_STREAM
        a = getaddrinfo(rootHost, rootPort)[0][-1]
        s = socket(AF_INET, SOCK_STREAM) 
        del getaddrinfo, socket, AF_INET, SOCK_STREAM

        try:
            s.connect(a)
        except OSError as e:
            if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e
            
        from utime import sleep
        s.setblocking(False)
        sleep(1)
        from ussl import wrap_socket
        ss = wrap_socket(s, do_handshake = True)
        del wrap_socket
        sleep(1)

        ss.write((atSign + "\r\n").encode())
        sleep(1)

        response = b''
        data = ss.read()
        sleep(1)
        del sleep
        response += data
        secondary = response.decode().replace('@', '')
        secondary = secondary.replace('\r\n', '')
    
        ss.close()
        # print('Address found: %s' % secondary)
        return secondary
    