
def main():
    import sys
    shouldRun = str(input('Run? (y/n): ')).lower()
    if shouldRun != 'y':
        sys.exit(1)
    del sys # make space in memory

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

    import time
    value = 0

    import machine
    led = machine.Pin("LED", machine.Pin.OUT)
    for i in range(100):
        time.sleep(5)
        # actuate the onboard LED
        if value == 0:
            led.off()
        elif value == 1:
            led.on()

        # emit the data
        time.sleep(2)
        data = atClient.put_public('led', str(value)) # update:public:led@soccer0 0
        time.sleep(2)

        print('response: data:%s' %data)

        # change
        if value == 0:
            value = 1
        elif value == 1:
            value = 0
        
if __name__ == '__main__':
    main()