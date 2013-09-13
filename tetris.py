# import pygame, sys
# from pygame.locals import *
import curses
import pdb
import random
import time

class Tetris():

    def __init__(self):
        self.board = [self.make_row() for i in range(23)]
        self.board.append([['obstacle', None, None] for i in range(12)])
        self.active_piece = None

    def make_row(self):
        return [['obstacle', None, None]] + [[None, None, None] for i in range(10)] + [['obstacle', None, None]]

    def draw_board_pygame(self):
        color_map = {
                    None : (0,0,0),
                    'J' : (255,255,255),
                    'L' : (255,0,0),
                    'line' : (0,255,0),
                    'T' : (0,0, 255),
                    'S' : (150,0,150),
                    'Z' : (0,150,150),
                    'box' : (255,255,0),
                    }

        DISPLAYSURF = pygame.display.set_mode((200,400),0,32)
        for i in range(3,23): #there are 24 rows total, 3 at the top and 1 at the bottom are NOT displayed
            for j in range(1,11): #there are 12 columns total, 1 on each side is NOT displayed
                y, x = i*20 - 60, j*20 - 20 #this maps to the coordinates being displayed, excluding borders
                piece_type = self.board[i][j][1]
                pygame.draw.rect(DISPLAYSURF, color_map[piece_type], (x,y,20,20))
        if self.you_lose():
            #print 'You lose!'
            pygame.font.init()
            myfont = pygame.font.SysFont('sawasdee', 30, bold=1)
            pygame.draw.rect(DISPLAYSURF, (125,125,125), (30,45,140,50))
            label = myfont.render('You lose!', 1, WHITE)
            DISPLAYSURF.blit(label, (40,50))
        pygame.display.update()

    def draw_board_terminal(self):
        out = []
        for i in range(3,23): #there are 24 rows total, 3 at the top and 1 at the bottom are NOT displayed
            row = ['o']
            for j in range(1,11): #there are 12 columns total, 1 on each side is NOT displayed
                if self.board[i][j][1] is not None:
                    row.append('xxx')
                else:
                    row.append('   ')
            row.append('o\n')
            out.append("".join(row))
            out.append("".join(row))
        out.append('o'*33)

        if self.you_lose():
            return "you lose!"

        return "".join(out)

    def pygame_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move('right')
            elif event.key == pygame.K_LEFT:
                self.move('left')
            elif event.key == pygame.K_DOWN:
                self.move('down')
            elif event.key == pygame.K_UP:
                self.rotate()

    def terminal_input(self, char):
        if char == 'A':
            self.rotate()
        elif char == 'B':
            self.move('down')
        elif char == 'C':
            self.move('right')
        elif char == 'D':
            self.move('left')
        elif char == 'p':
            time.sleep(60)

    def move(self, direction):
        # next_cell has (row, col) delta for next cell, depending on direction of movement
        next_cell = {
                     'right': (0, 1),
                     'left' : (0, -1),
                     'down' : (1, 0),
                    }
        r_delta, c_delta = next_cell[direction]
        column_order = {
                        'right': range(11,0,-1),
                        'left' : range(1, 11),
                        'down' : range(1, 11),
                        }

        obstacle_hit = False

        for row in range(22,-1,-1): #loop backwards from bottom to top - easier to check for obstacles
            for column in column_order[direction]:
                state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                if state == 'active' and self.board[row+r_delta][column+c_delta][0] == 'obstacle':
                    obstacle_hit = True

        if not obstacle_hit:
            for row in range(22,-1,-1):
                for column in column_order[direction]:
                    state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                    if state == 'active':
                        self.board[row][column] = [None, None, None]
                        self.board[row+r_delta][column+c_delta] = [state, piece_type, pivot_state]

        if obstacle_hit and direction == 'down':
            for row in range(22,-1,-1):
                for column in range(12):
                    if self.board[row][column][0] == 'active':
                        self.board[row][column][0] = 'obstacle'


    def rotate(self):
        if self.active_piece == 'line':
            self.rotate_line()
        elif self.active_piece == 'box':
            pass
        else:
            pivot_row, pivot_col, _ = self.find_pivot()
            self.rotate_grid(pivot_row, pivot_col)

    def rotate_line(self):
        pivot_row, pivot_col, pivot_state = self.find_pivot()
        horizontal_line = [(pivot_row, pivot_col + delta) for delta in range(-2,2)] # TODO: ?
        vertical_line = [(pivot_row + delta, pivot_col) for delta in range(-1,3)]

        if pivot_state == 'vertical':
            new_status = 'horizontal'
            next_line  = horizontal_line
            old_line   = vertical_line
        else:
            new_status = 'vertical'
            next_line  = vertical_line
            old_line   = horizontal_line

        obstacle_hit = False
        for cell in [self.board[row][col] for row, col in next_line]:
            if cell[0] == 'obstacle':
                obstacle_hit = True

        if not obstacle_hit:
            for row, col in old_line:
                self.board[row][col] = [None, None, None]
            for row, col in next_line:
                self.board[row][col] = ['active', 'line', None]

        self.board[pivot_row][pivot_col][2] = new_status

    def find_pivot(self):
        for row in range(23):
            for column in range(12):
                state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                if state == 'active' and pivot_state is not None:
                    return row, column, pivot_state

    def rotate_grid(self, pivot_row, pivot_col):
        top, bottom = pivot_row -1, pivot_row +1
        left, right = pivot_col -1, pivot_col +1
        new = [[0 for i in range(3)] for j in range(3)] #initializes 3x3 grid
        mapping = {
                    (0,0) : (bottom, left),
                    (0,1) : (pivot_row, left),
                    (0,2) : (top, left),
                    (1,0) : (bottom, pivot_col),
                    (1,1) : (pivot_row, pivot_col),
                    (1,2) : (top, pivot_col),
                    (2,0) : (bottom, right),
                    (2,1) : (pivot_row, right),
                    (2,2) : (top, right),
                  }

        for new_x, new_y in mapping:
            old_x, old_y = mapping[(new_x, new_y)]
            new[new_x][new_y] = self.board[old_x][old_y]

        # check if rotation avoids obstacles
        obstacle_hit = False
        for new_row in range(3):
            for new_column in range(3):
                if new[new_row][new_column][0] == 'active' and self.board[new_row+top][new_column+left][0] == 'obstacle':
                    obstacle_hit = True

        #Assign to self.board
        if not obstacle_hit:
            for new_row in range(3):
                for new_column in range(3): #place new onto self.board
                    if new[new_row][new_column][0] != 'obstacle':
                        self.board[top+new_row][left+new_column] = new[new_row][new_column]

    def piece_is_active(self):  #returns True if any active cells on the board
        return any('active' in cell for row in self.board for cell in row)

    def generate_piece(self):
        random_piece = random.choice(['line', 'T', 'J', 'L', 'box', 'S', 'Z'])
        coords = {
            'line' : [(0,6), (2,6), (3,6), (1,6)],
            'T'    : [(3,5), (3,7), (2,6), (3,6)],
            'J'    : [(3,5), (3,7), (2,5), (3,6)],
            'L'    : [(3,5), (3,7), (2,7), (3,6)],
            'box'  : [(3,6), (3,7), (2,6), (2,7)],
            'S'    : [(3,5), (2,6), (2,7), (3,6)],
            'Z'    : [(3,7), (2,5), (2,6), (3,6)],
        }

        for x, y in coords[random_piece]:
            self.board[x][y] = ['active', random_piece, None]

        pivot_x, pivot_y = coords[random_piece][3]
        status = 'vertical' if random_piece == 'line' else 'pivot'
        self.board[pivot_x][pivot_y] = ['active', random_piece, status]
        self.active_piece = random_piece

    def line_drop(self):
        newline = self.make_row()
        lines_dropped = 0
        for row in range(23): #must use range(23), not range(24), to avoid knocking out bottom row, which is just an obstacle.
            filled = all(status == 'obstacle' for status, _, _ in self.board[row])
            if filled:
                self.board.pop(row)
                self.board.insert(0,newline)
                lines_dropped += 1
        return lines_dropped

    def score(self, lines_dropped):
        points = {1 : 100, 2 : 300, 3 : 600, 4 : 1000}
        return points[lines_dropped]

    def you_lose(self):
        """ Returns true when any cell other than the two border cells
            in the top visible row (the fourth) is "obstacle"
        """
        return sum(status == 'obstacle' for status, _, _ in self.board[3]) > 2

