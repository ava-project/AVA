import sys
from os import path
from multiprocessing import freeze_support

sys.executable = path.join(sys.exec_prefix, 'pythonw.exe')
freeze_support()

__version__ = '0.0.1'
