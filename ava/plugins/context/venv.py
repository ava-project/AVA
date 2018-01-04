import os
import sys
import platform
import subprocess
import virtualenv

if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except:
        raise RuntimeError('An unexpected error occured')
    venv = os.path.join(os.path.expanduser('~'), '.ava', 'plugins', name, 'venv')
    if platform.system() == 'Windows':
        venv_dir = 'Scripts'
        venv_executable = '{}/{}.exe'.format(venv_dir, 'pip3.6')
    else:
        venv_dir = 'bin'
        venv_executable = '{}/{}'.format(venv_dir, 'pip3.6')
    script = os.path.join(venv, venv_dir, 'activate_this.py')
    try:
        virtualenv.create_environment(venv, site_packages=False, clear=True)
    except:
        raise RuntimeError('Creating virtualenv failed')
    if sys.executable is None:
        raise RuntimeError('Could not find a python interpreter')
    with open(os.devnull, 'w') as FNULL:
        try:
            subprocess.call([sys.executable, '{}'.format(script)], stdout=FNULL)
        except subprocess.CalledProcessError:
            raise RuntimeError('Could not activate the virtual environment')
        try:
            subprocess.call(
                [
                    '{}'.format(os.path.join(venv, venv_executable)), 'install',
                    'git+https://github.com/ava-project/sdk.git'
                ],
                stdout=FNULL)
        except subprocess.CalledProcessError:
            raise RuntimeError('Downloading avasdk in virtualenv failed')