def pygame_mode():
    board = Tetris()
    frames = 0
    points = 0

    while True:
        if not board.piece_is_active() and not board.you_lose():
            board.generate_piece()
        board.draw_board_pygame()
        lines_dropped = board.line_drop()
        if lines_dropped > 0:
            points = points + board.score(lines_dropped)
            print points
        frames += 1
        if frames % 100 == 0:
            board.move('down')
            #pdb.set_trace()
        for event in pygame.event.get():
            board.pygame_input(event)
            #print event.type, event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def terminal_mode(screen):
    begin_x = 20 ; begin_y = 7
    height = 50 ; width = 45
    win = curses.newwin(height, width, begin_y, begin_x)
    win.nodelay(1)

    board = Tetris()
    frames = 0
    points = 0

    while True:
        if not board.piece_is_active() and not board.you_lose():
            board.generate_piece()
        str_board = board.draw_board_terminal()
        lines_dropped = board.line_drop()
        if lines_dropped:
            points += board.score(lines_dropped)
        frames += 1
        if frames % 1000 == 0:
            board.move('down')
        char = win.getch()
        if char == -1:
            pass
        else:
            board.terminal_input(chr(char))
        win.addstr(0, 0, str_board)
        win.refresh()


if __name__ == '__main__':
    # pygame_mode()
    curses.wrapper(terminal_mode)
