import wx
from square import *


class MyPanel(wx.Panel):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.number_of_buttons = 0
        self.frame = parent
        self.squares = []
        #        square=Square(self)
        self.mainGrid = wx.GridSizer(rows=3, cols=3, hgap=0, vgap=0)

        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.controlSizer = wx.BoxSizer(wx.VERTICAL)

        self.startManual = wx.ToggleButton(self, label="Set new game manually")
        self.startManual.Bind(wx.EVT_TOGGLEBUTTON, self.manual_start)
        self.controlSizer.Add(self.startManual, 0, wx.CENTER | wx.ALL, 5)

        self.startAuto = wx.Button(self, label="Start new random game")
        self.startAuto.Bind(wx.EVT_BUTTON, self.automatic_start)
        self.controlSizer.Add(self.startAuto, 0, wx.CENTER | wx.ALL, 5)

        for i in range(9):
            self.squares.append(Square(self, i))
            self.mainGrid.Add(self.squares[i])
        self.mainSizer.Add(self.mainGrid, 0, wx.CENTER | wx.ALL, 0)
        self.mainSizer.Add(self.controlSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)
        self.status_bar = parent.CreateStatusBar()
        self.status_bar.SetStatusText('You Can set init numbers manually or start game with random numbers')

    # ----------------------------------------------------------------------
    def manual_start(self, event):
        """"""
        if event.GetEventObject().GetValue():
            [singleSquare.enable_all(True) for singleSquare in self.squares]
            [singleSquare.reset_determine_cells() for singleSquare in self.squares]
            [singleSquare.toggle_all(True) for singleSquare in self.squares]

            self.status_bar.SetStatusText("Set the initial numbers using right mouse button, "
                                          "and press 'Start Manually'")
            event.GetEventObject().SetLabel('Start Manually')
        else:
            [single_square.disable_all_init_cells() for single_square in self.squares]
            self.status_bar.SetStatusText("Play the game")
            event.GetEventObject().SetLabel("Set new game manually")

    # ----------------------------------------------------------------------
    def automatic_start(self, event):
        """"""
        self.extract_entire_line(1, 3)

    def extract_entire_line(self, square_id, cell_id):
        digits_in_line = []
        for i in Square.get_line_ids(square_id):
            digits_in_line += self.squares[i].extract_line_from_square(cell_id)
        return digits_in_line

    def extract_entire_col(self, square_id, cell_id):
        digits_in_col = []
        for i in Square.get_col_ids(square_id):
            digits_in_col += self.squares[i].extract_col_from_square(cell_id)
        return digits_in_col