import network # type: ignore
import time
from ntp_client import sync_time, format_time_string, format_time_id
import usocket as socket # type: ignore
import ussl as ssl # type: ignore
import sys
import machine
import ujson

ssid = password = atSign = ''

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def main():
    
    ssid, password, atSign = read_settings()

    wlan = network.WLAN(network.STA_IF)  # type: ignore
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected() and wlan.status() >= 0:
        time.sleep(1)
        print("Wi-Fi .. Connecting")

    print ("Wi-Fi Connected")

    sync_time()
    
    while True:
        print("Welcome! What would you like to do?\n\t1) REPL\n\t2) Temperature sensor menu\n\t3) Exit")
        opt= input("> ")
        
        if int(opt) == 1:
            secondary = find_secondary(atSign)
            ss = connect_to_secondary(secondary)

            print('Connected\n')
            command = '@'
            while True:
                verb = str(input(command))
                response, command = send_verb(ss, verb)
                print(response)
                if('error:AT' in response): 
                    ss.close()
                    sys.exit(1)
        elif int(opt) == 2:
            while True:
                print("Temperature sensor menu\n\t1) See current temperature\n\t2) Record current temperature\n\t3) Exit")
                tmp = input("> ")
                if int(tmp) == 1:
                    print("--------------------\n")
                    print(format_time_string() + "\nTemperature: " + str(measure_temp()))
                    print("\n--------------------")
                elif int(tmp) == 2:
                    tm = str(measure_temp())
                    verb = "update:" + str(format_time_id()) + ".temperature@" + atSign + " " + tm
                    secondary = find_secondary(atSign)
                    ts = connect_to_secondary(secondary)
                    print('Connected\n')
                    response, command = send_verb(ts, 'from:' + atSign)
                    print(response)
                    pkam = str(input(command))
                    response, command = send_verb(ts, pkam)
                    print(response)
                    if('success' in response): 
                        send_verb(ts, verb)
                        print("Current temperature measurement has been recorded:\n" + verb.replace('update:', '') + '\n')
                    else:
                        print('Could not record temperature: Wrong pkam')
                    ts.close()
                elif int(tmp) == 3:
                    break
                else:
                    print('Invalid option. Please enter a number in the range [1-3]')
        elif int(opt) == 3:
            sys.exit(1)
        else:
            print('Invalid option. Please enter a number in the range [1-3]')

    
def send_verb(skt, verb):
    skt.write((verb + "\r\n").encode())
    time.sleep(1)
    response = b''
    data = skt.read()
    response += data
    parts = response.decode().split('\n')
    return parts[0], parts[1]
    
def measure_temp():
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

def read_settings():
    with open('settings.json') as f:
        info = ujson.loads(f.read())
        return info['ssid'], info['password'], info['atSign']

def connect_to_secondary(secondary):
    print('Connecting to secondary... ', end="")

    secondary = secondary.split(':')
    address = secondary[0]
    port = secondary[1]

    a = socket.getaddrinfo(address, int(port))[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        s.connect(a)
    except OSError as e:
        if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
            print("In Progress")
        else:
            raise e
        
    s.setblocking(False)
    ss = ssl.wrap_socket(s, do_handshake = True)
    return ss
    
def find_secondary(atSign):
    print('Finding secondary for @' + atSign + '...')
    a = socket.getaddrinfo('root.atsign.org', 64)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        s.connect(a)
    except OSError as e:
        if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
            print("In Progress")
        else:
            raise e
        
    s.setblocking(False)
    ss = ssl.wrap_socket(s, do_handshake = True)

    ss.write((atSign + "\r\n").encode())
    time.sleep(1)

    response = b''
    data = ss.read()
    response += data
    secondary = response.decode().replace('@', '')
    secondary = secondary.replace('\r\n', '')
 
    ss.close()
    print('Address found: %s' % secondary)
    return secondary

if __name__ == '__main__':
    main()
