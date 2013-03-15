#
# -*- coding: utf-8 -*-
# setup.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import os
import sys
from sos_pip_tool import var
from distutils.core import setup


if sys.version_info[0] != 2:
    sys.stderr.write('Sorry, Python 2 only.')
    sys.stderr.write(os.linesep)
    sys.exit(-1)

data_files = []

translations = []
for lang in os.listdir('locale'):
    translations.append(
        (
            os.path.join('share', 'locale', lang, 'LC_MESSAGES'),
            [os.path.join('locale', lang, 'LC_MESSAGES', var.DOMAIN + '.mo')]
        )
    )
data_files += translations

setup(
    name=var.NAME,
    version=var.VERSION,
    packages=[str(var.NAME)],  # Python 2 distutils.core setup unicode fails
    url='https://github.com/d10n/sos_pip_tool',
    license='Public domain',
    author='d10n',
    author_email='david@bitinvert.com',
    description='A simple Picture-in-Picture clip creation tool '
                'for Science on a Sphere',
    scripts=[os.path.join('bin', 'sospiptool')],
    data_files=data_files,
    requires=[
        'wxPython',
        'sh(>=1.08)',
        # 'Wand(==0.3.0)',
    ],
    install_requires=[
        'sh>=1.08',
        # 'wxPython',  # Can't be installed from pip
        # 'Wand==0.3.0',  # Needs non-Python deps to install from pip
    ]
)
