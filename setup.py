# -*- coding: utf-8 -*-

from setuptools import find_packages
from cx_Freeze import setup, Executable
from sys import platform

import ava


# additionnal packages for cx_Freeze
build_exe_packages = ['idna', 'gtts', 'asyncio', 'venv']
if platform == "darwin":
    build_exe_packages.append('appdirs')
    build_exe_packages.append('packaging')
    build_exe_packages.append('_sysconfigdata_m_darwin_darwin')

include_files = [r"C:\Users\jibb\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",
                 r"C:\Users\jibb\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll",
                 ('ava\\plugins\\context\\main.py', 'lib\\ava\\plugins\\context\\main.py'),
                 ('ava\\plugins\\context\\venv.py', 'lib\\ava\\plugins\\context\\venv.py')]

# project requirements from pip
with open('requirements.txt') as requirement_file:
    requirements = requirement_file.read().splitlines()


setup(
    name='ava',
    version=ava.__version__,
    packages=find_packages(),
    options={
        'build_exe': {
            'packages': build_exe_packages,
            'include_files': include_files
        }
    },
    author='AVA Project',
    author_email='ava_2018@labeip.epitech.eu',
    description='The daemon of the AVA Project',
    long_description=open('README.md').read(),
    install_requires=requirements,
    include_package_data=True,
    url='https://github.com/ava-project/ava-core',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'avad = ava.ava:main',
        ],
    },
    executables=[Executable('app.py')]
)
