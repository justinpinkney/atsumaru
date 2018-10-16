import random
import curses
import time

import atsumaru


if __name__ == "__main__":

    canvas_size = (100, 100)
    artist = atsumaru.Artist(canvas_size)
    steps = canvas_size[0]*canvas_size[1]-1
    for i in range(steps):
        print(i)
        artist.step()

    artist.show()
