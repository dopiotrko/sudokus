import wx
from square import *
from grid import *
from threading import Thread
from time import sleep


class MyPanel(wx.Panel):
    """Definition and operation on GUI"""
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

        self.startManual = wx.Button(self, label="Set new game manually")
        self.startManual.Bind(wx.EVT_BUTTON, self.manual_start)
        self.controlSizer.Add(self.startManual, 0, wx.EXPAND | wx.ALL, 5)

        self.startAuto = wx.Button(self, label="Start new random game")
        self.startAuto.Bind(wx.EVT_BUTTON, self.automatic_start)
        self.controlSizer.Add(self.startAuto, 0, wx.EXPAND | wx.ALL, 5)

        self.validate_in_flow = wx.CheckBox(self, id=8001, label="    Allow only\n correct moves")
        self.validate_in_flow.Disable()
        self.validate_in_flow.Bind(wx.EVT_CHECKBOX, self.set_block_errors)
        self.controlSizer.Add(self.validate_in_flow, 0, wx.CENTER | wx.ALL, 5)

        self.check = wx.Button(self, label="Check")
        self.check.Disable()
        self.check.Bind(wx.EVT_BUTTON, self.check_correctness)
        self.controlSizer.Add(self.check, 0, wx.EXPAND | wx.ALL, 5)

        self.solve = wx.Button(self, label="Solve")
        self.solve.Disable()
        self.solve.Bind(wx.EVT_BUTTON, self.solve_game)
        self.controlSizer.Add(self.solve, 0, wx.EXPAND | wx.ALL, 5)

        self.endGame = wx.Button(self, label="End game")
        self.endGame.Disable()
        self.endGame.Bind(wx.EVT_BUTTON, self.end_game)
        self.controlSizer.Add(self.endGame, 0, wx.CENTER | wx.ALL, 5)

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
        """Starts the game: allowing to set up initial cells, or/and blocking initial cells, or/and reseting game"""
        if self.grid is None:  # self.startManual.GetValue():
            self.grid = Grid(self)
            self.grid.__class__.init_mode = True
            [singleSquare.enable_all(True) for singleSquare in self.squares]
            [singleSquare.reset_determine_cells() for singleSquare in self.squares]
            [singleSquare.toggle_all(True) for singleSquare in self.squares]

            self.status_bar.SetStatusText("Set the initial numbers, and then press 'Start Manually'")
            self.startManual.SetLabel('Start Manually')
            self.validate_in_flow.Disable()
            self.endGame.Enable()
            self.startAuto.Disable()
            self.set_block_errors(state=True)
            self.startManual.Disable()
        else:
            self.disable_all_init_cells_thread()
            self.status_bar.SetStatusText("Play the game")
            self.startManual.SetLabel("Set new game manually")
            self.validate_in_flow.Enable()
            self.check.Enable()
            self.solve.Enable()
            self.startManual.Disable()
            self.set_block_errors(state=False)
            self.grid.__class__.init_mode = False

    # ----------------------------------------------------------------------
    def automatic_start(self, event):
        """Randomly setting initial cells, and blocking them"""
        self.grid = Grid(self)
        [singleSquare.enable_all(True) for singleSquare in self.squares]
        [singleSquare.reset_determine_cells() for singleSquare in self.squares]
        [singleSquare.toggle_all(True) for singleSquare in self.squares]
        self.status_bar.SetStatusText("Play the game")
        self.validate_in_flow.Enable()
        self.startManual.Disable()
        self.startAuto.Disable()
        self.endGame.Enable()
        self.check.Enable()
        self.solve.Enable()
        self.set_block_errors(state=True)
        self.grid.get_last().random_game()
        self.set_block_errors(state=False)
        thread = Thread(target=self.disable_all_init_cells_thread)
        thread.start()

    def disable_all_init_cells_thread(self):
        wx.CallAfter(self.disable_all_init_cells_thread_wx)

    def disable_all_init_cells_thread_wx(self):
        [single_square.disable_all_init_cells() for single_square in self.squares]
        self.grid.__class__.init_mode = False
        self.startManual.Disable()

    def end_game(self, event):
        if self.grid is not None:
            self.grid.reset()
            self.grid = None
        [singleSquare.enable_all(False) for singleSquare in self.squares]
        [singleSquare.reset_determine_cells() for singleSquare in self.squares]
        [singleSquare.toggle_all(False) for singleSquare in self.squares]
        self.validate_in_flow.Disable()
        self.startManual.Enable()
        self.startManual.SetLabel("Set new gama manually")
        self.startAuto.Enable()
        self.check.Disable()
        self.solve.Disable()
        self.endGame.Disable()

    def post_determine_cell(self, possibility_id):
        """Setting GUI cell according to data from grid"""
        square_id = possibility_id[0]
        self.squares[square_id].post_determine_cell(possibility_id)

    def determine_grid_thread(self, event):
        """In every move: Updating (in new thread) algorytm validating/solving the moves in game"""
        possibility_id = event.GetId()
        option_id, cell_no = divmod(possibility_id, 10)
        square_id, cell_id = divmod(option_id, 10)
        possibility_id = square_id, cell_id, cell_no
        thread = Thread(target=self.grid.get_last().determine_grid, args=(possibility_id,))
        thread.start()

    def show_error(self, option_id, show):
        """Showing collided numbers"""
        square_id, cell_id = option_id
        self.squares[square_id].show_error(cell_id, show)

    def show_errors(self, errors, delay=.2):
        """Showing collided numbers"""
        for x in errors:
            self.show_error(x, True)
        while delay >= 1:
            self.check.Disable()
            self.check.SetLabel('%d' % int(delay))
            sleep(1)
            delay -= 1
            if self.solve.IsEnabled():
                self.check.Enable()
        sleep(delay)
        self.check.SetLabel('Check')
        for x in errors:
            self.show_error(x, False)

    def undetermine_cell(self, option_id):
        """Deleting determined cell in GUI, and showing back options of this cell"""
        square_id, cell_id = option_id
        self.squares[square_id].undetermine_cell(cell_id)

    def undetermine_grid(self, option_id):
        """Then move is cancelled: Updating (algorytm validating/solving the moves in game"""
        option_id = divmod(option_id, 10)
        self.grid.get_last().undetermine_grid(option_id)

    def set_block_errors(self, event=None, state=True):
        """Changing block_errors - class Grid attribute. On/off checking for errors on flow"""
        if event is None:
            self.grid.__class__.block_errors = state
            self.validate_in_flow.SetValue(state)
        else:
            if len(self.grid.get_errors_list()) is 0:
                self.grid.__class__.block_errors = self.validate_in_flow.IsChecked()
            else:
                self.status_bar.SetStatusText('Errors already on board. Correct errors to activate checkbox')
                self.validate_in_flow.SetValue(False)

    def check_correctness(self, event):
        Thread(target=self.grid.check_correctness).start()

    def solve_game(self, event):
        Thread(target=self.grid.solve_game).start()
