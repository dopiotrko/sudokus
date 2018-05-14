from itertools import repeat, product, compress
import wx
from square import *
from time import sleep


class Grid(list):
    """"""
    def __init__(self, panel, parent_grid=None):
        """"Constructor"""
        if parent_grid is None:
            list.__init__(self, repeat(None, 9*9))
            self.options = [[True] * 9 for i in range(81)]
        else:
            list.__init__(self, parent_grid)
            self.options = list(parent_grid.options)

        tmp = list(product(range(9), repeat=2))
        self.coordinate_list = []
        for j in (0, 27, 54):
            for i in (0, 3, 6):
                self.coordinate_list += tmp[j+i:j+i+3]+tmp[j+i+9:j+i+12]+tmp[j+i+18:j+i+21]
        self.panel = panel

    def reset(self):
        self[:] = repeat(None, 9*9)
        self.options = [[True] * 9 for i in range(81)]

    def test(self):
        [print(self[i*9: i*9+9]) for i in range(9)]
        print('------------')
        [print(self.options[i*9: i*9+9]) for i in range(9)]

    def get_row(self, row):
        return self[row * 9: row * 9 + 9]

    def get_col(self, col):
        return self[col::9]

    def get_square(self, square_id):
        tmp = [(square_id, j) for j in range(9)]
        tmp2 = [self.coordinate_list.index(x) for x in tmp]
        return [self[x] for x in tmp2]

    def panel_to_grid_co(self, option_id):
        return self.coordinate_list.index(option_id)

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
        square_id, cell_id = divmod(option_id, 10)
        possibility_id = (square_id, cell_id, cell_no)
        option_id = possibility_id[:2]
        if self.validate(possibility_id):
            grid_co = self.panel_to_grid_co(option_id)
            self[grid_co] = cell_no
#           self.update_options(option_id, False)
        else:
            cell = self.panel.get_cell(option_id)
            Square.reset_determine_cell(cell)
        self.test()
        self.try_and_check_solve()

    def undetermine_cell(self, event):
        option_id = divmod(event.GetId(), 10)
        self[self.panel_to_grid_co(option_id)] = None
        self.update_options(option_id, True)

    def update_options(self, option_id, state): #TODO całkowicie do wymiany
        square_id, cell_id = option_id
        self.square_options[square_id][cell_id] = state
        row_no = self.get_row_no(option_id)
        col_no = self.get_col_no(option_id)
        self.row_options[row_no][col_no] = state
        self.col_options[col_no][row_no] = state
        self.options[grid_co][cell_no] = False

    def validate(self, possibility_id):
        square_id, cell_id, cell_no = possibility_id
        errors = self.find_repetitions(possibility_id)

        if len(errors) == 0:
            return True
        errors.append((square_id, cell_id))
        errors = set(errors)
        for x in errors:
            self.panel.show_error(x, True)
        sleep(.2)
        for x in errors:
            self.panel.show_error(x, False)

        return False

    def find_repetitions(self, possibility_id):
        square_id, cell_id, cell_no = possibility_id
        errors = []
        try:
            index = self.get_square(square_id).index(cell_no)
            errors.append((square_id, index))
        except ValueError:
            pass
        row_no = self.get_row_no(possibility_id[:2])
        try:
            index = self.get_row(row_no).index(cell_no)
            tmp = self.grid_to_panel_co(row_no * 9 + index)
            errors.append(tmp)
        except ValueError:
            pass
        col_no = self.get_col_no(possibility_id[:2])
        try:
            index = self.get_col(col_no).index(cell_no)
            tmp = self.grid_to_panel_co(index * 9 + col_no)
            errors.append(tmp)
        except ValueError:
            pass
        return errors

    def try_and_check_solve(self):
        i = 0
        solving = Grid(self.panel, self)
        empty_cells = [tmp for tmp in range(81) if solving[tmp] is None]
        while i < len(empty_cells):
            index = empty_cells[i]
            co = self.grid_to_panel_co(index)
            k = solving[index]
            if k is None:
                k = 0
            else:
                k += 1
            solving[index] = None
            for j in range(k, 9):
                if len(solving.find_repetitions((co[0], co[1], j))) == 0:
                    solving[index] = j
                    i += 1
                    break
            else:
                i -= 1
                print(index)
                solving.test()
            if i < 0:
                print('nie ma rozwiązania')
                break
        solving.test()
        del solving
