import pygame
import time

pygame.font.init()
fnt = pygame.font.SysFont("arial", 13)
img = pygame.image.load('icon.png')
bg = pygame.image.load('cute.jpg')
pygame.display.set_icon(img)

square_selected = None

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.squares = [[Square(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def draw(self):
        # Draw Squares
        for i in range(self.rows):
            for j in range(self.cols):
               self.squares[i][j].draw(self.win)
        # Draw Grid Lines
        lengthMinusOnePx = (self.width - 1) / 9
        for i in range(self.rows + 1):
            if i in [3, 6]:
                continue
            else:
                pygame.draw.line(self.win, (95, 95, 95), (0, i * lengthMinusOnePx), (self.width, i * lengthMinusOnePx), 3) #horizontal
                pygame.draw.line(self.win, (95, 95, 95), (i * lengthMinusOnePx, 0), (i * lengthMinusOnePx, self.height), 3) #vertical
        for i in range(self.rows + 1):
            if i in [3, 6]:
                pygame.draw.line(self.win, (0, 0, 0), (0, i * lengthMinusOnePx), (self.width, i * lengthMinusOnePx), 3) #horizontal
                pygame.draw.line(self.win, (0, 0, 0), (i * lengthMinusOnePx, 0), (i * lengthMinusOnePx, self.height), 3) #vertical
        #Draw Red Box
        if square_selected != None:
            y = square_selected.row * lengthMinusOnePx
            x = square_selected.col * lengthMinusOnePx
            pygame.draw.rect(self.win, (255, 0, 0), (x + 2, y + 2, lengthMinusOnePx - 3, lengthMinusOnePx - 3), 3)
                

    def select(self, row, col):
        # Reset all other
        global square_selected
        if square_selected != None:
            square_selected.selected = False

        self.squares[row][col].selected = True
        square_selected = self.squares[row][col]
        self.selected = (row, col)
        
    def deselect(self, row, col):
        global square_selected
        if square_selected != None:
            square_selected.selected = False
            square_selected = None
        self.selected = None

    def clear(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            lengthMinusOnePx = (self.width - 1) / 9
            x = pos[0] // lengthMinusOnePx
            y = pos[1] // lengthMinusOnePx
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.squares[row][col].set(i)
                self.squares[row][col].green = True
                redraw_window(self.win, self, play_time, True)
                pygame.display.update()
                pygame.time.delay(10)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.squares[row][col].set(0)
                self.squares[row][col].green = False
                redraw_window(self.win, self, play_time, True)
                pygame.display.update()
                pygame.time.delay(10)

        return False
    
    def instructions(self):
        text1 = fnt.render('Press: R to Reset, C to Clear, Space to Solve', 1, (0, 0, 255), (255, 255, 255))
        text2 = fnt.render('& Hold D for Sudoku Doggy', 1, (0, 0, 255), (255, 255, 255))
        text3 = fnt.render('Enter Values', 1, (0, 0, 255), (255, 255, 255))
        self.win.blit(text1, (20, 525))
        self.win.blit(text2, (20, 545))
        self.win.blit(text3, (20, 565))

    def ungreen(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].green = False


class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.green = False

    def draw(self, win):

        lengthMinusOnePx = (self.width - 1) / 9
        x = self.col * lengthMinusOnePx
        y = self.row * lengthMinusOnePx

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (95, 95, 95))
            win.blit(text, (x + (lengthMinusOnePx - text.get_width()) / 2, y + (lengthMinusOnePx - text.get_height()) / 2))
        
        elif self.value != 0:
            #render purple
            pygame.draw.rect(win, (127, 127, 255), (x + 2, y + 2, lengthMinusOnePx - 3, lengthMinusOnePx - 3), 0)
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (lengthMinusOnePx - text.get_width()) / 2, y + (lengthMinusOnePx - text.get_height()) / 2))

        if self.green == True:
            pygame.draw.rect(win, (0, 255, 0), (x + 2, y + 2, lengthMinusOnePx - 3, lengthMinusOnePx - 3), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(model):
    for i in range(len(model)):
        for j in range(len(model[0])):
            if model[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(model, num, pos):
    # Check row
    for i in range(len(model[0])):
        if model[pos[0]][i] == num and i != pos[1]:
            return False

    # Check column
    for i in range(len(model)):
        if model[i][pos[1]] == num and i != pos[0]:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if model[i][j] == num and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, trans):
    if trans == True:
        win.blit(bg, (0, 0))
    else:
        win.fill((255, 255, 255))
    # Draw time
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 255))
    win.blit(text, (505 - 110, 525))
    # Draw instructions
    board.instructions()
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60

    s = " " + f"{minute:02}" + ":" + f"{sec:02}" + " "
    return s


