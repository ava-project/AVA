# -*- coding: utf-8 -*-

from setuptools import find_packages
from cx_Freeze import setup, Executable

import ava

setup(
    name='ava',
    version=ava.__version__,
    packages=find_packages(),
    options={
        'build_exe': {
            'packages': ['idna', 'gtts', 'asyncio']
        }
    },
    author='AVA Project',
    author_email='ava_2018@labeip.epitech.eu',
    description='The daemon of the AVA Project',
    long_description=open('README.md').read(),
    install_requires=[
        'flask==0.12',
        'requests',
        'gtts',
        'pynput',
        'watson-developer-cloud',
        'avasdk',
        'playsound',
        'websockets',
    ],
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
