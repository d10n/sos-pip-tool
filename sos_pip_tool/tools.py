#
# -*- coding: utf-8 -*-
# tools.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import os
import errno
# try:
#     import wand.api
#     import wand.image
# except ImportError as ex:
#     if ex.args[0].startswith('No module named'):
#         print('sudo apt-get install libmagickwand-dev')
#         raise
try:
    # noinspection PyUnresolvedReferences
    from sh import convert, identify  # Depends on imagemagick
    # mogrify $1 -strip -colorspace RGB
except ImportError as ex:
    if ex.args[0].startswith('cannot import name'):
        print('sudo apt-get install imagemagick')
    elif ex.args[0] == 'No module named sh':
        print('sudo apt-get install python-pip')
        print('sudo pip install sh')
    raise


def default_clip_config():
    """
    http://www.sos.noaa.gov/Docs/pl_4_0_x.html
    """
    return {
        'name': 'PiP over BG',  # Don't remove this line
        'data': 'bg.jpg',       # Don't remove this line
        'pip': 'pip.png',       # Don't remove this line
        'pipalpha': '1.0',
        'piptimer': '0',
        'pipwidth': '40',
        'pipheight': '40',
        'category': 'extra',
        #'catalog_url': None,    # Meta; email sos.gsd@noaa.gov to contribute
        #'audio': None,          # Background audio
        #'fps': '30',            # Overrides data fps
        #'pipstyle': None,       # projector|globe|room
        #'pipcoords': None,      # lat,lon
        #'pipfps': None,         # Overrides pip fps
        #'piptimer': None,       # Total secs pip is displayed
        #'pipdelay': None,       # Seconds before pip is displayed
        #'pipfadein': None,      # Seconds for pip to fade in
        #'pipfadeout': None,     # Seconds for pip to fade out
        #'pipvertical': None,    # Degrees pip center is shifted above equator
        #'piphorizontal': None,  # Degrees pip center is shifted right
        #'duration': None,       # Repeat time in seconds for entire clip
    }


def sanitize_path(fpath):
    """
    SOS path names can include non-ASCII chars, but not spaces
    """
    return fpath.replace(' ', '_')


def mkdir_p(dpath):
    # http://stackoverflow.com/questions/600268/
    try:
        os.makedirs(dpath)
    except OSError as ex:  # Python >2.5
        if ex.errno == errno.EEXIST and os.path.isdir(dpath):
            pass
        else:
            raise


def encode(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    return text


def get_pip_size(pip_fpath, pip_scale):
    """
    Returns proportional width and height for an image, with the longer
    side being image_scale units
    """
    # if var.USE_WAND:
    #     pip_fpath = encode(pip_fpath)  # Wand wants str
    #     with wand.image.Image(filename=pip_fpath) as img:
    #         aspect_ratio = float(img.size[0]) / img.size[1]
    # else:
    width, height = identify('-format', '%w %h', pip_fpath).split()
    aspect_ratio = float(width) / float(height)

    if aspect_ratio > 1:  # w>h
        pip_width = pip_scale
        pip_height = pip_scale / aspect_ratio
    else:  # w<h
        pip_width = pip_scale * aspect_ratio
        pip_height = pip_scale
    return pip_width, pip_height


def save_safe_image(clip_out_dpath, image_in_fpath):
    """
    Trust image manipulation libraries to read
    potentially broken images and save fixed images
    """
    out_fname = os.path.split(image_in_fpath)[1]
    out_fname = sanitize_path(out_fname)
    image_out_fpath = os.path.join(clip_out_dpath, out_fname)
    # if var.USE_WAND:
    #     image_in_fpath = encode(image_in_fpath)  # Wand wants str
    #     image_out_fpath = encode(image_out_fpath)  # Wand wants str
    #     with wand.image.Image(filename=image_in_fpath) as img:
    #         img.type = 'truecolor'  # TODO check color profile
    #         if img.format == 'PNG':
    #             # Hack; Wand doesn't seem to always save alpha channels
    #             img.alpha_channel = True
    #             # img.type 'colorseparation' crashes SOS
    #         img.save(filename=image_out_fpath)
    # else:
    convert(image_in_fpath, image_out_fpath)


def save_thumbnails(thumb_out_dpath, pip_in_fpath):
    # if var.USE_WAND:
    #     pip_in_fpath = encode(pip_in_fpath)  # Wand wants str
    #     with wand.image.Image(filename=pip_in_fpath) as img:
    #         # use expected sizes and names for thumbnails
    #         for size, thumb_out_fpath in (
    #             (800, os.path.join(thumb_out_dpath, 'thumbnail_big.jpg')),
    #             (128, os.path.join(thumb_out_dpath, 'thumbnail_small.jpg'))
    #         ):
    #             with img.clone().convert('jpeg') as i:
    #                 # Wand wants str
    #                 thumb_out_fpath = encode(thumb_out_fpath)
    #                 i.type = 'truecolor'
    #                 i.resize(size, size)
    #                 i.save(filename=thumb_out_fpath)
    # else:
    thumb_big_fpath = \
        os.path.join(thumb_out_dpath, 'thumbnail_big.jpg')
    thumb_small_fpath = \
        os.path.join(thumb_out_dpath, 'thumbnail_small.jpg')

    convert(
        pip_in_fpath,
        '-resize',
        '800x800!',  # ! allows aspect ratio change
        thumb_big_fpath
    )
    convert(
        thumb_big_fpath,  # Save time converting from a huge image
        '-resize',
        '128x128!',
        thumb_small_fpath
    )


def make_shortcut():
    shortcut_fname = 'SOS PiP Tool.desktop'
    desktop_dpath = os.path.join(os.path.expanduser('~sos'), 'Desktop')
    shortcut_fpath = os.path.join(desktop_dpath, shortcut_fname)

    if not os.path.exists(desktop_dpath):
        raise OSError('No sos desktop exists')

    import var
    import textwrap
    import stat  # chmod +x
    import pwd  # chown

    with open(shortcut_fpath, 'w') as shortcut_fobj:
        shortcut_fobj.writelines(textwrap.dedent(
            """[Desktop Entry]
            Encoding=UTF-8
            Version={}
            Type=Application
            Terminal=false
            Icon[en_US]=gnome-panel-launcher
            Name[en_US]=SOS PiP Tool
            Exec=sospiptool
            Name=SOS PiP Tool
            Icon=gnome-panel-launcher
            """.format(var.VERSION)
        ))

        permissions = os.stat(shortcut_fpath)
        sos_user = pwd.getpwnam('sos')  # Get sos uid and gid
        shortcut_fd = shortcut_fobj.fileno()
        os.fchmod(shortcut_fd, permissions.st_mode | stat.S_IEXEC)  # chmod +x
        os.fchown(shortcut_fd, sos_user.pw_uid, sos_user.pw_gid)

    exit_after = True
    return exit_after
