import pygame
import time

pygame.font.init()

screen = pygame.display.set_mode((500, 600))

# Title and Icon
pygame.display.set_caption('Sudoku Solver')
img = pygame.image.load('icon.png')
bg = pygame.image.load('cute.jpg')
pygame.display.set_icon(img)

x = 0
y = 0
gap = 500/9
val = 0
# Default Sudoku Board.
grid = [[0, 6, 0, 0, 7, 0, 0, 3, 0],
        [5, 0, 7, 6, 0, 1, 4, 0, 9],
        [0, 4, 0, 0, 8, 0, 0, 1, 0],

        [0, 0, 2, 7, 0, 4, 1, 0, 0],
        [0, 5, 1, 0, 2, 0, 7, 4, 0],
        [0, 0, 3, 9, 0, 6, 5, 0, 0],

        [0, 1, 0, 0, 9, 0, 0, 5, 0],
        [2, 0, 5, 3, 0, 7, 8, 0, 1],
        [0, 3, 0, 0, 6, 0, 0, 7, 0]]

# Load test fonts for future use
font = pygame.font.SysFont('arial', 13)
font2 = pygame.font.SysFont('arial', 20)


def setXY(pos):
    global x
    x = int(pos[0] // gap)
    global y
    y = int(pos[1] // gap)


# Highlight the cell selected
def red_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * gap, (y + i) * gap), (x * gap + gap, (y + i) * gap), 1) #top, bottom
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * gap, y * gap), ((x + i) * gap, y * gap + gap), 1) #left, right


# Function to draw required lines for making Sudoku grid
def draw():
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (101, 112, 110), (i * gap, j * gap, gap, gap))
                # Fill gird with default numbers specified
                text1 = font2.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * gap + 15, j * gap + 15))
            # Draw lines horizontally and vertically to form grid
    for i in range(10):
        if i in [3, 6]:
            thick = 7
        else:
            thick = 3
        pygame.draw.line(screen, (0, 0, 0), (0, i * gap), (500, i * gap), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * gap, 0), (i * gap, 500), thick)

    # Fill value entered in cell


def draw_val(val):
    text1 = font.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * gap + 15, y * gap + 15))


# Raise error when wrong value entered
def errorWrong():
    text1 = font.render('Wrong', 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


def errorInvalidKey():
    text1 = font.render('Invalid Key', 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    it = i//3
    jt = j//3
    for i in range(it*3, it*3 + 3):
        for j in range(jt*3, jt*3 + 3):
            if m[i][j] == val:
                return False
    return True


# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    while grid[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if valid(grid, i, j, it) == True:
            grid[i][j] = it
            global x, y
            x = i
            y = j
            #background
            #screen.fill((255, 255, 255))
            screen.blit(bg, (0, 0))
            draw()
            red_box()
            pygame.display.update()
            pygame.time.delay(20)
            if solve(grid, i, j) == 1:
                return True
            else:
                grid[i][j] = 0
            # white color background\
            #screen.fill((255, 255, 255))
            screen.blit(bg, (0, 0))

            draw()
            red_box()
            pygame.display.update()
            pygame.time.delay(50)
    return False


# Display instruction for the game
def instruction():
    text1 = font.render('Press: R to Reset, C to Clear, Return to Solve & Press D for Sudoku Doggy', 1, (0, 0, 0))
    text2 = font.render('Enter Values', 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))

run = True
red = 0
sol = 0
dog = 0

# The loop that keeps the window running
while run:

    # White color background
    screen.fill((255, 255, 255))
    #screen.blit(bg, (0, 0))
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False
        # Get the mouse postion to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            red = 1
            pos = pygame.mouse.get_pos()
            setXY(pos)
        # Get the number to be inserted if key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                red = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                red = 1
            if event.key == pygame.K_UP:
                y -= 1
                red = 1
            if event.key == pygame.K_DOWN:
                y += 1
                red = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                sol = 1
            # If C is pressed clear the sudoku board
            if event.key == pygame.K_c:
                sol = 0
                grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],

                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
            # If R is pressed reset the board to default
            if event.key == pygame.K_r:
                sol = 0
                grid = [[0, 6, 0, 0, 7, 0, 0, 3, 0],
                        [5, 0, 7, 6, 0, 1, 4, 0, 9],
                        [0, 4, 0, 0, 8, 0, 0, 1, 0],

                        [0, 0, 2, 7, 0, 4, 1, 0, 0],
                        [0, 5, 1, 0, 2, 0, 7, 4, 0],
                        [0, 0, 3, 9, 0, 6, 5, 0, 0],

                        [0, 1, 0, 0, 9, 0, 0, 5, 0],
                        [2, 0, 5, 3, 0, 7, 8, 0, 1],
                        [0, 3, 0, 0, 6, 0, 0, 7, 0]]
            if event.key == pygame.K_d:
                dog = 1


    if sol == 1:
        if solve(grid, 0, 0) == False:
            errorWrong()
        else:
            text1 = font.render('Done', 1, (0, 0, 0))
            screen.blit(text1, (20, 570))
        sol = 0
    if val != 0:
        draw_val(val)
        if valid(grid, x, y, val) == True:
            grid[x][y] = val
            red = 0
        else:
            grid[x][y] = 0
            errorInvalidKey()
        val = 0
    draw()
    if red == 1:
        red_box()
    instruction()
    if dog == 1:
        screen.blit(bg, (0, 0))
    pygame.display.update()

pygame.quit()
