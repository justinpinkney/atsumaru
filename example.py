import random
import curses
import time

import atsumaru


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    try:
        canvas_size = (50, 50)
        artist = atsumaru.Artist(canvas_size)
        for i in range(100):
            artist.step()
            to_print = artist.canvas.__repr__()
            stdscr.addstr(0, 0, to_print)
            stdscr.refresh()
            time.sleep(10/60)

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
