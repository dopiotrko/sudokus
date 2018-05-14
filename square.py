import wx
from options import *
from determinedcell import *


class Square(wx.Panel):
    """"""
    def __init__(self, parent, init_id):
        """"Constructor"""
        self.id = init_id
        self.parent = parent
        self.determined_cells = [None for x in range(9)]
        wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
        self.grid = wx.GridSizer(rows=3, cols=3, hgap=3, vgap=3)
        self.cell = []
        for i in range(3*3):
            self.cell.append(Options(self, self.id*10+i))
            self.grid.Add(self.cell[i], 0, wx.EXPAND)
        self.SetSizer(self.grid)

    def determine_cell(self, event):
        """"""
        possibility_id = event.GetId()
        option_id, cell_no = divmod(possibility_id, 10)
        square_id, cell_id = divmod(option_id, 10)
        bold_bool = self.parent.startManual.GetValue()
        self.determined_cells[cell_id] = DeterminedCell(self, option_id, cell_no, bold_bool)
        self.grid.Hide(cell_id)
        self.grid.Detach(cell_id)
        self.grid.Insert(cell_id, self.determined_cells[cell_id])
        self.grid.Layout()
        self.determined_cells[cell_id].Bind(wx.EVT_BUTTON, self.parent.grid.undetermine_cell)
        self.determined_cells[cell_id].Bind(wx.EVT_BUTTON, self.undetermine_cell)
        event.ResumePropagation(2)
        event.Skip()
#            self.determined_cells[cell_id].SetBackgroundColour(wx.Colour(255, 0, 0))
#            print(tmp)

    def undetermine_cell(self, event):
        """"""
        option_id = event.GetId()
        cell_id = option_id % 10
        self.grid.Hide(cell_id)
        self.grid.Remove(cell_id)
        self.determined_cells[cell_id].DestroyLater()
        self.determined_cells[cell_id] = None
        self.grid.Insert(cell_id, self.cell[cell_id])
        self.grid.Show(cell_id, True)
        self.grid.Layout()
    #        self.grid.Fit(self)
        event.Skip()

    def reset_determine_cells(self):
        for single_det_cell in self.determined_cells:
            if single_det_cell is not None:
                self.reset_determine_cell(single_det_cell)

    @staticmethod
    def reset_determine_cell(single_det_cell):
        determined_cell_id = single_det_cell.GetId()
        event = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, determined_cell_id)
        wx.PostEvent(single_det_cell, event)

    def enable_all(self, state):
        [singleCell.enable_all(state) for singleCell in self.cell]

    def toggle_all(self, state):
        [singleCell.toggle_all(state) for singleCell in self.cell]

    def disable_all_init_cells(self):
        [single_det_cell.Disable() for single_det_cell in self.determined_cells if single_det_cell is not None]

    def show_error(self, cell_id, show):
        self.grid.GetItem(cell_id).GetWindow().show_error(show)

    def get_cell(self, cell_id):
        return self.determined_cells[cell_id]
