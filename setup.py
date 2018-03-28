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


tests_require = [
    'vcrpy',
    'pytest',
    'tox',
]

setup(
    name='flag-bearer',
    version=__version__,
    url='http://github.com/ISEAGE-ISU/flag-bearer',
    description='CDC IScorE Flag Utility',
    long_description=read('README.md'),
    author='ISEAGE',
    author_email='iseage@iastate.edu',
    license='MIT',
    packages=find_packages(),

    setup_requires=[
        'pytest-runner',
    ],
    install_requires=parse_requirements(os.path.join(ROOT, 'requirements.txt')),
    tests_require=tests_require,

    extras_require={
        'remote': [
            'paramiko',
        ],
        'tests': tests_require,
    },

    classifiers=[
        'Development Status :: 4 - Beta',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Topic :: Internet :: WWW/HTTP',

        'License :: OSI Approved :: MIT License',
    ],

    entry_points={
        'console_scripts': [
            'flag-bearer=flag_bearer.cli:main',
        ]
    },
    package_data={
        'flag_bearer': ['default.ini'],
    },
)
