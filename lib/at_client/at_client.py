


class AtClient:

    def __init__(self, atSign: str, rootUrl: str = 'root.atsign.org:64'):
        self.atSign = atSign
        self.rootUrl = rootUrl
        self._initialize_keys() 
        self._initialize_remote_secondary()

    def _initialize_remote_secondary(self):
        """
        intializes remote secondary object and connects to secondary allowing for send_verb to work
        Assume already connected to WiFi. See lib.wifi for more info.
        """
        from lib.at_client.remote_secondary import RemoteSecondary
        self.remote_secondary = RemoteSecondary(self.atSign, self.rootUrl)
        self.remote_secondary.connect_to_secondary() # can now run send_verb

    def _initialize_keys(self):
        """
        write pem parameters in the keys/@atSign/ folder
        reads from keys/@atSign_key.atKeys file and converts to pem parameters
        
        """
        from lib.at_client.keys_util import initialize_keys
        initialize_keys(self.atSign)

    def send_verb(self, verb_command: str):
        """
        Returns a Tuple (response, command)

        response: the response from the secondary
        command: the command that was sent to the secondary
        """
        if self.remote_secondary is None:
            raise Exception("Remote secondary is not initialized. Please call _initialize_remote_secondary() first.")
        return self.remote_secondary.send_verb(verb_command) # returns (response, command)

    def pkam_authenticate(self, verbose = False):
        """
        to run this function, you must have your .atKeys file in the keys/ folder and _initialize_keys() must be called first (which is already done in the constructor)
        """
        from lib.at_client.at_utils import without_prefix
        from lib.at_client import keys_util
        from lib.third_party import rsa
        from lib.pem_service import b42_urlsafe_encode

        atSign = self.atSign
        atSignWithoutPrefix = without_prefix(atSign)

        print('Sending from:%s' % atSign)
        response, command = self.remote_secondary.send_verb('from:%s' %atSignWithoutPrefix)
        challenge = response.replace('@data:', '')
        print('Challenge: %s' % challenge)
        print('Digesting...')
        pemPkamPrivateKey = keys_util.get_pem_pkam_private_key_from_file(atSign) # parameters
        rsaPkamPrivateKey = rsa.PrivateKey(pemPkamPrivateKey[0], pemPkamPrivateKey[1], pemPkamPrivateKey[2], pemPkamPrivateKey[3], pemPkamPrivateKey[4])
        signature = b42_urlsafe_encode(rsa.sign(challenge, rsaPkamPrivateKey, 'SHA-256'))
        print('Signature: %s' % str(signature))
        response, command = self.remote_secondary.send_verb('pkam:' + signature)
        print(response) # data:success

        del signature, challenge, rsaPkamPrivateKey, pemPkamPrivateKey
        pass