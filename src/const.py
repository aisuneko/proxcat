import os
conf_dir = os.path.join(os.environ["XDG_CONFIG_HOME"], "proxcat") if (
    "XDG_CONFIG_HOME" in os.environ) else os.path.join(os.path.expanduser("~"), ".proxcat")
config_path = os.path.join(conf_dir, "config.ini")

norm_status_bar_strs = ["TYPE", "VMID", "NAME", "STATUS", "%CPU",
                        "MEM", "%MEM", "DISK", "%DISK", "SWAP", "%SWAP", "UPTIME"]
qemu_status_bar_strs = ["TYPE", "VMID", "NAME", "STATUS", "%CPU",
                        "MEM", "%MEM", "DISK", "UPTIME"]
