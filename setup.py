#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages
from flag_bearer import __version__


ROOT = os.path.dirname(__file__)


def parse_requirements(filename):
    requirements = []
    for line in open(filename, 'r').read().split('\n'):
        # Skip comments
        if re.match(r'(\s*#)|(\s*#)', line):
            continue
        requirements.append(line)

    return requirements


def read(fname):
    return open(os.path.join(ROOT, fname)).read()


setup(
    name='flag-bearer',
    version=__version__,
    url='http://github.com/ISEAGE-ISU/flag-bearer',
    description='CDC IScorE Flag Utility',
    long_description=read('README.md'),
    author='ISEAGE',
    author_email='iseage@iastate.edu',
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=parse_requirements(os.path.join(ROOT, 'requirements.txt')),
    tests_require=[
        'pytest',
        'tox',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={
        'console_scripts': [
            'flag-bearer=flag_bearer.cli:main',
        ]
    }
)

