

def main():
    """
    Sample output

    >>> Connecting to Soup (Ctrl+C to stop)...
    >>> Connected to WiFi Soup: True
    """
    from lib.at_client.io_util import read_settings
    from lib.wifi import init_wlan

    # Add your SSID an Password in `settings.json`
    ssid, password, atSign = read_settings()
    del atSign, read_settings # atSign not needed in memory right now

    print('\nConnecting to %s (Ctrl+C to stop)...' % ssid)
    wlan = init_wlan(ssid, password)
    del init_wlan

    if not wlan == None:
        print('Connected to WiFi %s: %s' %(ssid, str(wlan.isconnected())))
    else:
        print('Failed to connect to \'%s\'... :(' %ssid)

if __name__ == '__main__':
    main()