import wx


class Options(wx.GridSizer):
    """"""
    def __init__(self, parent, init_id):
        """"Constructor"""
        self.id = init_id
        self.parent = parent
        self.determined = False
        wx.GridSizer.__init__(self, rows=3, cols=3, hgap=0, vgap=0)
        self.possibilities = []
        self.small_font = wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Arial')
        for i in range(3*3):
            t_button = wx.ToggleButton(parent, id=self.id * 10 + i, label='%s' % (i + 1), size=wx.Size(20, 20))
            self.possibilities.append(t_button)
            self.possibilities[i].SetFont(self.small_font)
            self.possibilities[i].SetValue(False)
            self.possibilities[i].Disable()
            self.possibilities[i].Bind(wx.EVT_RIGHT_DOWN, parent.determine_cell)
            self.Add(self.possibilities[i], 0, wx.EXPAND)

    def enable_all(self, state):
        [single_possibility.Enable() for single_possibility in self.possibilities if state]
        [single_possibility.Disable() for single_possibility in self.possibilities if not state]

    def toggle_all(self, state):
        [single_possibility.SetValue(state) for single_possibility in self.possibilities]

