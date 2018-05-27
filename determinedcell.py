import wx


class DeterminedCell(wx.Button):
    """Cell"""
    def __init__(self, parent, init_id, init_no, bold=False):
        """"Constructor"""
        self.int_label = init_no+1
        self.label = "%s" % self.int_label
        self.big_font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Arial')
        if bold:
            self.big_font = self.big_font.Bold()
        wx.Button.__init__(self, parent, id=init_id, label=self.label, size=wx.Size(60, 60))
        self.SetFont(self.big_font)

    def get_int_label(self):
        return self.int_label

    def show_error(self, show=True):
        """Showing collided numbers"""
        '''tmp = self.GetForegroundColour()
        self.SetForegroundColour(wx.Colour(205, 0, 0))
        sleep(.2)
        self.SetForegroundColour(tmp)
        sleep(.1)
        self.SetForegroundColour(wx.Colour(205, 0, 0))
        sleep(.1)
        self.SetForegroundColour(tmp)'''
        if show:
            self.SetLabel('X')
        else:
            self.SetLabel(self.label)
