from itertools import repeat, product, compress, starmap
from time import sleep
import numpy as n
from exceptions import *


class Grid(list):
    """"""
    tmp = list(product(range(9), repeat=2))
    coordinate_list = []
    for j in (0, 27, 54):
        for i in (0, 3, 6):
            coordinate_list += tmp[j+i:j+i+3]+tmp[j+i+9:j+i+12]+tmp[j+i+18:j+i+21]
    del tmp

    def __init__(self, panel, parent_grid=None):
        """"Constructor"""
        if parent_grid is None:
            list.__init__(self, repeat(None, 9*9))
            self.options = n.ones((9, 9, 9), dtype=bool)
        else:
            list.__init__(self, parent_grid)
            self.options = parent_grid.options.copy()

        self.parent_grid = parent_grid
        self.child_grid = None
        self.panel = panel

    def get_last(self):
        if self.child_grid is None:
            return self
        else:
            return self.child_grid.get_last()

    def test(self):
        print('------------')
        [print(self[i*9: i*9+9]) for i in range(9)]
        tmp1 = self.options.astype(int)
        for j in range(9):
            [print(tmp1[j, i], end=' ') for i in range(9)]
            print('')
        print('################')
#        tmp = ["{0:09b}".format(i) for i in self.options]
#        [print(tmp[i*9: i*9+9]) for i in range(9)]

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
        square_id, cell_id, cell_no = possibility_id
        option_id = possibility_id[:2]
        if self.validate(possibility_id):
            grid = self.add_grid(option_id, cell_no)
            grid.update_options(option_id, cell_no)
        else:
            self.panel.undetermine_cell(option_id)
#        self.try_and_check_solve()
        current_grid = self.get_last()
        try:
            current_grid.solve()
        except SolvingError:
            current_grid.show_errors((option_id,))
            current_grid.panel.undetermine_cell(option_id)
            current_grid.parent_grid.child_grid = None

        current_grid = self.get_last()
        current_grid.test()
        pass

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
        self.get_last().solve()
#        grid.test()
        print('qqq')

    def calculate_options(self):
        self.options[:] = True
        for i in range(81):
            if self[i] is not None:
                option_id = self.grid_to_panel_co(i)
                self.update_options(option_id, self[i])

    def update_options(self, option_id, cell_no):  # aktualizuje options o zmiany w pojedyńczym ruchu
        square_id, cell_id = option_id
        square_co = self.get_square_co(square_id)
        col_no = self.get_col_no(option_id)
        row_no = self.get_row_no(option_id)
        self.options[:, col_no, cell_no] = False
        self.options[row_no, :, cell_no] = False
        self.options[row_no, col_no, :] = False
        flatted_options = self.options.view()
        flatted_options.shape = -1, 9
        flatted_options[square_co, cell_no] = False

    def validate(self, possibility_id):
        square_id, cell_id, cell_no = possibility_id
        errors = self.find_repetitions(possibility_id)

        if len(errors) == 0:
            return True
        errors.append((square_id, cell_id))
        errors = set(errors)
        self.show_errors(errors)

        return False

    def show_errors(self, errors):
        for x in errors:
            self.panel.show_error(x, True)
        sleep(.2)
        for x in errors:
            self.panel.show_error(x, False)

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
#               print(index)
#                solving.test()
            if i < 0:
                print('nie ma rozwiązania')
                break
