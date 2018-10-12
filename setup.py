#!/usr/bin/env python
# coding: utf-8
from os import chdir
from os.path import abspath, dirname

from setuptools import find_packages, setup

chdir(dirname(abspath(__file__)))

with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    author='Brandon Davidson',
    author_email='brad@oatmail.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
    ],
    description='An implementation of JSON Web Tokens using the Bearer authentication scheme for Requests.',
    extras_require={
        'dev': [
            'setuptools-version-command'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    long_description=readme,
    name='requests-bearer',
    packages=find_packages(exclude=('docs')),
    provides=['requests_bearer'],
    url='https://github.com/brandond/requests-bearer',
    version_command=('git describe --tags --dirty', 'pep440-git-full'),
)
