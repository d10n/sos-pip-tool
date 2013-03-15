#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# _preamble.py

# Author: d10n
# No copyright
# Public domain

import os
import sys

path = os.path.abspath(sys.argv[0])
path = os.path.dirname(path)  # ./ (bin)
path = os.path.dirname(path)  # ../ (sos-pip-tool)

sys.path.insert(0, path)
