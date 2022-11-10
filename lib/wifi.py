import network

# Returns network.WLAN object
def init_wlan(ssid: str, password: str):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('\nConnecting to %s...' % ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('Connected to WiFi %s: %s' %(ssid, str(wlan.isconnected())))
    return wlan