from itertools import repeat, product
import wx
from time import sleep


class Grid(list):
    """"""
    def __init__(self, panel):
        """"Constructor"""
        list.__init__(self, repeat(None, 9*9))
        tmp = list(product(range(9), repeat=2))
        self.coordinate_list = []
        for j in (0, 27, 54):
            for i in (0, 3, 6):
                self.coordinate_list += tmp[j+i:j+i+3]+tmp[j+i+9:j+i+12]+tmp[j+i+18:j+i+21]
        self.panel = panel

    def reset(self):
        self[:] = repeat(None, 9*9)

    def test(self):
        [print(self[i*9: i*9+9]) for i in range(9)]
        print('------------')
        self.get_square(0)

    def get_row(self, row):
        return self[row: row+9]

    def get_col(self, col):
        return self[col::9]

    def get_square(self, square_id):
        tmp = [(square_id, j) for j in range(9)]
        tmp2 = [self.coordinate_list.index(x) for x in tmp]
        return [self[x] for x in tmp2]

    def coordinates(self, option_id):
        square_id, cell_id = divmod(option_id, 10)
        return self.coordinate_list.index((square_id, cell_id))

    def determine_cell(self, possibility_id):
        option_id, cell_no = divmod(possibility_id, 10)
        self[self.coordinates(option_id)] = cell_no
#        sleep(1)
#        self.squares[square_id].determined_cells[cell_id].SetForegroundColour(wx.Colour(255, 0, 0))
        self.panel.show_error(option_id)
        print('dddddddddddddddddd')

    def undetermine_cell(self, option_id):
        self[self.coordinates(option_id)] = None
