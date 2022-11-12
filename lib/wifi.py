import network

# Returns network.WLAN object
def init_wlan(ssid: str, password: str):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    return wlan