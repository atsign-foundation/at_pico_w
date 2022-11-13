

def main():
    import sys
    shouldRun = str(input('Run? (y/n): '))
    if shouldRun == 'n':
        sys.exit(1)

    from lib.at_client import keys_util
    from lib.at_client import io_util
    from lib.at_client import remote_secondary
    from lib import wifi
    from lib.third_party import rsa
    from lib.at_client.at_utils import without_prefix
    ssid, password, atSign = io_util.read_settings()
    keys_util.initialize_keys(atSign) # initialize /keys/@{your_atSign}/ containing _pem.json keys extracted from /keys/@fascinatingsnow_key.atKeys, you really only need to run this once per atSign

    atSignWithoutPrefix = without_prefix(atSign)
    rootUrl = 'root.atsign.org:64'

    print('Connecting to WiFi %s...' % ssid)
    wlan = wifi.init_wlan(ssid, password)

    remote_secondary = remote_secondary.RemoteSecondary(rootUrl, atSign, wlan)
    print('Connecting to remote secondary of atSign @%s...' % atSignWithoutPrefix)
    remote_secondary.connect_to_secondary()
    print('Connected to secondary of atSign @%s with address %s' %(atSignWithoutPrefix, str(remote_secondary.get_secondary_address())))
    if remote_secondary.is_connected():
        print('Sending from:%s' % atSign)
        response, command = remote_secondary.send_verb('from:%s' %atSignWithoutPrefix)
        challenge = response.replace('@data:', '')
        print('Challenge: %s' % challenge)
        print('Digesting...')
        pemPkamPrivateKey = keys_util.get_pem_pkam_private_key_from_file(atSign) # parameters
        rsaPkamPrivateKey = rsa.PrivateKey(pemPkamPrivateKey[0], pemPkamPrivateKey[1], pemPkamPrivateKey[2], pemPkamPrivateKey[3], pemPkamPrivateKey[4])
        signature = b42_urlsafe_encode(rsa.sign(challenge, rsaPkamPrivateKey, 'SHA-256'))
        print('Signature: %s' % str(signature))
        response, command = remote_secondary.send_verb('pkam:' + signature)
        print(response) # data:success

        del signature, challenge, rsaPkamPrivateKey, pemPkamPrivateKey, ssid, password
        sys.exit(1)
        
def b42_urlsafe_encode(payload):
    from lib.third_party import string
    from ubinascii import b2a_base64
    return string.translate(b2a_base64(payload)[:-1].decode('utf-8'),{ ord('+'):'-', ord('/'):'_' })

if __name__ == '__main__':
    main()