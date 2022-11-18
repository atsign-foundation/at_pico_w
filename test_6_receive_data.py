

def main():
    import sys
    shouldRun = input('Run (y/n): ')
    if(shouldRun != 'y'):
        sys.exit(1)
    del sys

    # read settings.json
    from lib.at_client import io_util
    ssid, password, atSign = io_util.read_settings()
    del io_util # make space in memory

    # connect to wifi
    from lib import wifi
    print('Connecting to WiFi %s...' % ssid)
    wifi.init_wlan(ssid, password)
    del ssid, password, wifi # make space in memory

    # connect and pkam authenticate into secondary
    from lib.at_client import at_client
    atClient = at_client.AtClient(atSign, writeKeys=True)
    atClient.pkam_authenticate(verbose=True)
    del at_client

    for i in range(5000):
        key = 'instructions'
        appAtSign = '@smoothalligator'
        data = atClient.get_public(key, appAtSign)
        print(data)


if __name__ == '__main__':
    main()