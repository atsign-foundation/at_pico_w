

def main():
    import sys
    shouldRun = str(input('Run? (y/n): ')).lower()
    if shouldRun != 'y':
        sys.exit(1)
    del sys

    from lib.at_client import io_util
    from lib import wifi
    from lib.at_client import at_client
    ssid, password, atSign = io_util.read_settings()
    del io_util

    print('Connecting to WiFi %s...' % ssid)
    wifi.init_wlan(ssid, password)
    del ssid, password, wifi

    atClient = at_client.AtClient(atSign)
    atClient.pkam_authenticate(verbose=True)

if __name__ == '__main__':
    main()
