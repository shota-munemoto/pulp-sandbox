import multiprocessing
import os
import signal
import subprocess
import webbrowser
import psutil
import tkinter
import tkinter.font
import server
import utils

host = 'localhost'
port = '5000'
development_static_port = '3000'


def run_server():
    server.run(host, port)


def run_development_static():
    project_root_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(project_root_directory, 'static'))
    subprocess.run(['npm', 'start'])


def browser_opener(url):
    def open_browser():
        webbrowser.open_new_tab(url)

    return open_browser


# http://psutil.readthedocs.io/en/latest/#kill-process-tree
def kill_proc_tree(pid,
                   sig=signal.SIGTERM,
                   include_parent=False,
                   timeout=None,
                   on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        p.send_signal(sig)
    gone, alive = psutil.wait_procs(
        children, timeout=timeout, callback=on_terminate)
    return (gone, alive)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()

    if utils.frozen():
        url = f'http://{host}:{port}'
    else:
        url = f'http://{host}:{development_static_port}'

    open_browser = browser_opener(url)

    if utils.frozen():
        open_browser()
    else:
        development_static_process = multiprocessing.Process(
            target=run_development_static)
        development_static_process.start()

    root = tkinter.Tk()
    root.title('scheduling')

    def terminate_all():
        kill_proc_tree(os.getpid())
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', terminate_all)
    frame = tkinter.Frame(root)
    frame.pack()
    font = tkinter.font.Font(size=12)
    open_browser_button = tkinter.Button(
        frame, command=open_browser, text='新しい画面を開く。', font=font)
    open_browser_button.pack(fill='x')
    terminate_button = tkinter.Button(
        frame, command=terminate_all, text='終了する。', font=font)
    terminate_button.pack(fill='x')

    def handler(signal_number, stack_frame):
        terminate_all()

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    root.mainloop()
