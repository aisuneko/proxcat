import datetime
from .utils import convert_size
from .const import norm_status_bar_strs, qemu_status_bar_strs, core_temp_chip, avg_temp_feature_label
from . import __version__ as version
try:
    import sensors
except InportError:
    sensors = None

def build_node_info(instance, node, show_sensors):
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
    if show_sensors:
        temp_data = sensors_get_info()
        # if temp_data == -1:
            # print(f"ERROR: Chip {core_temp_chip} not found on system.")
        # elif temp_data == -2:
            # print(f"ERROR: Unknown exception occured while fetching temperature data.")
        # else:
        temp = f"Node CPU Average Temperature: {temp_data} °C"
    return [node_title, cpu, mem, disk] + ([temp] if show_sensors else [])


def build_vm_list(instance, node):
    vm_list = instance.nodes(node['node']).qemu.get(
    ) + instance.nodes(node['node']).lxc.get()
    vm_list.sort(key=lambda d: int(d['vmid']))
    return vm_list


def build_single_vm_info(vm, is_qemu_only):
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
    if identifier == "lxc" and not is_qemu_only:  # container specific disk info
        if vm['maxswap'] == 0:
            if vm['status'] == "running":
                status_bar_item.extend([f"{convert_size(vm['disk'])}/{convert_size(vm['maxdisk'])}", f"{vm['disk']/vm['maxdisk']:.2%}",
                                    "", ""])
            else:
                status_bar_item.extend([f"({convert_size(vm['maxdisk'])})", "",
                                    "", ""])
        else:
            if vm['status'] == "running":
                status_bar_item.extend([f"{convert_size(vm['disk'])}/{convert_size(vm['maxdisk'])}", f"{vm['disk']/vm['maxdisk']:.2%}",
                                    f"{convert_size(vm['swap'])}/{convert_size(vm['maxswap'])}", f"{vm['swap']/vm['maxswap']:.2%}"])
            else:
                status_bar_item.extend([f"({convert_size(vm['maxdisk'])})", "",
                                    f"({convert_size(vm['maxswap'])})", ""])
    else:
        status_bar_item.extend(
            [f"({convert_size(vm['maxdisk'])})"])
        if not is_qemu_only:
            status_bar_item.extend(
                ["", "", ""])
    if vm['status'] == "running":
        status_bar_item.append(
            str(datetime.timedelta(seconds=vm['uptime'])))
    return status_bar_item


def build_vm_info(vm_list, no_lxc):
    vm_status_list = []
    status_bar_item_length = [0] * len(norm_status_bar_strs)
    is_qemu_only = True
    if not no_lxc:
        for vm in vm_list:
            if ('type' in vm and vm['type'] == "lxc"):
                is_qemu_only = False
                break

    for vm in vm_list:
        status_bar_item = build_single_vm_info(vm, is_qemu_only)
        vm_status_list.append(status_bar_item)
        for idx, val in enumerate(status_bar_item):
            status_bar_item_length[idx] = max(
                status_bar_item_length[idx], len(str(val)))
    return vm_status_list, status_bar_item_length, is_qemu_only


def build_vm_info_string(item, status_bar_item_length):
    item_str = ""
    for idx, val in enumerate(item, start=1):
        item_str = item_str + str(val) + " "
        if(len(str(val)) <= status_bar_item_length[idx-1]):
            for _ in range(status_bar_item_length[idx-1] - len(str(val)) + 1):
                item_str = item_str + " "
    return item_str


def build_upper_status_bar(status_bar_item_length, is_qemu_only):
    status_bar_strs = qemu_status_bar_strs if is_qemu_only else norm_status_bar_strs
    statusbar_str = ""
    for idx, item in enumerate(status_bar_strs):
        statusbar_str = statusbar_str + item + " "
        if len(item) <= status_bar_item_length[idx]:
            for _ in range(status_bar_item_length[idx] - len(item) + 1):
                statusbar_str = statusbar_str + " "
    return statusbar_str


def build_bottom_status_bar():
    local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    bottom_statusbar_str = f"proxcat {version} | Local time {local_time}"
    return bottom_statusbar_str

def sensors_get_info():
    sensors.init()
    try:
        has_coretemp_chip = False
        for chip in sensors.iter_detected_chips():
            if chip.__str__() == core_temp_chip:
                has_coretemp_chip = True
                avg_temp = feature_num = 0
                for feature in chip:
                    cur_temp = feature.get_value()
                    if feature.label == avg_temp_feature_label:
                        return cur_temp
                    else:
                        avg_temp = avg_temp + cur_temp
                        feature_num = feature_num + 1
        if not has_coretemp_chip:
            return -1
        avg_temp = avg_temp / feature_num 
        return round(avg_temp, 2)
    except Exception as e:
        return -2
    finally:
        sensors.cleanup()
