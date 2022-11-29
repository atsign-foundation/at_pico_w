

def main():
    import sys
    shouldRun = input('Run (y/n): ')
    if(shouldRun != 'y'):
        sys.exit(1)
    del sys
    
    from lib.at_client.io_util import read_settings
    ssid, password, atSign = read_settings()
    del read_settings

    print('Connecting to WiFi %s...' % ssid)
    from lib.wifi import init_wlan
    init_wlan(ssid, password)
    del ssid, password, init_wlan

    from lib.at_client.at_client import AtClient
    atClient = AtClient(atSign)
    del AtClient
    atClient.pkam_authenticate(verbose=True)

    for i in range(5000):
        key = 'test'
        appAtSign = '@22easy'
        data = atClient.get_public(key, appAtSign)
        print(data)


if __name__ == '__main__':
    main()