def main():
    win = pygame.display.set_mode((505, 600))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 505, 505, win)
    key = None
    run = True
    start = time.time()
    change = 0
    green = 0
    redraw_window(win, board, 0, False)
    pygame.display.update()
    clock = pygame.time.Clock()
    while run:
        
        clock.tick(10)
        global play_time
        play_time = round(time.time() - start)
        text = fnt.render("Time: " + format_time(play_time) + " ", 1, (0, 0, 255), (255, 255, 255))
        win.blit(text, (505 - 110, 525))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                    change = 1
                if event.key == pygame.K_2:
                    key = 2
                    change = 1
                if event.key == pygame.K_3:
                    key = 3
                    change = 1
                if event.key == pygame.K_4:
                    key = 4
                    change = 1
                if event.key == pygame.K_5:
                    key = 5
                    change = 1
                if event.key == pygame.K_6:
                    key = 6
                    change = 1
                if event.key == pygame.K_7:
                    key = 7
                    change = 1
                if event.key == pygame.K_8:
                    key = 8
                    change = 1
                if event.key == pygame.K_9:
                    key = 9
                    change = 1
                if event.key == pygame.K_KP1:
                    key = 1
                    change = 1
                if event.key == pygame.K_KP2:
                    key = 2
                    change = 1
                if event.key == pygame.K_KP3:
                    key = 3
                    change = 1
                if event.key == pygame.K_KP4:
                    key = 4
                    change = 1
                if event.key == pygame.K_KP5:
                    key = 5
                    change = 1
                if event.key == pygame.K_KP6:
                    key = 6
                    change = 1
                if event.key == pygame.K_KP7:
                    key = 7
                    change = 1
                if event.key == pygame.K_KP8:
                    key = 8
                    change = 1
                if event.key == pygame.K_KP9:
                    key = 9
                    change = 1
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                    change = 1
                if event.key == pygame.K_SPACE:
                    redraw_window(win, board, 0, True)
                    pygame.display.update()
                    board.solve_gui()
                    green = 1
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.place(board.squares[i][j].temp):
                            lengthMinusOnePx = (505 - 1) / 9
                            
                            x = j * lengthMinusOnePx
                            y = i * lengthMinusOnePx
                            
                            pygame.draw.rect(win, (127, 127, 255), (x + 2, y + 2, lengthMinusOnePx - 3, lengthMinusOnePx - 3), 0)
                            text = fnt.render(str(board.squares[i][j].temp), 1, (0, 0, 0))
                            win.blit(text, (x + (lengthMinusOnePx - text.get_width()) / 2, y + (lengthMinusOnePx - text.get_height()) / 2))
                            
                            text = fnt.render("Success", 1, (0, 0, 255))
                            win.blit(text, (505 - 81, 545))
                       
                        if board.is_finished():
                            text = fnt.render("Finished", 1, (0, 0, 255))
                            win.blit(text, (505 - 82, 565))
                    key = None
                    pygame.display.update()
                if event.key == pygame.K_r:
                    board.squares = [[Square(board.board[i][j], i, j, 505, 505) for j in range(9)] for i in range(9)]
                    board.update_model()
                    change = 1
                if event.key == pygame.K_c:
                    board.squares = [[Square(0, i, j, 505, 505) for j in range(9)] for i in range(9)]
                    change = 1
                if event.key == pygame.K_d:
                    win.blit(bg, (0, 0))
                    pygame.display.update()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    change = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked and clicked != board.selected:
                    board.select(clicked[0], clicked[1])
                    key = None
                    change = 1
                elif clicked and clicked == board.selected:
                    board.deselect(clicked[0], clicked[1])
                    key = None
                    change = 1

        if board.selected and key != None:
            board.sketch(key)
            change = 1

        if change == 1:
            if green == 1:
                board.ungreen()
            redraw_window(win, board, play_time, False)
            pygame.display.update()
            change = 0

main()
pygame.quit()
