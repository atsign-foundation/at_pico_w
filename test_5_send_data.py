
def main():
    import sys
    shouldRun = str(input('Run? (y/n): ')).lower()
    if shouldRun != 'y':
        sys.exit(1)
    del sys # make space in memory

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

    value = 0
    from machine import Pin
    from utime import sleep
    led = Pin("LED", Pin.OUT)
    for i in range(100):
        sleep(5)
        # actuate the onboard LED
        if value == 0:
            led.off()
        elif value == 1:
            led.on()

        # emit the data
        sleep(2)
        data = atClient.put_public('led', str(value)) # update:public:led@soccer0 0
        sleep(2)

        print('response: data:%s' %data)

        # change
        if value == 0:
            value = 1
        elif value == 1:
            value = 0
        
if __name__ == '__main__':
    main()