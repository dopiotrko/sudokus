import wx


class DeterminedCell(wx.Button):
    """"""
    def __init__(self, parent, init_id, init_no, bold=False):
        """"Constructor"""
        self.int_label = init_no+1
        self.big_font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Arial')
        if bold:
            self.big_font = self.big_font.Bold()
        wx.Button.__init__(self, parent, id=init_id, label="%s" % self.int_label, size=wx.Size(60, 60))
        self.SetFont(self.big_font)

    def get_int_label(self):
        return self.int_label
