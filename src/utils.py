import math
import os
import curses
from functools import wraps
import configparser
import argparse
from .const import config_path
from . import __version__ as version


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


def startup():
    parser = argparse.ArgumentParser(
        description="local htop-like monitor for remote Proxmox VE servers")
    parser.add_argument(
        "-c", "--config", help="Specify location of config file", type=str)
    parser.add_argument("-v", "--version",
                        help="Show version and exit", action="store_true")
    parser.add_argument("-l", "--no-lxc-only-info",
                        help="Disable LXC-only info", action="store_true")
    args = parser.parse_args()
    if args.version:
        print(f"v{version}")
        exit(0)
    config = configparser.ConfigParser()
    path = os.path.expanduser(args.d) if args.config else config_path
    no_lxc = True if args.no_lxc_only_info else False
    config.read(path)
    return config, no_lxc
