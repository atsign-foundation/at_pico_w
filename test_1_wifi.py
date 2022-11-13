

def main():
    """
    Sample output

    >>> Connecting to Soup (Ctrl+C to stop)...
    >>> Connected to WiFi Soup: True
    """
    from lib.at_client import io_util
    from lib import wifi

    # Add your SSID an Password in `settings.json`
    ssid, password, atSign = io_util.read_settings()
    del atSign # atSign not needed in memory right now

    print('\nConnecting to %s (Ctrl+C to stop)...' % ssid)
    wlan = wifi.init_wlan(ssid, password)

    if not wlan == None:
        print('Connected to WiFi %s: %s' %(ssid, str(wlan.isconnected())))
    else:
        print('Failed to connect to \'%s\'... :(' %ssid)

if __name__ == '__main__':
    main()