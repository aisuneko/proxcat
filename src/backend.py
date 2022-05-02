import datetime
from .utils import convert_size


def build_node_info(instance, node):
    node_title = f"Node {node['node']} - {node['status']}"
    if node['status'] == "online":
        node_uptime = str(
            datetime.timedelta(seconds=node['uptime']))
        time_info = instance.nodes(node['node']).time.get()
        remote_time = datetime.datetime.utcfromtimestamp(
            int(time_info['localtime'])).strftime('%Y-%m-%d %H:%M:%S')
        node_title = node_title + \
            f" for {node_uptime} | Remote time {remote_time} ({time_info['timezone']})"
    cpu = f"CPU Usage: {node['cpu']:.2%} of {node['maxcpu']} CPUs"
    mem = f"Memory Usage: {node['mem']/node['maxmem']:.2%} | {convert_size(node['mem'])} of {convert_size(node['maxmem'])}"
    disk = f"Bootdisk Usage: {node['disk']/node['maxdisk']:.2%} | {convert_size(node['disk'])} of {convert_size(node['maxdisk'])}"
    return [node_title, cpu, mem, disk]


def build_vm_list(instance, node):
    vm_list = instance.nodes(node['node']).qemu.get(
    ) + instance.nodes(node['node']).lxc.get()
    vm_list.sort(key=lambda d: int(d['vmid']))
    return vm_list


def build_single_vm_info(vm):
    identifier = "lxc" if (
        'type' in vm and vm['type'] == "lxc") else "qemu"
    if vm['status'] == "running":
        status_bar_item = [identifier, vm['vmid'], vm['name'],
                           vm['status'], f"{vm['cpu']:.2%} ({vm['cpus']})",
                           f"{convert_size(vm['mem'])}/{convert_size(vm['maxmem'])}",
                           f"{vm['mem']/vm['maxmem']:.2%}"]
    else:
        status_bar_item = [identifier, vm['vmid'], vm['name'],
                           vm['status'], f"({vm['cpus']})", f"({convert_size(vm['maxmem'])})", ""]
    if identifier == "lxc":  # container specific disk info
        status_bar_item.extend([f"{convert_size(vm['disk'])}/{convert_size(vm['maxdisk'])}", f"{vm['disk']/vm['maxdisk']:.2%}",
                                f"{convert_size(vm['swap'])}/{convert_size(vm['maxswap'])}", f"{vm['swap']/vm['maxswap']:.2%}"])
    else:
        status_bar_item.extend(
            [f"{convert_size(vm['maxdisk'])} (total)", "", "", ""])
    if vm['status'] == "running":
        status_bar_item.append(
            str(datetime.timedelta(seconds=vm['uptime'])))
    return status_bar_item


def build_vm_info(vm_list):
    vm_status_list = []
    status_bar_item_length = [0] * 12
    for vm in vm_list:  # iterate vm
        status_bar_item = build_single_vm_info(vm)
        vm_status_list.append(status_bar_item)
        for idx, val in enumerate(status_bar_item):
            status_bar_item_length[idx] = max(
                status_bar_item_length[idx], len(str(val)))
    return vm_status_list, status_bar_item_length


def build_vm_info_string(item, status_bar_item_length):
    item_str = ""
    for idx, val in enumerate(item, start=1):
        item_str = item_str + str(val) + " "
        if(len(str(val)) <= status_bar_item_length[idx-1]):
            for _ in range(status_bar_item_length[idx-1] - len(str(val)) + 1):
                item_str = item_str + " "
    return item_str


def build_upper_status_bar(status_bar_item_length):
    status_bar_strs = ["TYPE", "VMID", "NAME", "STATUS", "%CPU",
                       "MEM", "%MEM", "DISK", "%DISK", "SWAP", "%SWAP", "UPTIME"]
    statusbar_str = ""
    for idx, item in enumerate(status_bar_strs):
        statusbar_str = statusbar_str + item + " "
        if len(item) <= status_bar_item_length[idx]:
            for _ in range(status_bar_item_length[idx] - len(item) + 1):
                statusbar_str = statusbar_str + " "
    return statusbar_str


def build_bottom_status_bar():
    local_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %Z")
    bottom_statusbar_str = f"proxcat alpha | 'q' to quit, 'n' 'p' to switch between nodes, any other key to force refresh | Local time {local_time}"
    return bottom_statusbar_str
