from itertools import repeat, product
from time import sleep
import numpy as n
from exceptions import *


class Grid(list):
    """Solving/validating class"""
    tmp = list(product(range(9), repeat=2))
    coordinate_list = []
    for j in (0, 27, 54):
        for i in (0, 3, 6):
            coordinate_list += tmp[j+i:j+i+3]+tmp[j+i+9:j+i+12]+tmp[j+i+18:j+i+21]
    solve_count = 0
    del tmp
    block_errors = True
    one_solution_only = False
    solution = None

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
        """Returning last element from stack of Grid class"""
        if self.child_grid is None:
            return self
        else:
            return self.child_grid.get_last()

    def test(self):
        """Printing class data for debugging purposes"""
        print('------------')
        [print(self[i*9: i*9+9]) for i in range(9)]
        tmp1 = self.options.astype(int)
        for j in range(9):
            [print(tmp1[j, i], end=' ') for i in range(9)]
            print('')
        print('################')

    def get_row(self, row):
        """Returning specified row of solving grid"""
        return self[row * 9: row * 9 + 9]

    def get_col(self, col):
        """Returning specified column of solving grid"""
        return self[col::9]

    def get_square(self, square_id):
        """Returning data from specified 9x9 square from solving grid"""
        square_co = self.get_square_co(square_id)
        return [self[x] for x in square_co]

    def get_square_co(self, square_id):
        """Returning coordinates of data of specified 9x9 square in solving grid"""
        tmp = [(square_id, j) for j in range(9)]
        return [self.coordinate_list.index(x) for x in tmp]

    def panel_to_grid_co(self, option_id):
        """Translating GUI coordinates (square-cell) to Grid coordinates"""
        return self.coordinate_list.index(option_id)

    def grid_to_panel_co(self, index):
        """Translating Grid coordinates to GUI coordinates(square-cell)"""
        return self.coordinate_list[index]

    def xy_coordinates(self, option_id):
        """Translate GUI coordinates (square-cell) to row-col coordinates"""
        return divmod(self.panel_to_grid_co(option_id), 9)

    def get_row_no(self, option_id):
        """Calculating row from GUI coordinates"""
        return self.xy_coordinates(option_id)[0]

    def get_col_no(self, option_id):
        """Calculating column from GUI coordinates"""
        return self.xy_coordinates(option_id)[1]

    def determine_grid(self, possibility_id):
        """In every move: Updating data/algorytm validating/solving the moves in game"""
        square_id, cell_id, cell_no = possibility_id
        option_id = possibility_id[:2]
        if (not self.block_errors) or self.validate(possibility_id):
            grid = self.add_grid(option_id, cell_no)
            grid.update_options(option_id, cell_no)
            current_grid = self.get_last()
            if self.block_errors:
                try:
                    current_grid.solve()
                except SolvingError:
                    current_grid.show_errors((option_id,))
                    current_grid.panel.undetermine_cell(option_id)
                    current_grid.parent_grid.child_grid = None
        else:
            self.panel.undetermine_cell(option_id)

        current_grid = self.get_last()
#        current_grid.test()
#        print(self.solution)

    def add_grid(self, option_id, cell_no=None):
        """Addidng new Grid to stack: storing user moves (after determine of cell) in stack"""
        self.child_grid = Grid(self.panel, self)
        grid_co = self.panel_to_grid_co(option_id)
        last = self.get_last()
        last[grid_co] = cell_no
        return last

    def undetermine_grid(self, option_id):
        """Addidng new Grid to stack: storing user moves (after undetermine of cell) in stack"""
        grid = self.add_grid(option_id)
        grid.calculate_options()
        self.get_last().solve()
