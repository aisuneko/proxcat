import curses
from proxmoxer import ProxmoxAPI

from . import frontend
from . import utils


def start():
    config, no_lxc = utils.startup()
    account = config['Account']
    settings = config['Settings']
    instance = ProxmoxAPI(account['Host'], user=account['User'], token_name=account['TokenName'],
                          token_value=account['Token'], verify_ssl=False)
    interval = int(settings['UpdateInterval']
                   ) if settings['UpdateInterval'] else 1000
    curses.wrapper(frontend.draw, instance, interval, no_lxc)
