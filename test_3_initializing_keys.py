

def main():
    # Ensure that you have your keys ("@alice_key.atKeys") inside of the "keys" folder.
    # Add it now if you have not already.

    from lib.at_client.io_util import read_settings
    s, p, atSign = read_settings()
    del read_settings, s, p
    
    from lib.at_client.keys_util import initialize_keys
    initialize_keys(atSign)
    del initialize_keys

if __name__ == '__main__':
    main()