#        solving.test()
        print('TryAndCheck Solved')
        del solving

    def solve(self):
        current_grid = Grid(self.panel, self)
        current_grid.parent_grid = None
        current_grid.solve_step()

    def solve_step(self, redo=False):
        resized_options = self.options.view()
        resized_options.shape = 3, 3, 3, 3, 9
        square_sum = n.sum(resized_options, (1, 3))
        square_sum.shape = 9, 9
        row_sum = n.sum(self.options, 0)
        col_sum = n.sum(self.options, 1)
        cell_sum = n.sum(self.options, 2)
        zeros = (square_sum == 0).sum(), (row_sum == 0).sum(), (col_sum == 0).sum(), (cell_sum == 0).sum()
        determined_count = 81 - self.count(None)
        if determined_count == 81:
            #  raise Solved('Solved')
            print('Solved')
            self.test()
            return
        if zeros != tuple([determined_count] * 4):
            print('solving impossible, back one or more moves, and try again ')
            try:
                self.parent_grid.solve_step(redo=True)
                return
            except AttributeError:
                raise SolvingError('solving impossible, back one or more moves, and try again ')

        try:
            square_id, cell_id, cell_no = self.find_determined(square_sum, row_sum, col_sum, cell_sum)
            grid_co = self.panel_to_grid_co((square_id, cell_id))
            self[grid_co] = cell_no
            self.update_options((square_id, cell_id), cell_no)

            # drukuj
#            border = n.full((9, 1), None)
#            print('det')
#            self.test()
#            print(n.hstack((row_sum, border, col_sum, border, cell_sum, border)))

            self.solve_step()
        except FindFailed:

            row_no, col_no = n.where(cell_sum == n.amin(cell_sum[n.nonzero(cell_sum)]))
            row_no, col_no = row_no[0], col_no[0]
            grid_co = 9 * row_no + col_no
            cell_no = n.nonzero(self.options[row_no, col_no, :])[0]
            if redo:
                incorrect_cell_no = self.child_grid[grid_co]
                self.child_grid = None
                try:
                    cell_no = cell_no.item(Grid.find_first_index(incorrect_cell_no, cell_no)+1)
                except IndexError:
                    self.parent_grid.solve_step(redo=True)
                    return
            else:
                cell_no = cell_no.item(0)
            option_id = self.grid_to_panel_co(grid_co)
            grid = self.add_grid(option_id, cell_no)
            grid.update_options(option_id, cell_no)

            # drukuj
#            border = n.full((9, 1), None)
#            print('undet')
#            grid.test()
#            print(n.hstack((row_sum, border, col_sum, border, cell_sum, border)))

            grid.solve_step()

    def find_determined(self, square_sum, row_sum, col_sum, cell_sum):

        row_no, col_no, cell_no = 0, 0, 0
        for i in (1, 2):
            if i is 2:
                grid_co = 9 * row_no + col_no
                square_id, cell_id = self.grid_to_panel_co(grid_co)
                break
            tmp = row_sum == 1
            if n.any(tmp):
                col_no, cell_no = n.where(tmp)
                col_no, cell_no = col_no[0], cell_no[0]
                row_no = n.where(self.options[:, col_no, cell_no].flatten())[0][0]
                continue

            tmp = col_sum == 1
            if n.any(tmp):
                row_no, cell_no = n.where(tmp)
                row_no, cell_no = row_no[0], cell_no[0]
                col_no = n.where(self.options[row_no, :, cell_no].flatten())[0][0]
                continue

            tmp = cell_sum == 1
            if n.any(tmp):
                row_no, col_no = n.where(tmp)
                row_no, col_no = row_no[0], col_no[0]
                cell_no = n.where(self.options[row_no, col_no, :].flatten())[0][0]
                continue

            tmp = square_sum == 1
            if n.any(tmp):
                square_id, cell_no = n.where(tmp)
                square_id, cell_no = square_id[0], cell_no[0]
                square_x, square_y = divmod(square_id, 3)
                resized_options = self.options.view()
                resized_options.shape = 3, 3, 3, 3, 9
                cell_id = n.where(resized_options[square_x, :, square_y, :, cell_no].flatten())[0][0]
                break

            raise FindFailed('did not find any determined')
        return square_id, cell_id, int(cell_no)

    @staticmethod
    def find_first_index(item, vec):
        """return the index of the first occurence of item in vec"""
        for i in range(len(vec)):
            if item == vec[i]:
                return i
        raise FindFailed('Find_firs_index failed')
