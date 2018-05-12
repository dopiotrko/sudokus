from itertools import repeat, product
import wx
from square import *
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
        return self[row * 9: row * 9 + 9]

    def get_col(self, col):
        return self[col::9]

    def get_square(self, square_id):
        tmp = [(square_id, j) for j in range(9)]
        tmp2 = [self.coordinate_list.index(x) for x in tmp]
        return [self[x] for x in tmp2]

    def panel_to_grid_co(self, option_id):
        square_id, cell_id = divmod(option_id, 10)
        return self.coordinate_list.index((square_id, cell_id))

    def grid_to_panel_co(self, index):
        return self.coordinate_list[index]

    def xy_coordinates(self, option_id):
        return divmod(self.panel_to_grid_co(option_id), 9)

    def get_row_no(self, option_id):
        return self.xy_coordinates(option_id)[0]

    def get_col_no(self, option_id):
        return self.xy_coordinates(option_id)[1]

    def determine_cell(self, possibility_id):
        option_id, cell_no = divmod(possibility_id, 10)
        if self.validate(option_id, cell_no):
            self[self.panel_to_grid_co(option_id)] = cell_no
        else:
            cell = self.panel.get_cell(option_id)
            Square.reset_determine_cell(cell)

    def undetermine_cell(self, option_id):
        self[self.panel_to_grid_co(option_id)] = None

    def validate(self, option_id, cell_no):
        square_id, cell_id = divmod(option_id, 10)
        errors = []
        try:
            index = self.get_square(square_id).index(cell_no)
            errors.append((square_id, index))
        except ValueError:
            pass

        row_no = self.get_row_no(option_id)
        try:
            index = self.get_row(row_no).index(cell_no)
            tmp = self.grid_to_panel_co(row_no * 9 + index)
            errors.append(tmp)
        except ValueError:
            pass

        col_no = self.get_col_no(option_id)
        try:
            index = self.get_col(col_no).index(cell_no)
            tmp = self.grid_to_panel_co(index * 9 + col_no)
            errors.append(tmp)
        except ValueError:
            pass

        if len(errors) == 0:
            return True
        errors.append((square_id, cell_id))
        errors = set(errors)
        errors = [tmp[0]*10+tmp[1] for tmp in errors]
        for x in errors:
            self.panel.show_error(x, True)
        sleep(.2)
        for x in errors:
            self.panel.show_error(x, False)

        return False
