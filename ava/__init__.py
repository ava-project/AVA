import os
import sys
import platform
import multiprocessing

if platform.system() == 'Windows':
    sys.executable = os.path.join(sys.exec_prefix, 'pythonw.exe')
elif platform.system() == 'Darwin':
    sys.executable = '/usr/bin/pythonw'
multiprocessing.freeze_support()

__version__ = '0.0.1'
