

def main():
    # Ensure that you have your keys ("@alice_key.atKeys") inside of the "keys" folder.
    # Add it now if you have not already.

    from lib.at_client import io_util
    from lib.at_client import keys_util

    s, p, atSign = io_util.read_settings()
    del s, p
    
    keys_util.initialize_keys(atSign)
    pass

if __name__ == '__main__':
    main()