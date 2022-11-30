# ntp, network time protocol client

# Substract 1 hour, so we get + 1 hour
TIMESTAMP_DELTA = 2208988800 - 3600*1 # epoch time - 1 hour
NTP_QUERY = b'\x1b' + 47 * b'\0'

def sync_time():
    from usocket import getaddrinfo, socket, AF_INET, SOCK_DGRAM
    a = getaddrinfo('pool.ntp.org', 123)[0][-1]
    s = socket(AF_INET, SOCK_DGRAM) # UDP can only be used with SOCK_DGRAM

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
    from struct import unpack
    t = unpack("!I", data[40:44])[0] # Transmit Timestamp field of the NTP packet header
    t -= TIMESTAMP_DELTA
    from utime import gmtime
    tm = gmtime(t)
    import machine
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print(format_time_string())
    
def format_time_string():
    from utime import localtime
    t = localtime()
    s = str("Current time: " + get_week_day(t[6]) + ", " + str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + ", " + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]))
    return s
    
def format_time_id():
    from utime import time
    return time()

def get_week_day(day):
    d = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return d[day]

    
    
    
    
    
    
    
