#
# -*- coding: utf-8 -*-
# i18n.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import os
import var
import gettext


def translation(domain, localedir=None, languages=None,
                class_=None, fallback=False, codeset=None):
    """
    First look in localedir,
    then system default localedir,
    then optionally fall back to no translation.
    """
    # noinspection PyUnusedLocal
    try:
        # fallback=False to check system localedir on error
        result = gettext.translation(
            domain, localedir, languages, class_,
            fallback=False, codeset=codeset)
    except IOError as ex:
        try:
            result = gettext.translation(
                domain, None, languages, class_, fallback, codeset)
        except IOError as ex:
            if fallback:
                return gettext.NullTranslations()
            raise ex
    return result


# noinspection PyShadowingBuiltins
def install(domain, localedir=None, unicode=False, codeset=None, names=None):
    """
    Install builtin _().
    Look first in localedir,
    then system default locale dir,
    then fall back to no translation.
    """
    # Default to unicode=False to keep uniformity when other
    # parts of the program use i18n.translation.install()
    t = translation(domain, localedir, fallback=True, codeset=codeset)
    t.install(unicode, names)


_localedir = os.path.join(os.path.dirname(__file__), '../locale')
_t = translation(var.DOMAIN, localedir=_localedir, fallback=True)
_ = _t.ugettext
