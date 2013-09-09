# import pygame, sys
# from pygame.locals import *
import curses
import pdb
import random

class Tetris():

    def __init__(self):
        def make_row():
            return [['obstacle', '', '']] + [['', '', ''] for i in range(10)] + [['obstacle', '', '']]
        self.board = [make_row() for i in range(23)]
        self.board.append([['obstacle', '', ''] for i in range(12)])

        self.active_piece = None

    def draw_board_pygame(self):
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        RED = (255,0,0)
        GREEN = (0,255,0)
        BLUE = (0,0, 255)
        PURPLE = (150,0,150)
        TURQUOISE = (0,150,150)
        YELLOW = (255,255,0)
        GREY = (125,125,125)
        DISPLAYSURF = pygame.display.set_mode((200,400),0,32)
        for i in range(3,23): #there are 24 rows total, 3 at the top and 1 at the bottom are NOT displayed
            for j in range(1,11): #there are 12 columns total, 1 on each side is NOT displayed
                y, x = i*20 - 60, j*20 - 20 #this maps to the coordinates being displayed, excluding borders
                piece_type = self.board[i][j][1]
                if piece_type == '':
                    pygame.draw.rect(DISPLAYSURF,BLACK,(x,y,20,20))
                elif piece_type == 'line':
                    pygame.draw.rect(DISPLAYSURF,GREEN,(x,y,20,20))
                elif piece_type == 'T':
                    pygame.draw.rect(DISPLAYSURF,BLUE,(x,y,20,20))
                elif piece_type == 'J':
                    pygame.draw.rect(DISPLAYSURF,WHITE,(x,y,20,20))
                elif piece_type == 'L':
                    pygame.draw.rect(DISPLAYSURF,RED,(x,y,20,20))
                elif piece_type == 'S':
                    pygame.draw.rect(DISPLAYSURF,PURPLE,(x,y,20,20))
                elif piece_type == 'Z':
                    pygame.draw.rect(DISPLAYSURF,TURQUOISE,(x,y,20,20))
                elif piece_type == 'box':
                    pygame.draw.rect(DISPLAYSURF,YELLOW,(x,y,20,20))
        if self.you_lose():
            #print 'You lose!'
            pygame.font.init()
            myfont = pygame.font.SysFont('sawasdee', 30, bold=1)
            pygame.draw.rect(DISPLAYSURF, GREY, (30,45,140,50))
            label = myfont.render('You lose!', 1, WHITE)
            DISPLAYSURF.blit(label, (40,50))
        pygame.display.update()

    def draw_board_terminal(self):
        out = []
        for i in range(3,23): #there are 24 rows total, 3 at the top and 1 at the bottom are NOT displayed
            row = ['o']
            for j in range(1,11): #there are 12 columns total, 1 on each side is NOT displayed
                if self.board[i][j][1] != '':
                    row.append('xxx')
                else:
                    row.append('   ')
            row.append('o\n')
            out.append("".join(row))
            out.append("".join(row))
        out.append('o'*33)

        if self.you_lose():
            str_out = "you lose!"

        return "".join(out)


    def piece_fall(self):
        obstacle_hit = False
        for row in range(22,-1,-1):
            for column in range(12):
                #print 'row: %d column: %d' %(row,column)
                if self.board[row][column][0] == 'active':
                    if self.board[row+1][column][0] == 'obstacle':
                        obstacle_hit = True
                        #print 'obstacle found at %d %d' %(row, column)

        if not obstacle_hit: #keep falling as long as obstacle not hit
            for row in range(22,-1,-1):
                for column in range(12):
                    if self.board[row][column][0] == 'active':
                        #print "found piece in piece_fall", row, column
                        color, pivot_state = self.board[row][column][1], self.board[row][column][2]
                        self.board[row][column] = ['','','']
                        self.board[row+1][column] = ['active',color,pivot_state]

        elif obstacle_hit: #if obstacle encountered, active piece becomes obstacle
            for row in range(22,-1,-1):
                for column in range(12):
                    if self.board[row][column][0] == 'active':
                        self.board[row][column][0] = 'obstacle'

    def pygame_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_LEFT:
                self.move_left()
            elif event.key == pygame.K_DOWN:
                self.piece_fall()
            elif event.key == pygame.K_UP:
                self.rotate()

    def terminal_input(self, char):
        moves = {'B': self.piece_fall,
                 'C': self.move_right,
                 'D': self.move_left,
                 }
        if char in moves:
            func = moves[char]
            func()
        elif char == 'A':
            self.rotate() #TODO: refactor rotate to not take piece as input


    def move_left(self):
        obstacle_hit = False
        for row in range(22,-1,-1): #loop backwards from bottom to top - easier to check for obstacles
            for column in range(1,11):
                state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                if state == 'active':
                    if self.board[row][column-1][0] == 'obstacle': #checks state of cell to left
                        obstacle_hit = True
        if not obstacle_hit: #obstacle not encountered
            for row in range(22,-1,-1):
                for column in range(1,11):
                    state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                    if state == 'active':
                        self.board[row][column] = ['','','']
                        self.board[row][column-1] = [state,piece_type,pivot_state]
                        #assigns cell on left to values of original cell

    def move_right(self):
        obstacle_hit = False
        for row in range(22,-1,-1):
            for column in range(11,0,-1): #loop from right to left
                state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                if state == 'active':
                    if self.board[row][column+1][0] == 'obstacle': #check state of cell to right
                        obstacle_hit = True
        if not obstacle_hit: #obstacle not encountered
            for row in range(22,-1,-1):
                for column in range(11,0,-1):
                    state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                    if state == 'active':
                        self.board[row][column] = ['','',''] #reset cell you're moving away from
                        self.board[row][column+1] = [state,piece_type,pivot_state]

    def rotate(self):
        if self.active_piece == 'line':
            self.rotate_line()
        elif self.active_piece == 'box':
            pass #rotating box does nothing
        else: #other five piece types
            pivot_row, pivot_col, pivot_state = self.find_pivot() #don't need pivot_state here, but find_pivot returns it
            self.rotate_grid(pivot_row, pivot_col)

    def rotate_line(self):
        pivot_row, pivot_col, pivot_state = self.find_pivot()

        obstacle_hit = False
        if pivot_state == 'vertical':
            for cell in [self.board[pivot_row][pivot_col+1], self.board[pivot_row][pivot_col-1], self.board[pivot_row][pivot_col-2]]:
                if cell[0] == 'obstacle':
                    obstacle_hit = True
            if not obstacle_hit:
                self.board[pivot_row][pivot_col+1] = self.board[pivot_row-1][pivot_col]
                self.board[pivot_row-1][pivot_col] = ['','','']
                self.board[pivot_row][pivot_col-1] = self.board[pivot_row+1][pivot_col]
                self.board[pivot_row+1][pivot_col] = ['','','']
                self.board[pivot_row][pivot_col-2] = self.board[pivot_row+2][pivot_col]
                self.board[pivot_row+2][pivot_col] = ['','','']
                self.board[pivot_row][pivot_col][2] = 'horizontal' #switch pivot state
        else: #pivot state is horizontal
            for cell in [self.board[pivot_row-1][pivot_col], self.board[pivot_row+1][pivot_col], self.board[pivot_row-2][pivot_col]]:
                if cell[0] == 'obstacle':
                    obstacle_hit = True
            if not obstacle_hit:
                self.board[pivot_row+1][pivot_col] = self.board[pivot_row][pivot_col-1]
                self.board[pivot_row][pivot_col-1] = ['','','']
                self.board[pivot_row-1][pivot_col] = self.board[pivot_row][pivot_col+1]
                self.board[pivot_row][pivot_col+1] = ['','','']
                self.board[pivot_row+2][pivot_col] = self.board[pivot_row][pivot_col-2]
                self.board[pivot_row][pivot_col-2] = ['','','']
                self.board[pivot_row][pivot_col][2] = 'vertical' #switch pivot state

    def find_pivot(self):
        for row in range(23):
            for column in range(12):
                state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
                if state == 'active' and pivot_state in ['pivot', 'vertical', 'horizontal']:
                    return row, column, pivot_state

    def rotate_grid(self, pivot_row, pivot_col):
        top, bottom = pivot_row -1, pivot_row +1
        left, right = pivot_col -1, pivot_col +1
        new = [[0 for i in range(3)] for j in range(3)] #initializes 3x3 grid
        #MAPPING
        new[0][0] = self.board[bottom][left]
        new[0][1] = self.board[pivot_row][left]
        new[0][2] = self.board[top][left]
        new[1][0] = self.board[bottom][pivot_col]
        new[1][1] = self.board[pivot_row][pivot_col]
        new[1][2] = self.board[top][pivot_col]
        new[2][0] = self.board[bottom][right]
        new[2][1] = self.board[pivot_row][right]
        new[2][2] = self.board[top][right]
        #Assign to self.board
        obstacle_hit = False
        for new_row in range(3):
            for new_column in range(3):
                if new[new_row][new_column][0] == 'active' and self.board[new_row+top][new_column+left][0] == 'obstacle':
                    obstacle_hit = True
        if not obstacle_hit:
            for new_row in range(3):
                for new_column in range(3): #place new onto self.board
                    if new[new_row][new_column][0] != 'obstacle':
                        self.board[top+new_row][left+new_column] = new[new_row][new_column]



    def piece_is_active(self):  #returns True if any active cells on the board
        for row in range(23):
            for column in range(12):
                if self.board[row][column][0] == 'active':
                    return True
        else:
            return False

    def generate_piece(self):
        random_piece = random.choice(['line', 'T', 'J', 'L', 'box', 'S', 'Z'])
        coords = {
            'line' : [(0,6), (2,6), (3,6), (1,6)],
            'T'    : [(3,5), (3,7), (2,6), (3,6)],
            'J'    : [(3,5), (3,7), (2,5), (3,6)],
            'L'    : [(3,5), (3,7), (2,7), (3,6)],
            'box'  : [(3,6), (3,7), (2,6), (2,7)],
            'S'    : [(3,5), (2,6), (2,7), (3,6)],
            'Z'    : [(3,6), (2,5), (2,6), (3,7)],
        }

        for x, y in coords[random_piece]:
            self.board[x][y] = ['active', random_piece, '']

        pivot_x, pivot_y = coords[random_piece][3]
        self.board[pivot_x][pivot_y] = ['active', random_piece, 'pivot']
        self.active_piece = random_piece

    def line_drop(self):
        newline = [['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']]
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
            board.piece_fall()
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
        if lines_dropped > 0:
            points = points + board.score(lines_dropped)
        frames += 1
        if frames % 1000 == 0:
            board.piece_fall()
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
