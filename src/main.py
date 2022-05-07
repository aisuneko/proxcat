import curses
import os
import configparser
from proxmoxer import ProxmoxAPI
import argparse

from . import frontend
from . import utils
from . import __version__ as version


def start():
    config = configparser.ConfigParser()
    parser = argparse.ArgumentParser(
        description="local htop-like monitor for remote Proxmox VE servers")
    parser.add_argument(
        "-c", "--config", help="Specify location of config file", type=str)
    parser.add_argument("-v", "--version",
                        help="Show version and exit", action="store_true")
    parser.add_argument("-l", "--no-lxc-only-info",
                        help="Disable LXC-only info", action="store_true")
    args = parser.parse_args()
    path = utils.config_path
    if args.version:
        print(f"v{version}")
        return
    if args.config:
        path = os.path.expanduser(args.d)
    no_lxc = False
    if args.no_lxc_only_info:
        no_lxc = True
    config.read(path)

    account = config['Account']
    settings = config['Settings']
    instance = ProxmoxAPI(account['Host'], user=account['User'], token_name=account['TokenName'],
                          token_value=account['Token'], verify_ssl=False)
    interval = int(settings['UpdateInterval']
                   ) if settings['UpdateInterval'] else 1000
    curses.wrapper(frontend.draw, instance, interval, no_lxc)


if __name__ == "__main__":
    start()
