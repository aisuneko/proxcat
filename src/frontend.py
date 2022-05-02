import curses
from . import backend
from .utils import handle


class Pointer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tabspace = 4
        # direction: X [down], Y [right]

    def tab(self, tabs=None):
        self.y = self.y + (tabs if tabs else self.tabspace)

    def reverttab(self, tabs=None):
        self.y = self.y - (tabs if tabs else self.tabspace)

    def newline(self):
        self.x = self.x + 1


@handle
def printline(stdscr, string, ptr, maxc):
    stdscr.addnstr(ptr.x, ptr.y, string, maxc)
    ptr.newline()


@handle
def init(stdscr):
    stdscr.idcok(False)
    stdscr.idlok(False)
    stdscr.scrollok(True)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)


@handle
def print_bottom_status_bar(stdscr, width, height):
    bottom_statusbar_str = backend.build_bottom_status_bar()
    stdscr.attron(curses.color_pair(4))
    stdscr.addnstr(height-1, 0, bottom_statusbar_str, width)
    stdscr.addnstr(height-1, len(bottom_statusbar_str), " " *
                   (width - len(bottom_statusbar_str)), width)
    stdscr.attroff(curses.color_pair(4))


@handle
def print_node_info(stdscr, ptr, data, maxc):
    stdscr.attron(curses.color_pair(1))
    ptr.newline()
    for item in data:
        printline(stdscr, item, ptr, maxc)
    ptr.newline()
    stdscr.attroff(curses.color_pair(1))


@handle
def print_vm_info(stdscr, ptr, vm_status_list, status_bar_item_length, maxc):
    stdscr.attron(curses.color_pair(2))
    for item in vm_status_list:
        item_str = backend.build_vm_info_string(item, status_bar_item_length)
        printline(stdscr, item_str, ptr, maxc)
    stdscr.attroff(curses.color_pair(2))


@handle
def print_upper_status_bar(stdscr, width, status_bar_str, node_info_len):
    stdscr.attron(curses.color_pair(3))
    stdscr.addnstr(node_info_len, 0, status_bar_str, width)
    stdscr.addnstr(node_info_len, len(status_bar_str), " " *
                   (width - len(status_bar_str)), width)
    stdscr.attroff(curses.color_pair(3))


def draw(stdscr, instance, update_interval):
    init(stdscr)
    k = 0
    node_idx = 0
    while True:
        k = stdscr.getch()
        nodes = instance.nodes.get()
        nodes_cnt = len(nodes)
        if k == ord('q'):
            break
        elif k == ord('n'):
            node_idx = nodes_cnt - 1 if node_idx + 1 >= nodes_cnt else node_idx + 1
        elif k == ord('p'):
            node_idx = 0 if node_idx - 1 < 0 else node_idx - 1
        node = nodes[node_idx]
        node_info_str = backend.build_node_info(instance, node)
        vm_list = backend.build_vm_list(instance, node)
        vm_status_list, status_bar_item_length = backend.build_vm_info(
            vm_list)
        status_bar_str = backend.build_upper_status_bar(
            status_bar_item_length)
        ptr = Pointer()
        height, width = stdscr.getmaxyx()
        stdscr.erase()

        print_node_info(stdscr, ptr, node_info_str, width)
        print_vm_info(stdscr, ptr, vm_status_list,
                        status_bar_item_length, width)
        print_bottom_status_bar(stdscr, width, height)
        print_upper_status_bar(
            stdscr, width, status_bar_str, len(node_info_str))
        stdscr.noutrefresh()
        curses.doupdate()
        stdscr.timeout(update_interval)
    curses.endwin()
