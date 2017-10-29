import sys
import platform
import subprocess
import virtualenv
from os import path

name = sys.argv[1]
venv = path.join(path.expanduser('~'), '.ava', 'plugins', name, 'venv')
if platform.system() == 'Windows':
    venv_dir = 'Scripts'
    venv_executable = '{}/{}.exe'.format(venv_dir, 'pip3.6')
else:
    venv_dir = 'bin'
    venv_executable = '{}/{}'.format(venv_dir, 'pip3.6')
script = path.join(venv, venv_dir, 'activate_this.py')
virtualenv.create_environment(venv, site_packages=False, clear=True)
_ = subprocess.check_output([sys.executable, '{}'.format(script)])
_ = subprocess.check_output(
    [
        '{}'.format(path.join(venv, venv_executable)),
        'install',
        'git+https://github.com/ava-project/sdk.git'
    ])
