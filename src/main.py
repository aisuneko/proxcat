import curses
from proxmoxer import ProxmoxAPI

from . import frontend
from . import utils


def start():
    config, no_lxc, interval, show_sensors = utils.startup()
    account = config['Account']
    settings = config['Settings']
#    verify_ssl = utils.parse_boolean_config_value(config, 'Account', 'VerifySSL')
    verify_ssl = False  # todo
    instance = ProxmoxAPI(account['Host'], user=account['User'], token_name=account['TokenName'],
                          token_value=account['Token'], verify_ssl=verify_ssl)
    interval = interval if interval else (int(settings['UpdateInterval']
                                              ) if settings['UpdateInterval'] else 1000)
    show_sensors = show_sensors if show_sensors else (
        utils.parse_boolean_config_value(config, 'Settings', 'ShowSensors'))
    if show_sensors and (account['Host'] != '127.0.0.1'):
        raise utils.SensorsInitError(
            "It seems that proxcat isn't run on the host itself, thus the CPU temperature info might be wrong. If it does, please change the Host parameter in config to '127.0.0.1' or 'localhost'.")
    curses.wrapper(frontend.draw, instance, interval, show_sensors, no_lxc)
