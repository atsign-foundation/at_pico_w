# from https://github.com/micropython/micropython-lib/blob/master/logging/logging.py
import sys
import utime

CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERROR",
    WARNING: "WARN",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

_stream = sys.stderr

class LogRecord:
    def __init__(self):
        self.__dict__ = {}

    def __getattr__(self, key):
        return self.__dict__[key]

class Handler:
    def __init__(self):
        pass

    def setFormatter(self, fmtr):
        pass

class Logger:

    level = NOTSET
    handlers = []
    record = LogRecord()

    def __init__(self, name):
        self.name = name

    def _level_str(self, level):
        levelfromdict = _level_dict.get(level)
        if levelfromdict is not None:
            return levelfromdict
        return "LVL%s" % level

    def setLevel(self, level):
        self.level = level

    def isEnabledFor(self, level):
        return level >= (self.level or _level)

    def log(self, level, msg, *args):
        if self.isEnabledFor(level):
            levelname = self._level_str(level)
            if args:
                # accept both '%' formatted messages and '.format()' messages
                # in both cases avoid exceptions inside logs due to badly formatted log messages...
                try:
                    if msg.find('%s') >=0 or msg.find('%d') >=0 :
                        msg = msg % args
                    else:
                        msg = msg.format(*args)
                except Exception:
                    msg = msg + '--BAD LOG FORMAT--'
            if self.handlers:
                d = self.record.__dict__
                d["levelname"] = levelname
                d["levelno"] = level
                d["message"] = msg
                d["name"] = self.name
                for h in self.handlers:
                    h.emit(self.record)
            else:
                now = utime.ticks_ms()
                print(now, levelname, self.name, msg, sep="-", file=_stream)

    def debug(self, msg, *args):
        self.log(DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(INFO, msg, *args)

    def warning(self, msg, *args):
        self.log(WARNING, msg, *args)

    def error(self, msg, *args):
        self.log(ERROR, msg, *args)

    def critical(self, msg, *args):
        self.log(CRITICAL, msg, *args)

    def exc(self, e, msg, *args):
        self.log(ERROR, msg, *args)
        from uio import StringIO
        sio = StringIO()
        sys.print_exception(e, sio)
        sio.seek(0,0)
        self.log(ERROR, sio.read())
        sio.close()

    def exception(self, msg, *args):
        self.exc(sys.exc_info()[1], msg, *args)

    def addHandler(self, hndlr):
        self.handlers.append(hndlr)

_level = WARNING
_loggers = {}

def getLogger(name="root"):
    if name in _loggers:
        return _loggers[name]
    loggername = Logger(name)
    _loggers[name] = loggername
    return loggername

def exc(e, msg, *args):
    getLogger().exc(e, msg, *args)

def error(msg, *args):
    getLogger().error(msg, *args)

def warn(msg, *args):
    getLogger().warning(msg, *args)

def info(msg, *args):
    getLogger().info(msg, *args)

def debug(msg, *args):
    getLogger().debug(msg, *args)

def basicConfig(level=INFO, filename=None, stream=None, format=None):
    global _level, _stream
    _level = level
    if stream:
        _stream = stream
    if filename is not None:
        print("logging.basicConfig: filename arg is not supported")
    if format is not None:
        print("logging.basicConfig: format arg is not supported")
