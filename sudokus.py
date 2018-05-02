import wx
from panel import *


class MainWidow(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Sudoku Solver")
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        main_panel = MyPanel(self)
        self.fSizer.Add(main_panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWidow()
    app.MainLoop()
