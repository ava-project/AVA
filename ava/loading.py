from .state import State

def run_in_thread(fn):
    def run(*k, **kw):
        import threading
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    run._origin = fn
    return run

@run_in_thread
def loading(plugins_nbr=0, process_time=1, target=''):
    """
    """
    import os
    from sys import stdout
    from time import sleep
    if not plugins_nbr:
        path = os.path.join(os.path.expanduser('~'), '.ava', 'plugins')
        for element in os.listdir(path):
            if os.path.isdir(os.path.join(path, element)):
                plugins_nbr += 1
    sleep(0.1)
    n = plugins_nbr * process_time
    for i in range(n):
        stdout.write('\r')
        j = (i + 1) / n
        if not State().is_loading() or j > 1:
            break
        stdout.write("Loading %s [%-20s] %d%%" % (target, '='*int(20*j), 100*j))
        stdout.flush()
        sleep(n / 100 * (plugins_nbr / 3))
