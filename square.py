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
        square_id = int(possibility_id / 100)
        cell_id = int((possibility_id-square_id*100) / 10)
        cell_no = possibility_id % 10
        bold_bool = self.parent.startManual.GetValue()
        if not self.validate(cell_id, cell_no):
            self.determined_cells[cell_id] = DeterminedCell(self, cell_id, cell_no, bold_bool)
            self.grid.Hide(cell_id)
            self.grid.Detach(cell_id)
            self.grid.Insert(cell_id, self.determined_cells[cell_id])
            self.determined_cells[cell_id].Bind(wx.EVT_BUTTON, self.undetermine_cell)
            self.grid.Layout()

    def undetermine_cell(self, event):
        """"""
        cell_id = event.GetId()
        self.grid.Hide(cell_id)
        self.grid.Remove(cell_id)
        self.determined_cells[cell_id] = None
        self.grid.Insert(cell_id, self.cell[cell_id])
        self.grid.Show(cell_id, True)
        self.grid.Layout()
    #        self.grid.Fit(self)

    def reset_determine_cells(self):
        for single_det_cell in self.determined_cells:
            if single_det_cell is not None:
                determined_cell_id = single_det_cell.GetId()
                event = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, determined_cell_id)
                wx.PostEvent(single_det_cell, event)

    def enable_all(self, state):
        [singleCell.enable_all(state) for singleCell in self.cell]

    def toggle_all(self, state):
        [singleCell.toggle_all(state) for singleCell in self.cell]

    def disable_all_init_cells(self):
        [single_det_cell.Disable() for single_det_cell in self.determined_cells if single_det_cell is not None]

    def check_for_repetition_in_square(self, cell_no):
        # sprawdza czy mamy już zdefiniowaną cyfre 'init_no' w danym kwadracie, jeśli tak to zwraca True
        list_of_det_cells = [single_det_cell.get_int_label() for single_det_cell in self.determined_cells
                             if single_det_cell is not None]
        if cell_no+1 in list_of_det_cells:
            return True
        return False

    @staticmethod
    def get_line_ids(init_id):
        if init_id in [0, 1, 2]:
            return [0, 1, 2]
        if init_id in [3, 4, 5]:
            return [3, 4, 5]
        if init_id in [6, 7, 8]:
            return [6, 7, 8]

    @staticmethod
    def get_col_ids(init_id):
        if init_id in [0, 3, 6]:
            return [0, 3, 6]
        if init_id in [1, 4, 7]:
            return [1, 4, 7]
        if init_id in [2, 5, 8]:
            return [2, 5, 8]

    def extract_line_from_square(self, cell_id):
        # zwraca zdefiniowene już cyfry, z tej linji z tego kwadratu
        return [self.determined_cells[i].get_int_label() for i in self.get_line_ids(cell_id)
                if self.determined_cells[i] is not None]

    def extract_col_from_square(self, cell_id):
        # zwraca zdefiniowene już cyfry, z tej linji z tego kwadratu
        return [self.determined_cells[i].get_int_label() for i in self.get_col_ids(cell_id)
                if self.determined_cells[i] is not None]

    def check_for_repetition_in_line(self, cell_id, cell_no):
        tmp = self.parent.extract_entire_line(self.id, cell_id)
        if cell_no+1 in tmp:
            return True
        return False

    def check_for_repetition_in_col(self, cell_id, cell_no):
        tmp = self.parent.extract_entire_col(self.id, cell_id)
        if cell_no+1 in tmp:
            return True
        return False

    def validate(self, cell_id, cell_no):
        return self.check_for_repetition_in_line(cell_id, cell_no) or \
               self.check_for_repetition_in_square(cell_no) or \
               self.check_for_repetition_in_col(cell_id, cell_no)
