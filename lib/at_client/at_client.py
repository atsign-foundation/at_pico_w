


class AtClient:

    def __init__(self, atSign: str, rootUrl: str = 'root.atsign.org:64', writeKeys:bool=True, secondary_address=None):
        from lib.at_client.at_utils import format_atSign
        self.atSign = format_atSign(atSign)
        del format_atSign
        self.rootUrl = rootUrl
        if writeKeys:
            self._initialize_keys()
        self._initialize_remote_secondary(secondary_address)

    def _initialize_keys(self):
        """
        write pem parameters in the keys/@atSign/ folder
        reads from keys/@atSign_key.atKeys file and converts to pem parameters
        
        """
        from lib.at_client.keys_util import initialize_keys
        initialize_keys(self.atSign)
        del initialize_keys

    def _initialize_remote_secondary(self, secondary_address=None):
        """
        intializes remote secondary object and connects to secondary allowing for send_verb to work
        Assume already connected to WiFi. See lib.wifi for more info.
        """
        from lib.at_client.remote_secondary import RemoteSecondary
        self.remote_secondary = RemoteSecondary(self.atSign, self.rootUrl)
        del RemoteSecondary
        self.remote_secondary.connect_to_secondary(secondary_address=secondary_address) # can now run send_verb


    # Not working due to RSA decryption
    # def _get_shared_key_from_other(self, otherAtSign: str):
    #     """
    #     otherAtSign: the atsign of the other person that is sharing data with you.

    #     does lookup:shared_key@otherAtSign and decrypts the response with your encrypt private key to get the
    #     shared aes 256 encryption key
    #     """
    #     from lib.at_client.at_utils import format_atSign
    #     # get the AES shared key from the other person
    #     command = 'lookup:shared_key%s' %format_atSign(otherAtSign) # lookup:shared_key@bob
    #     del format_atSign

    #     # run command
    #     response, command = self.send_verb(command)
    #     response = response.replace('data:', '')
    #     del command

    #     print('response: %s' % response)

    #     # decrypt with my encrypt private key
    #     from lib.at_client.keys_util import get_pem_encrypt_private_key_from_file
    #     encryptPrivateKey = get_pem_encrypt_private_key_from_file(self.atSign)
    #     del get_pem_encrypt_private_key_from_file

    #     # construct rsa private key
    #     from lib.third_party import rsa
    #     rsaPrivateKey = rsa.PrivateKey(encryptPrivateKey[0], encryptPrivateKey[1], encryptPrivateKey[2], encryptPrivateKey[3], encryptPrivateKey[4])
    #     del encryptPrivateKey

    #     # get the encrypted aes shared key
    #     verb = 'lookup:shared_key%s' %otherAtSign
    #     response, command = self.send_verb(verb)
    #     response = response.replace('data:', '')
    #     del command
    #     print(response)

    #     # decrypt the encrypted aes shared key with our rsaPrivateKey
    #     someData = rsa.decrypt(response, rsaPrivateKey)
    #     print(someData)
    #     import ubinascii
    #     shared_aes_key = str(ubinascii.b2a_base64(someData)).rstrip('\n')
    #     return shared_aes_key

    def send_verb(self, verb_command: str):
        """
        Returns a Tuple (response, command)

        response: the response from the secondary
        command: the command that was sent to the secondary
        """
        if self.remote_secondary is None:
            raise Exception("Remote secondary is not initialized. Please call _initialize_remote_secondary() first.")
        return self.remote_secondary.send_verb(verb_command) # returns (response, command)

    # TODO ADD VERBOSE OPTION
    def put_public(self, keyName: str, value: str, ttr:int = 1000, namespace=None) -> str:
        """
        keyName: the key name
        value: the value to put
        ttr: time to refresh the public key, default 1 second
        ttr == -1 means permanent cache the key
        ttr == 0 means do not cache the key
        ttr > 0 means refresh after ttr milliseconds

        return: response from the secondary
        """
        del ttr # TODO: implement ttr
        
        from lib.at_client.at_utils import format_atSign
        fullKeyName = keyName
        if not namespace == None:
            fullKeyName = keyName + '.' + namespace
        verb = 'update:public:%s%s %s' %(fullKeyName, format_atSign(self.atSign), value)
        del format_atSign, fullKeyName
        from utime import sleep
        sleep(1)
        print('sending verb: %s' % verb)
        response, command = self.send_verb(verb)
        sleep(1)
        del command, sleep
        response = response.replace('data:', '')
        return response

    def get_public(self, keyName: str, otherAtSign:str, namespace=None) -> str:
        """
        """
        from lib.at_client.at_utils import format_atSign
        otherAtSign = format_atSign(otherAtSign)
        del format_atSign
        from utime import sleep

        # get the public key
        fullKeyName = keyName
        if not namespace == None:
            fullKeyName = keyName + '.' + namespace
        verb = 'plookup:bypassCache:true:%s%s' %(fullKeyName, otherAtSign)
        del fullKeyName
        sleep(1)
        # print('Executing verb %s' %verb)
        response, command = self.send_verb(verb)
        del command
        sleep(1)

        response = response.replace('data:', '')
        return response

    def pkam_authenticate(self, verbose = False) -> None:
        """
        to run this function, you must have your .atKeys file in the keys/ folder and _initialize_keys() must be called first (which is already done in the constructor)
        """
        atSign = self.atSign
        from lib.at_client.at_utils import without_prefix
        atSignWithoutPrefix = without_prefix(atSign)

        if verbose:
            print('Sending from:%s' % atSign)
        response, command = self.remote_secondary.send_verb('from:%s' %atSignWithoutPrefix)
        del command, atSignWithoutPrefix
        challenge = response.replace('@data:', '')
        del response
        if verbose:
            print('Challenge: %s' % challenge)
            print('Digesting...')

        from lib.at_client.keys_util import get_pem_pkam_private_key_from_file
        pemPkamPrivateKey = get_pem_pkam_private_key_from_file(atSign) # parameters
        del get_pem_pkam_private_key_from_file

        from lib.third_party.rsa import PrivateKey, sign
        rsaPkamPrivateKey = PrivateKey(pemPkamPrivateKey[0], pemPkamPrivateKey[1], pemPkamPrivateKey[2], pemPkamPrivateKey[3], pemPkamPrivateKey[4])
        del pemPkamPrivateKey, atSign

        from lib.pem_service import b42_urlsafe_encode
        signature = b42_urlsafe_encode(sign(challenge, rsaPkamPrivateKey, 'SHA-256'))
        del b42_urlsafe_encode, challenge, rsaPkamPrivateKey

        if verbose:
            print('Signature: %s' % str(signature))
        response, command = self.remote_secondary.send_verb('pkam:' + signature)
        del command

        if verbose:
            print(response) # data:success

        del signature
