#
# -*- coding: utf-8 -*-
# var.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import os

NAME = 'sos_pip_tool'
DOMAIN = 'sospiptool'
VERSION = '0.1'
# USE_WAND = False

MEDIA_DPATH = os.path.realpath('/shared/sos/media/')
CONFIG_DPATH = os.path.join(
    os.path.expanduser('~'),  # /home/user
    '.config',
    DOMAIN
)
