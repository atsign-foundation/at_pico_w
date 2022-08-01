import network # type: ignore
import time
import usocket as socket # type: ignore
import struct
import machine

# Substract 2 hours, so we get + 2 hours
t_delta = 2208988800 - 3600*2 # epoch time - 2 hours
# 1/1/1970 (Unix) vs 1/1/1900 (TIME protocol)
# We are gonna be given time since 1/1/1900, which is 70 years larger than Unix (system)

# Simple TIME protocol client: https://datatracker.ietf.org/doc/html/rfc868
def sync_time():
    
    # unused, but simpler than 123 (NTP), useful until 2036
    a = socket.getaddrinfo('time-a.timefreq.bldrdoc.gov', 37)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        s.connect(a)
    except OSError as e:
        if str(e) == '119': # For non-Blocking sockets 119 is EINPROGRESS
            print("In Progress")
        else:
            raise e
    
    data = s.read()
    t = struct.unpack("!I", data)[0]
    t -= t_delta
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print(format_time_string())
    s.close()
    
def format_time_string():
    t = time.localtime()
    s = str("Current time: " + get_week_day(t[6]) + ", " + str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + ", " + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5]))
    return s
    
def format_time_id():
    return time.time()

def get_week_day(day):
    d = ''
    if(day == 0):
        d = 'Monday'
    elif(day == 1):
        d = 'Tuesday'
    elif(day == 2):
        d = 'Wednesday'
    elif(day == 3):
        d = 'Thursday'
    elif(day == 4):
        d = 'Friday'
    elif(day == 5):
        d = 'Saturday'
    elif(day == 6):
        d = 'Sunday'
    return d

    
    
    
    
    
    
    