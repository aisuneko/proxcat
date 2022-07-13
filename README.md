# proxcat
A htop-like status monitor for Proxmox VE servers, powered by python curses, with support for multiple nodes, VM (QEMU) and Container (LXC) status and node status.

## Screenshot
![connected to my own PVE server](screenshot.jpg)
## Installation
`pip install requests proxmoxer proxcat`
(optional) `pip install PySensors` for CPU temperature info support (only when ran directly on PVE host)

Or, clone repository and run `pip install .`. 

## Usage
1. On your PVE server, create an API token in WebUI under Datacenter -> Permissions -> API Tokens. Remember to deselect "Priviledge Separation". For security concerns, it is recommended to use it with a dedicated low-level user - for example, one with the "PVEAuditor" role assigned - instead of root or other administrators.
2. Create a config file. `proxcat` will look for `config.ini` under
    - `$XDG_CONFIG_HOME/proxcat/` or
    - `~/.proxcat/`

    Or, you can specify a custom config file with the `-c` / `--config` flag.

    Then fill in the config file like this:
   ```ini
   [Account]
   # address of PVE host
   Host = 
   # Username (format: <username>@<realm)
   User = 
   # name of your token
   TokenName = 
   # your token value
   Token = 

   [Settings]
   # set data update interval (in ms), optional
   UpdateInterval = 
   # whether to enable host CPU temperature info (requires lm_sensors and PySensors). Disabled by default.
   ShowSensors = False
   ```
   The options in [Settings] can be overriden by command-line flags; see `-h` or `--help` for details.

3. run the `proxcat` command.
   > Keybindings:
   > 
   > `q` to quit
   > 
   > `n` `p` for switching between nodes
   > 
   > any other key for force refreshing screen
## Changelog
see [CHANGELOG.md](CHANGELOG.md).

## Todo
- [ ] Switch entirely to `pyproject.toml`
- [x] Add optional lm_sensors support for HW monitoring (if ran on host)
- [ ] Change time display to difference between host and local client
- [ ] More functionality for curses UI (custom sorting, ...)
- [ ] Invoke VM/CT jobs within app
- [ ] **Optional headless/daemon mode with WebUI**

## License
[MIT](LICENSE)
