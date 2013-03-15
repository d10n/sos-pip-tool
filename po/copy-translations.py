#!/usr/bin/env python
# -*- coding: utf-8 -*-
# copy-translations.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import os
import errno
import shutil


DOMAIN = 'sospiptool'


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def copy_translations():
    translations = []
    for fname in os.listdir('.'):
        lang, ext = os.path.splitext(fname)
        if ext == '.mo' and lang != DOMAIN:
            translations.append((lang, ext))

    for lang, ext in translations:
        dest_dpath = os.path.join('..', 'locale', lang, 'LC_MESSAGES')
        dest_fpath = os.path.join(dest_dpath, DOMAIN + ext)
        mkdir_p(dest_dpath)
        shutil.move(lang + ext, dest_fpath)


if __name__ == '__main__':
    copy_translations()
