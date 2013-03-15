#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sospiptool.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import os
import sys
import wx
import gui_skeleton
import tools
import var
import shutil
import threading
# import subprocess  # for auto-updating the SOS library
# import Tkinter  # for auto-updating the SOS library
from i18n import _


def SetInitialDirectory(wx_file_picker_ctrl, initial_dpath):
    # Bring wxPy 2.9.4+'s SetInitialDirectory to 2.8.
    # wx bug becomes a feature: set a FilePickerCtrl path to a
    # nonexistent path and it goes as close to the nonexistent
    # path as possible. Then unset the path to have a default
    # directory set when opening the dialog.
    near_dpath = os.path.join(initial_dpath, ' ')  # Assume no subdir named ' '
    wx_file_picker_ctrl.SetPath(near_dpath)
    wx_file_picker_ctrl.SetPath('')


class MainFrame(gui_skeleton.MainFrameBase):
    def __init__(self, parent):
        gui_skeleton.MainFrameBase.__init__(self, parent)
        self.Show()
        self.load_panel(self.panel_loading)
        wx.CallAfter(self.extract_templates)

    def extract_templates(self):
        template_dpath = os.path.join(var.CONFIG_DPATH, 'templates')
        tools.mkdir_p(template_dpath)
        if not os.listdir(template_dpath):  # Is dir empty?
            self.load_panel(self.panel_firstrun)
            wx.Yield()
            import bg_templates_tar_bz2

            default_templates = bg_templates_tar_bz2.get_tarfile()
            default_templates.extractall(template_dpath)
        SetInitialDirectory(self.panel_main.file_picker_bg, template_dpath)
        wx.CallAfter(self.load_panel, self.panel_main)

    def information_message(self, information):
        # MessageBox is equivalent to:
        # a = MessageDialog
        # a.ShowModal()
        wx.MessageBox(information, _('Information'), wx.ICON_INFORMATION, self)
        self.load_panel(self.panel_main)
        self.panel_main.btn_add.Enable(True)

    def error_message(self, message):
        wx.MessageBox(message, _('Error'), wx.ICON_ERROR, self)
        self.load_panel(self.panel_main)
        self.panel_main.btn_add.Enable(True)

    def validate(self):
        """
        Returns True if valid, False if not valid.
        Shows a dialog if not valid.
        """
        errors = [
            (self.clip_name,
             _('Clip name is empty.')),
            (self.bg_input_fpath,
             _('No background image is selected.')),
            (self.pip_input_fpath,
             _('No PiP image is selected.')),
            (self.clip_category,
             _('Clip category is empty.'))
        ]
        #: Get errors that correspond to empty fields
        errors = [err[1] for err in errors if not err[0]]
        errors = '\n'.join(errors)
        if errors:
            errors = _('All fields must be filled in.') + '\n' + errors
            self.error_message(errors)
            return False
        return True

    def clobber_check(self, clip_dpath):
        """
        Returns True if it's OK to proceed
        """
        if not os.path.exists(clip_dpath):
            return True
        dialog = wx.MessageDialog(
            self,
            _('A clip with this name already exists. Replace?'),
            _('Confirm Replacement'),
            wx.YES_NO
        )
        result = dialog.ShowModal()
        if result != wx.ID_YES:
            return False
        shutil.rmtree(clip_dpath)
        return True

    def btn_add_act(self, event):
        is_valid = self.validate()
        if not is_valid:
            return
        can_proceed = self.clobber_check(self.clip_dpath)
        if not can_proceed:
            return

        self.panel_main.btn_add.Enable(False)
        self.load_panel(self.panel_adding)
        wx.CallAfter(WorkerThread, self, self.clip_name, self.bg_input_fpath,
                     self.pip_input_fpath, self.clip_category, self.clip_dpath,
                     self.pip_scale)

    @property
    def clip_name(self):
        return self.panel_main.txt_clip_name.GetValue()

    @property
    def bg_input_fpath(self):
        return self.panel_main.file_picker_bg.GetPath()

    @property
    def pip_input_fpath(self):
        return self.panel_main.file_picker_pip.GetPath()

    @property
    def clip_category(self):
        return self.panel_main.combo_category.GetValue()

    @property
    def clip_dpath(self):
        category_dpath = os.path.join(
            var.MEDIA_DPATH, tools.sanitize_path(self.clip_category))
        clip_dir = os.path.join(
            category_dpath, tools.sanitize_path(self.clip_name))
        return clip_dir

    @property
    def pip_scale(self):
        return self.panel_main.slider_scale.GetValue()


