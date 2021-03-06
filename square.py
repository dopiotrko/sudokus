import wx
from options import *
from determinedcell import *
from threading import Thread


class Square(wx.Panel):
    """Operating on 9x9 square in GUI"""
    def __init__(self, parent, init_id):
        """"Constructor"""
        self.id = init_id
        self.parent = parent
        self.determined_cells = [None]*9
        wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
        self.grid = wx.GridSizer(rows=3, cols=3, hgap=1, vgap=1)
        self.cell = []
        for i in range(3*3):
            self.cell.append(Options(self, self.id*10+i))
            self.grid.Add(self.cell[i], 0, wx.EXPAND)
        self.SetSizer(self.grid)

    def post_determine_cell(self, possibility_id):
        """Setting GUI cell according to data from grid"""
        self.cell[possibility_id[1]].post_determined_cell(possibility_id)

    def determine_cell(self, event):
        """Creating/determining single cell, and hiding options of this cell"""
        possibility_id = event.GetId()
        option_id, cell_no = divmod(possibility_id, 10)
        square_id, cell_id = divmod(option_id, 10)
        bold_bool = self.parent.grid.init_mode
        self.determined_cells[cell_id] = DeterminedCell(self, option_id, cell_no, bold_bool)
        self.grid.Hide(cell_id)
        self.grid.Detach(cell_id)
        self.grid.Insert(cell_id, self.determined_cells[cell_id])
        self.determined_cells[cell_id].Bind(wx.EVT_BUTTON, self.undetermine)
        self.grid.Layout()
        event.Skip()
        Thread(target=self.refresh).start()

    def refresh(self):
        """Refreshing window to fix layout problems"""
        wx.CallAfter(self.parent.frame.Layout)

    def undetermine(self, event):
        """Colling undetermine functions"""
        option_id = event.GetId()
        self.parent.undetermine_grid(option_id)
        cell_id = option_id % 10
        self.undetermine_cell(cell_id)

    def undetermine_cell(self, cell_id):
        """Deleting determined cell, and showing back options of this cell"""
        if self.determined_cells[cell_id] is None:
            return
        self.grid.Hide(cell_id)
        self.grid.Remove(cell_id)
        self.determined_cells[cell_id].DestroyLater()
        self.determined_cells[cell_id] = None
        self.grid.Insert(cell_id, self.cell[cell_id])
        self.grid.Show(cell_id, True)
        self.grid.Layout()
    #        self.grid.Fit(self)

    def reset_determine_cells(self):
        """Colling undetermined_cell for every cell i 9x9 square"""
        for single_det_cell in self.determined_cells:
            if single_det_cell is not None:
                determined_cell_id = single_det_cell.GetId()
                cell_id = determined_cell_id % 10
                self.undetermine_cell(cell_id)

    def enable_all(self, state):
        """Enabling or disabling possibilitys of all cells in 9x9 square"""
        [singleCell.enable_all(state) for singleCell in self.cell]

    def toggle_all(self, state):
        """Toggling on/off possibilitys of all cells in 9x9 square"""
        [singleCell.toggle_all(state) for singleCell in self.cell]

    def disable_all_init_cells(self):
        """Blocking all cells setted as initial cells on the beginning of the game"""
        [single_det_cell.Unbind(wx.EVT_BUTTON) for single_det_cell in self.determined_cells
         if single_det_cell is not None]

    def show_error(self, cell_id, show):
        """Showing collided numbers"""
        if self.determined_cells[cell_id] is not None:
            self.determined_cells[cell_id].show_error(show)
