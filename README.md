# proxcat
A htop-like status monitor for Proxmox VE servers, powered by python curses, with support for multiple nodes, VM (QEMU) and Container (LXC) status and node status.

## Screenshot
![connected to my own PVE server](screenshot.jpg)
## Installation
`pip install requests proxmoxer proxcat`

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
   UpdateInterval = 1000
   ```
3. run the `proxcat` command.

## Changelog
see [CHANGELOG.md](CHANGELOG.md).

## Todo
- [ ] Switch entirely to `pyproject.toml`
- [ ] More functionality for curses UI (custom sorting, ...)
- [ ] Invoke VM/CT jobs within app
- [ ] **Optional headless/daemon mode with WebUI**

## License
[MIT](LICENSE)