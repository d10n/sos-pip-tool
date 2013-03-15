============
SOS PiP Tool
============

A simple Picture-in-Picture clip creation tool for Science On a Sphere.

.. image:: http://dl.dropbox.com/u/34148684/sos-pip-tool-screenshot.png
   :alt: Screenshot

Installation
============

Easy mode
---------
1. Log in as ``sos``
2. Open the terminal (Ctrl + Alt + T)
3. Paste these lines, one at a time (Ctrl + Shift + V)::

    sudo apt-get install -y python-pip python-wxgtk2.8 imagemagick
    sudo pip install http://dl.dropbox.com/u/34148684/sos_pip_tool-0.1.tar.gz
    which rehash && rehash
    sospiptool --make-shortcut

   * Enter the ``sos`` account password when prompted

Advanced notes
--------------
Dependencies:
 * `wxPython 2.8 <http://www.wxpython.org/>`_
 * `imagemagick <http://www.imagemagick.org/>`_
 * `sh <https://pypi.python.org/pypi/sh>`_

Usage
=====

1. Run the program, fill in the blanks, and click the "Add Clip" button.

   * The scale slider sets the length of the longer side of the PiP in degrees.

2. In the SOS Stream GUI, update the library and (re)open the category of the new clip.

License
=======

Public domain. See ``UNLICENSE``

Todo
====

 * Previews.
 * Support video background and PiP. This could make previews harder.
 * Automatic .po compilation.

Notes
=====

It would have been "sos-pip-tool" if Python module names could have dashes. I don't like program names with underscores.

Hopefully easy mode install will become easier.

Previously required Wand 0.3.0
