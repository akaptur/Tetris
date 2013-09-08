import curses
from tetris import Tetris



def draw_screen(screen, board):
    begin_x = 20 ; begin_y = 7
    height = 25 ; width = 15
    win = curses.newwin(height, width, begin_y, begin_x)

    str_board = board.draw_board_terminal()
    win.addstr(str_board)
    
    win.refresh()
    while True:
        pass
    

if __name__ == '__main__':
    board = Tetris()
    curses.wrapper(draw_screen, board)