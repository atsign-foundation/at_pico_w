

def main():
    """

    Finds the secondary address of `atSign` from settings.json. Ensure `SSID` AND `password` are correct in settings.json.

    Sample output

    >>> Connecting to Soup (Ctrl+C to stop)...
    >>> Connecting to remote secondary of atSign @fascinatingsnow...
    >>> Connected to secondary of atSign @fascinatingsnow with address 6fe57327-01c1-5bbc-8a3c-3af1df169545.swarm0002.atsign.zone:5004
    """

    # get values
    from lib.at_client.io_util import read_settings
    ssid, password, atSign = read_settings()
    del read_settings

    # connect to internet
    print('\nConnecting to %s (Ctrl+C to stop)...' % ssid)
    from lib.wifi import init_wlan
    wlan = init_wlan(ssid, password)
    del init_wlan
    print('Connected: %s' %str(not wlan == None))

    # initialize RemtoeSecondary object
    from lib.at_client.remote_secondary import RemoteSecondary
    rs = RemoteSecondary(atSign,  wlan=wlan)
    del RemoteSecondary

    # find secondary address
    print('Connecting to remote secondary of atSign @%s...' % atSign)
    ss_address = rs.find_secondary(atSign)
    print('Connected to secondary of atSign @%s with address %s' %(atSign, ss_address))

if __name__ == '__main__':
    main()

