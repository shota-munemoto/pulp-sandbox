import multiprocessing
import webbrowser
import tkinter
import tkinter.font
import server
import utils

host = 'localhost'
port = '5000'
development_static_port = '3000'


def run_server():
    server.run(host, port)


def browser_opener(url):
    def open_browser():
        webbrowser.open_new_tab(url)

    return open_browser


def terminator(tkinter_root, server_process):
    def terminate_all():
        server_process.terminate()
        server_process.join()
        tkinter_root.destroy()

    return terminate_all


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

    root = tkinter.Tk()
    root.title('scheduling')
    terminate_all = terminator(root, server_process)
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
    root.mainloop()
