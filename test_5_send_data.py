

def main():
    import sys
    shouldRun = str(input('Run? (y/n): '))
    if shouldRun == 'n':
        sys.exit(1)
    del sys # make space in memory

    from lib.at_client import io_util
    from lib import wifi
    from lib.at_client import at_client
    ssid, password, atSign = io_util.read_settings()
    del io_util # make space in memory

    print('Connecting to WiFi %s...' % ssid)
    wifi.init_wlan(ssid, password)
    del ssid, password, wifi # make space in memory

    atClient = at_client.AtClient(atSign)
    atClient.pkam_authenticate()

    from lib.at_client import at_utils
    atSign = at_utils.format_atSign(atSign)
    del at_utils
    sharedWith = '@smoothalligator'
    key = '%s:led%s' %(sharedWith, atSign) # @smoothalligator:led@fascinatingsnow

    import machine
    import time
    led = machine.Pin(0, machine.Pin.OUT)
    del machine
    value = 0
    for i in range(100):
        time.sleep(5)
        
        # actuate the LED accordingly
        if value == 0:
            led.off()
        elif value == 1:
            led.on()
        print('LED: %s' %value)

        # emit the data
        verb = 'update:%s %s' %(key, value)
        print('Running verb: %s' %verb)
        response, command = atClient.send_verb(verb)
        del command
        print(response)

        # update the value
        if value == 0:
            value = 1
        elif value == 1:
            value = 0
        
        

        
        

if __name__ == '__main__':
    main()