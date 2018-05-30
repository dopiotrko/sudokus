import wx
import wx.lib.newevent

DetermineEvent, EVT_DETERMINE_CELL = wx.lib.newevent.NewCommandEvent()


class Options(wx.GridSizer):
    """Options ic single cell"""
    def __init__(self, parent, init_id):
        """"Constructor"""
        self.id = init_id
        self.parent = parent
        wx.GridSizer.__init__(self, rows=3, cols=3, hgap=0, vgap=0)
        self.possibilities = []
        self.small_font = wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Arial')
        for i in range(3*3):
            t_button = wx.ToggleButton(parent, id=self.id * 10 + i, label='%s' % (i + 1), size=wx.Size(20, 20))
            self.possibilities.append(t_button)
            self.possibilities[i].SetFont(self.small_font)
            self.possibilities[i].SetValue(False)
            self.possibilities[i].Disable()
            self.possibilities[i].Bind(wx.EVT_RIGHT_DOWN, self.toggle)
            self.possibilities[i].Bind(wx.EVT_LEFT_DOWN, parent.parent.determine_grid_thread)
            self.possibilities[i].Bind(wx.EVT_LEFT_DOWN, parent.determine_cell)
            self.possibilities[i].Bind(EVT_DETERMINE_CELL, parent.determine_cell)
            self.Add(self.possibilities[i], 0, wx.EXPAND)

    def enable_all(self, state):
        """Enabling or disabling possibilitys of single cell"""
        [single_possibility.Enable() for single_possibility in self.possibilities if state]
        [single_possibility.Disable() for single_possibility in self.possibilities if not state]

    def toggle_all(self, state):
        """Toggling on/off possibilitys of single cell"""
        [single_possibility.SetValue(state) for single_possibility in self.possibilities]

    @staticmethod
    def toggle(event):
        """Toggling on/off single possibility of single cell"""
        toggle_button = event.GetEventObject()
        toggle_button.SetValue((not toggle_button.GetValue()))

    def post_determined_cell(self, possibility_id):
        wx.PostEvent(self.possibilities[possibility_id[2]],
                     DetermineEvent(id=possibility_id[0]*100+possibility_id[1]*10+possibility_id[2]))