class WorkerThread(threading.Thread):
    def __init__(self, wx_parent, clip_name, bg_input_fpath, pip_input_fpath,
                 clip_category, clip_dpath, pip_scale):
        threading.Thread.__init__(self)
        self.wx_parent = wx_parent
        self.clip_name = clip_name
        self.bg_input_fpath = bg_input_fpath
        self.pip_input_fpath = pip_input_fpath
        self.clip_category = clip_category
        self.clip_dpath = clip_dpath
        self.pip_scale = pip_scale
        self.start()

    def run(self):
        thumbnail_dpath = os.path.join(self.clip_dpath, 'media')
        try:
            tools.mkdir_p(thumbnail_dpath)
        except OSError as err:
            wx.CallAfter(
                self.wx_parent.error_message,
                _('Permission error creating clip directory.')
            )
            return

        tools.save_safe_image(self.clip_dpath, self.bg_input_fpath)
        tools.save_safe_image(self.clip_dpath, self.pip_input_fpath)
        tools.save_thumbnails(thumbnail_dpath, self.pip_input_fpath)

        pip_width, pip_height = tools.get_pip_size(
            self.pip_input_fpath,
            self.pip_scale
        )

        bg_fname = tools.sanitize_path(os.path.split(self.bg_input_fpath)[1])
        pip_fname = tools.sanitize_path(os.path.split(self.pip_input_fpath)[1])
        clip_config = tools.default_clip_config()
        clip_config['name'] = self.clip_name
        clip_config['data'] = bg_fname
        clip_config['pip'] = pip_fname
        clip_config['pipwidth'] = pip_width
        clip_config['pipheight'] = pip_height
        clip_config['category'] = self.clip_category

        clip_config_buf = ''
        # name, data, pip must be first 3 items in order
        ordered_config_items = ['name', 'data', 'pip']
        for line in ordered_config_items:
            clip_config_buf += line + ' = ' + clip_config[line] + os.linesep
            # Add the rest of the items whose order probably doesn't matter
        for key, value in clip_config.iteritems():
            key = unicode(key)
            value = unicode(value)
            if value and (key not in ordered_config_items):
                clip_config_buf += key + ' = ' + value + os.linesep

        clip_config_fpath = os.path.join(self.clip_dpath, 'playlist.sos')
        with open(clip_config_fpath, 'wb') as clip_config_fobj:
            clip_config_fobj.write(tools.encode(clip_config_buf))

        # # Update the SOS library
        # # Not used because updating the library doesn't automatically update
        # # the playlist panel in SOS Stream GUI, and updating the playlist
        # # panel in SOS Stream GUI the right way would be tedious.
        # # Rescanning the library automatically without refreshing the
        # # playlist panel could confuse users.
        # child = subprocess.Popen(
        #    ['/shared/sos/default/bin/scan_library'], stdout=subprocess.PIPE
        # )
        # while child.poll() is None:  # Read command output as it comes
        #    out = child.stdout.readline()
        #    print(out.strip())  # Put this in a status window later
        # # The menu can be updated, at least:
        # wish = Tkinter.Tk()
        # wish.withdraw()  # Hide Tk window. Possible with constructor?
        # try:
        #    wish.send('sos_stream_gui',
        #              'destroy',
        #              '.menubar.library')
        #    wish.send('sos_stream_gui',
        #              'mk_library_menu',
        #              '.menubar.library')
        # except Tkinter.TclError as err:
        #    pass  # SOS Stream GUI not open

        # Done
        success_message = '\n'.join(
            [
                _('Clip "{}" successfully added.'),
                _('To activate the changes, '
                  'perform the following actions in SOS Stream GUI:'),
                _('Library -> Update Library...\n'
                  'Library -> (all/{})')
            ]
        ).format(
            clip_config['name'],
            clip_config['category']
        )
        wx.CallAfter(self.wx_parent.information_message, success_message)


def main():
    # Switch to argparse for any new flags.
    if len(sys.argv) > 1 and sys.argv[1] == '--make-shortcut':
        try:
            ret = tools.make_shortcut()
        except OSError as err:
            sys.stderr.write(err.args[0] + '\n')
            return
        if ret:
            return
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
