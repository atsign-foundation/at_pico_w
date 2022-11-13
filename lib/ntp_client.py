# ntp, network time protocol client

import time
import usocket as socket # type: ignore
import struct
import machine

# Substract 1 hour, so we get + 1 hour
TIMESTAMP_DELTA = 2208988800 - 3600*1 # epoch time - 1 hour
NTP_QUERY = b'\x1b' + 47 * b'\0'

def sync_time():
    
    a = socket.getaddrinfo('pool.ntp.org', 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP can only be used with SOCK_DGRAM

    try:
        s.connect(a)
    except OSError as e:
        if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
            print("In Progress")
        else:
            raise e
    
    s.sendto(NTP_QUERY, a)
    data = s.recv(48)
    s.close()
    
    t = struct.unpack("!I", data[40:44])[0] # Transmit Timestamp field of the NTP packet header
    t -= TIMESTAMP_DELTA
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print(format_time_string())
    
def format_time_string():
    t = time.localtime()
    s = str("Current time: " + get_week_day(t[6]) + ", " + str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + ", " + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]))
    return s
    
def format_time_id():
    return time.time()

def get_week_day(day):
    d = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return d[day]

    
    
    
    
    
    
    
