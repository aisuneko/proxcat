# proxcat
A htop-like status monitor for Proxmox VE servers, powered by python curses, with support for multiple nodes, VM (QEMU) and Container (LXC) status and node status.

## Installation
Install dependencies: `pip install proxmoxer`

Or, clone repository and run `pip install .`. 

## Usage
1. On your PVE server, create an API token in WebUI under Datacenter -> Permissions -> API Tokens. Remember to deselect "Priviledge Separation" (for this reason, it is recommended to use the app with a dedicated low-level user instead of root).
2. Create a config file. The app will look for `config.ini` under
    - `$XDG_CONFIG_HOME/proxcat/` or
    - `~/.proxcat/`

    Or, you can specify a custom config file with the `-c` / `--config` flag.

    Then fill in the config file like this:
   ```ini
   [Account]
   # address of PVE host
   Host = 
   # Username (format: <username>@<realm>)
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

