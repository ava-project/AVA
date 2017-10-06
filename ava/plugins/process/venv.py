import os
import pip
import sys
import platform
import virtualenv

name = sys.argv[1]
venv = os.path.join(os.path.expanduser('~'), '.ava', 'plugins', name, 'venv')
script = os.path.join(
    venv,
    'Scripts' if platform.system() == 'Windows' else 'bin',
    'activate_this.py')
virtualenv.create_environment(venv, site_packages=False, clear=True)
os.system(sys.executable + ' {}'.format(script))
os.system("{} install git+https://github.com/ava-project/sdk.git".format(
    os.path.join(
        venv,
        'Scripts/pip3.6.exe' if platform.system() == 'Windows' else 'bin/pip3.6')))
