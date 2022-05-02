import math
import os
import curses
from functools import wraps

conf_dir = os.path.join(os.path.expanduser("~"), ".proxcat")
if "XDG_CONFIG_HOME" in os.environ:
    conf_dir = os.path.join(os.environ["XDG_CONFIG_HOME"], "proxcat")

config_path = os.path.join(conf_dir, "config.ini")


def convert_size(size_bytes):  # convert from bytes to other units
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def handle(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except curses.error:
            pass
    return decorated
