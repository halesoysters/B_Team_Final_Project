#!/usr/bin/env python
import os
from setuptools import setup, find_packages
build_dir = '/home/jm/pycharm_projects/python-wheels'
with open('requirements.txt') as f:
    requirements = f.read().replace(build_dir, os.getcwd()).split('\n')
setup(name='dependencies',
      version='1.1',
      install_requires=requirements,
)