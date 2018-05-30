import wx


class DeterminedCell(wx.Panel):
    """Cell"""
    def __init__(self, parent, init_id, init_no, bold=False):
        """"Constructor"""
        self.int_label = init_no+1
        self.label = "%s" % self.int_label
        wx.Panel.__init__(self, parent, id=init_id, size=wx.Size(60, 60), style=wx.ALIGN_CENTER)
        bg_sizer = wx.BoxSizer()
        self.big_font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Arial')
        if bold:
            self.big_font = self.big_font.Bold()
        self.button = wx.Button(self, id=init_id, label=self.label, size=wx.Size(56, 56))
        self.button.SetFont(self.big_font)
        bg_sizer.AddStretchSpacer()
        bg_sizer.Add(self.button, 0, wx.CENTER)
        bg_sizer.AddStretchSpacer()
        self.SetSizer(bg_sizer)

    def Bind(self, event, handler, **kwargs):
        self.button.Bind(event, handler, **kwargs)

    def Unbind(self, event, **kwargs):
        self.button.Unbind(event, **kwargs)

    def get_int_label(self):
        return self.int_label

    def show_error(self, show=True):
        """Showing collided numbers"""
        if show:
            self.SetBackgroundColour(wx.RED)
        else:
            self.SetBackgroundColour(None)
        self.Refresh()
