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
    show_sensors = utils.parse_boolean_config_value(config, 'Settings', 'ShowSensors')
    curses.wrapper(frontend.draw, instance, interval, show_sensors, no_lxc)
