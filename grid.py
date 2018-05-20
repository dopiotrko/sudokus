from itertools import repeat, product, compress
import wx
from time import sleep


class Grid(list):
    """"""
    def __init__(self, panel, parent_grid=None):
        """"Constructor"""
        if parent_grid is None:
            list.__init__(self, repeat(None, 9*9))
            self.options = [0b111111111 for i in range(81)]
        else:
            list.__init__(self, parent_grid)
            self.options = list(parent_grid.options)

        self.parent_grid = parent_grid
        self.child_grid = None
        tmp = list(product(range(9), repeat=2))
        self.coordinate_list = []
        for j in (0, 27, 54):
            for i in (0, 3, 6):
                self.coordinate_list += tmp[j+i:j+i+3]+tmp[j+i+9:j+i+12]+tmp[j+i+18:j+i+21]
        self.panel = panel

    def get_last(self):
        if self.child_grid is None:
            return self
        else:
            return self.child_grid.get_last()

    def test(self):
        [print(self[i*9: i*9+9]) for i in range(9)]
        print('------------')
        tmp = ["{0:09b}".format(i) for i in self.options]
        [print(tmp[i*9: i*9+9]) for i in range(9)]

    def get_row(self, row):
        return self[row * 9: row * 9 + 9]

    def get_col(self, col):
        return self[col::9]

    def get_square(self, square_id):
        square_co = self.get_square_co(square_id)
        return [self[x] for x in square_co]

    def get_square_co(self, square_id):
        tmp = [(square_id, j) for j in range(9)]
        return [self.coordinate_list.index(x) for x in tmp]

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

    def determine_grid(self, possibility_id):
        option_id, cell_no = divmod(possibility_id, 10)
        square_id, cell_id = divmod(option_id, 10)
        possibility_id = (square_id, cell_id, cell_no)
        option_id = possibility_id[:2]
        if self.validate(possibility_id):
            grid = self.add_grid(option_id, cell_no)
            grid.update_options(option_id, cell_no)
        else:
            self.panel.undetermine_cell(option_id)
        self.get_last().test()
#        self.try_and_check_solve()

    def add_grid(self, option_id, cell_no=None):
        self.child_grid = Grid(self.panel, self)
        grid_co = self.panel_to_grid_co(option_id)
        last = self.get_last()
        last[grid_co] = cell_no
        return last

    def undetermine_grid(self, possibility_id):
        option_id = possibility_id[:2]
        grid = self.add_grid(option_id)
        grid.calculate_options()
        grid.test()
        print('qqq')

    def calculate_options(self):
        self.options = [0b111111111 for i in range(81)]
        for i in range(81):
            if self[i] is not None:
                option_id = self.grid_to_panel_co(i)
                self.update_options(option_id, self[i])

    def update_options(self, option_id, cell_no):  # aktualizuje options o zmiany w pojedyńczym ruchu
        square_id, cell_id = option_id
        square_co = self.get_square_co(square_id)
        cell_no_bite = 0b111111111-(1 << cell_no)
        for x in square_co:
            self.options[x] &= cell_no_bite
        col_no = self.get_col_no(option_id)
        self.options[col_no::9] = [cell_no_bite & tmp for tmp in self.options[col_no::9]]
        row_no = self.get_row_no(option_id)
        self.options[row_no * 9: row_no * 9 + 9] = [cell_no_bite & i for i in self.options[row_no * 9: row_no * 9 + 9]]

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
