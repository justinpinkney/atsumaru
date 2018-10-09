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
        canvas = atsumaru.Canvas(canvas_size)
        patch = atsumaru.Patch([])
        canvas.insert(patch, (25, 25))
        for step in range(canvas_size[0]*canvas_size[1]):
            available = canvas.available
            chosen_position = random.sample(available, 1)
            canvas.insert(patch, chosen_position[0])
            to_print = canvas.__repr__()
            stdscr.addstr(0, 0, to_print)
            stdscr.refresh()
            time.sleep(1/60)

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