#        grid.test()

    def calculate_options(self):
        """recalculating options grid from the scratch. Necessary after deleting determined cell"""
        self.options[:] = True
        for i in range(81):
            if self[i] is not None:
                option_id = self.grid_to_panel_co(i)
                self.update_options(option_id, self[i])

    def update_options(self, option_id, cell_no):
        """Updating options gridon flow. After determine of every cell"""
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
        """Checking if newly determined cell is not colliding with other determined cell i row, column, or square"""
        square_id, cell_id, cell_no = possibility_id
        errors = self.find_repetitions(possibility_id)

        if len(errors) == 0:
            return True
        errors.append((square_id, cell_id))
        errors = set(errors)
        self.show_errors(errors)

        return False

    def show_errors(self, errors):
        """Showing collided numbers"""
        for x in errors:
            self.panel.show_error(x, True)
        sleep(.2)
        for x in errors:
            self.panel.show_error(x, False)

    def find_repetitions(self, possibility_id):
        """Checking for coordinates of cell colliding with each other in row, column, or square"""
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
        """Simple solving routine. Unused due to large solving time"""
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
        """Strats solving in new stack"""
        current_grid = Grid(self.panel, self)
        current_grid.parent_grid = None
        current_grid.solve_step()

    def solve_step(self, redo=False):
        """Recursiwly solving the game. Up to 5 different solutions (if exists)"""
        resized_options = self.options.view()
        resized_options.shape = 3, 3, 3, 3, 9
        square_sum = n.sum(resized_options, (1, 3))
        square_sum.shape = 9, 9
        row_sum = n.sum(self.options, 0)
        col_sum = n.sum(self.options, 1)
        cell_sum = n.sum(self.options, 2)
        zeros = (square_sum == 0).sum(), (row_sum == 0).sum(), (col_sum == 0).sum(), (cell_sum == 0).sum()

        """Checking if algoritm solved the game.
        If yes, asking to find up to 5 solutions, and return after success 
        If solution do not exists, raise SolvingError - catched in determine_grid method"""
        try:
            self.check_if_solved(zeros)
        except Return:
            return

        try:
            """determining cell, with can be determined in one way only (without adding another Grid to the stack)
            (if there is no such cell: raise FindFiled)"""
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
            """determining cell, with can by determined in many ways (adding Grid to the stack) [till line 280]"""
            row_no, col_no = n.where(cell_sum == n.amin(cell_sum[n.nonzero(cell_sum)]))
            row_no, col_no = row_no[0], col_no[0]
            grid_co = 9 * row_no + col_no
            cell_no = n.nonzero(self.options[row_no, col_no, :])[0]
            """if cell needs to be redefined 
            (because last version was dead end or we are looking for another solution)"""
            if redo:
                incorrect_cell_no = self.child_grid[grid_co]
                self.child_grid = None
                try:
                    cell_no = cell_no.item(Grid.find_first_index(incorrect_cell_no, cell_no)+1)
                except IndexError:
                    self.parent_grid.solve_step(redo=True)  # this version is dead end as well: so try again
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

    def check_if_solved(self, zeros):
        """Checking if algoritm solved the game.
        If yes, asking to find up to 2 solutions, and after success raise Return exception.
        If solution do not exists, raise SolvingError"""
        find_next_solution = False
        determined_count = 81 - self.count(None)
        if determined_count == 81:
            if self.solve_count < 1:
                self.__class__.solve_count += 1
                find_next_solution = True
            #           self.test()
            else:
                #  print('2 or more solution available')
                self.__class__.solve_count = 0
                raise Return
        if zeros != tuple([determined_count] * 4) or find_next_solution:
            try:
                self.parent_grid.solve_step(redo=True)
                raise Return
            except AttributeError:
                if self.solve_count is not 0:
                    print(self.solve_count, 'solutions available ')
                    if self.solve_count is 1:
                        self.__class__.solution = n.array(self)
                        self.__class__.one_solution_only = True
                    else:
                        self.__class__.one_solution_only = False
                    self.__class__.solve_count = 0
                    raise Return
                else:
                    raise SolvingError('solving impossible, back one or more moves, and try again ')

    def find_determined(self, square_sum, row_sum, col_sum, cell_sum):
        """Checking for coordinates of undetermined cell, with can be determined in one way only (if exist)"""

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

    def random_game(self):
        """Starting random game"""
        random_cells = n.random.permutation(self.coordinate_list)
        undetermined_count = 81
        determined_cell_list = []
        for cell in random_cells:
            for cell_no in n.random.permutation(range(9)):
                possibility_id = cell[0], cell[1], cell_no
                self.get_last().determine_grid(possibility_id)
                if undetermined_count != self.get_last().count(None):
                    determined_cell_list.append(possibility_id)
                    break
            if self.one_solution_only is True:
                break

        self.get_last().test()
        for cell in determined_cell_list:
            self.panel.determine_cell(cell)

