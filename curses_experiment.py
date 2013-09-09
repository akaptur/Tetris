import curses
import string
import random

def letters():
    for char in string.letters:
        yield char

def draw_screen(screen):
    begin_x = 20 ; begin_y = 7
    height = 25 ; width = 15
    win = curses.newwin(height, width, begin_y, begin_x)
    # lets = letters()

    tick = 0
    while True:
    
        inp = win.getch()
        mapper = {curses.KEY_UP:    'up   ',
                  curses.KEY_DOWN:  'down ',
                  curses.KEY_LEFT:  'left ',
                  curses.KEY_RIGHT: 'right',

        }
        if inp in mapper:
            char = mapper[inp]
        else:
            char = chr(inp)

        win.addstr(0,0, char+"  ")
        win.refresh()


if __name__ == '__main__':
    curses.wrapper(draw_screen)