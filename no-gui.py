from numpy import *


def solve_sudoku(grid):
    cell = empty(grid)
    if not cell:
        return True
    else:
        r, c = cell

    for i in range(1, 10):
        if valid(grid, i, (r, c)):
            grid[r][c] = i
            if solve_sudoku(grid):
                return True
            grid[r][c] = 0
    return False


def valid(grid, num, pos):

    for i in range(9):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(9):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False

    box1 = pos[1] // 3
    box2 = pos[0] // 3

    for i1 in range(box2*3, box2*3 + 3):

        for i2 in range(box1*3, box1*3 + 3):
            if grid[i1][i2] == num and (i1, i2) != pos:
                return False

    return True


def print_sudoku(grid):

    for r in range(9):
        if r in [0, 3, 6, 9]:
            print('- - - - - - - - - - -')

        for c in range(9):
            if c in [3, 6]:
                print('| ', end='')
            if c == 8:
                print(grid[r][c])
            else:
                print('{} '.format((grid[r][c])), end='')

    print('- - - - - - - - - - -')


def empty(grid):

    for r in range(9):

        for c in range(9):
            if grid[r][c] == 0:
                return (r, c)

    return None


sudoku = zeros((9, 9), dtype=int)

for r in range(9):
    print('Row {}:'.format(r + 1))
    s = input()
    l = s.split()
    sudoku[r] = [int(e) for e in l]

print('\nThe input sudoku is:\n')
print_sudoku(sudoku)
solve_sudoku(sudoku)
print('\nThe solved sudoku is:\n')
print_sudoku(sudoku)
