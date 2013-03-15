#
# -*- coding: utf-8 -*-
# gui_skeleton.py

# Author: d10n
# No copyright
# Public domain

from __future__ import unicode_literals
import wx
from i18n import _


class MainFrameBase(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            title=_('SOS PiP Tool'),
            style=(wx.DEFAULT_FRAME_STYLE
                   & ~wx.MAXIMIZE_BOX
                   & ~wx.RESIZE_BORDER)
        )

        self.sizer_main = wx.BoxSizer()
        self.SetSizer(self.sizer_main)

        self.panel_main = MainPanel(self)
        self.panel_firstrun = NoticePanel(
            self, _('Initial setup: installing background templates...'))
        self.panel_adding = NoticePanel(
            self, _('Adding Clip...'))
        self.panel_loading = NoticePanel(
            self, _('Loading...')
        )

        self.SetSize(self.panel_main.GetBestSize())
        self.SetSize((400, -1))

        self.panels = []

        def add_panel(panel):
            self.panels.append(panel)
            self.sizer_main.Add(panel, 1, wx.EXPAND)
            self.sizer_main.Show(panel, False)

        add_panel(self.panel_main)
        add_panel(self.panel_firstrun)
        add_panel(self.panel_adding)
        add_panel(self.panel_loading)

        self.load_panel(self.panel_loading)

        self.panel_main.btn_add.Bind(wx.EVT_BUTTON, self.btn_add_act)

    def load_panel(self, panel):
        for item in self.panels:
            item.Show(False)
        panel.Show(True)
        self.Layout()
        # self.Update()
        wx.Yield()

    # Virtual event handlers. Override them in your derived class
    def btn_add_act(self, event):
        event.Skip()


class NoticePanel(wx.Panel):
    def __init__(self, parent, message):
        wx.Panel.__init__(self, parent)
        sizer_h = wx.BoxSizer(wx.VERTICAL)
        sizer_v = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl = wx.StaticText(self, label=message)
        border = 5
        label_max_width = self.GetParent().GetSize()[0] - (10 * border)
        self.lbl.Wrap(label_max_width)
        sizer_h.Add(sizer_v, 1, flag=wx.CENTER)
        sizer_v.Add(self.lbl, 0, flag=wx.CENTER, border=border)
        self.SetSizer(sizer_h)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.FlexGridSizer(rows=0, cols=2)
        sizer.AddGrowableCol(1)

        self.lbl_clip = wx.StaticText(
            self, label=_('Clip Name'))
        self.lbl_bg = wx.StaticText(
            self, label=_('Background Image'))
        self.lbl_pip = wx.StaticText(
            self, label=_('PiP Image'))
        self.lbl_scale = wx.StaticText(
            self, label=_('PiP Scale'))
        self.lbl_category = wx.StaticText(
            self, label=_('Category'))

        self.txt_clip_name = wx.TextCtrl(self, wx.ID_ANY)

        # Bug: wxPython doesn't do tab traversal over FPC (at least on GTK)
        # Bug: wxPython clears the filename but keeps the value on cancel
        # TODO: work around these bugs
        self.file_picker_bg = wx.FilePickerCtrl(
            self,
            message=_('Select a file'),
            wildcard=(_('Supported Image Types') +
                      '(*.png;*.jpg;*.jpeg;*.gif;*.bmp)' +
                      '|*.png;*.jpg;*.jpeg;*.gif;*.bmp')
        )

        self.file_picker_pip = wx.FilePickerCtrl(
            self,
            message=_('Select a file'),
            wildcard=(_('Supported Image Types') +
                      '(*.png;*.jpg;*.jpeg;*.gif;*.bmp)' +
                      '|*.png;*.jpg;*.jpeg;*.gif;*.bmp')
        )

        self.slider_scale = wx.Slider(
            self,
            value=60, minValue=45, maxValue=90,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )

        # TRANSLATORS: "extra" is the standard SOS extra category
        combo_category_choices = [_('extra'), _('sponsors')]
        self.combo_category = wx.ComboBox(self, choices=combo_category_choices)
        self.combo_category.SetSelection(0)

        self.btn_add = wx.Button(self, label=_('&Add Clip'))

        margin = 5

        def add_label(item):
            flag_label = wx.ALL | wx.ALIGN_CENTER_VERTICAL
            sizer.Add(item, flag=flag_label, border=margin)

        def add_input(item):
            flag_input = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND
            sizer.Add(item, flag=flag_input, border=margin)

        add_label(self.lbl_clip)
        add_input(self.txt_clip_name)
        add_label(self.lbl_bg)
        add_input(self.file_picker_bg)
        add_label(self.lbl_pip)
        add_input(self.file_picker_pip)
        add_label(self.lbl_scale)
        add_input(self.slider_scale)
        add_label(self.lbl_category)
        add_input(self.combo_category)
        sizer.AddSpacer(0)
        add_label(self.btn_add)
        self.SetSizer(sizer)
        # self.Fit()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrameBase(None)
    frame.Show()
    frame.load_panel(frame.panel_main)
    app.MainLoop()
