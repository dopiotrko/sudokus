import wx
from square import *
from grid import *
from threading import Thread


class MyPanel(wx.Panel):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.number_of_buttons = 0
        self.frame = parent
        self.squares = []
        self.grid = None
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
            if self.grid is not None:
                del self.grid
            self.grid = Grid(self)
#            self.Bind(wx.EVT_RIGHT_DOWN, self.determine_cell_thread)
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
        pass

    def determine_grid_thread(self, event):
        possibility_id = event.GetId()
        thread = Thread(target=self.grid.get_last().determine_grid, args=(possibility_id,))
        thread.start()

    def show_error(self, option_id, show):
        square_id, cell_id = option_id
        self.mainGrid.GetItem(square_id).GetWindow().show_error(cell_id, show)

    def undetermine_cell(self, option_id):
        square_id, cell_id = option_id
        return self.squares[square_id].undetermine_cell(cell_id=cell_id)

    def undetermine_grid(self, event):
        option_id = divmod(event.GetId(), 10)
        self.grid.get_last().undetermine_grid(option_id)
