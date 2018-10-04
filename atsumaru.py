import random

from PIL import Image

class Canvas():
    """Represents a canvas on which to place patches."""

    def __init__(self, size):
        self.size = size
        self.slots = [[0] * self.size[0]] * self.size[1]
        self.available = set([])


    def insert(self, contents, position):
        self.slots[position[0]][position[1]] = contents
        self.update_available(position)


    def update_available(self, position):
        neighbours = ((-1, 0),
                      (1, 0),
                      (0, -1),
                      (0, 1),)


        for neighbour in neighbours:
            location = tuple(x+y for x,y in zip(neighbour, position))
            if all([x>=0 for x in location]) \
                and all([x<max for x,max in zip(location, self.size)]):
                    self.available.add(location)

        
class Patch():
    """Respresents a small patch of image."""
    
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    im = Image.open("data/test.JPG")
    box_size = (400, 400)
    final_size = (50, 50)
    canvas_size = (1000, 600)
    n_boxes = [int(x/y) for x, y in zip(canvas_size, final_size)]

    canvas = Image.new('RGB', canvas_size)
    for i in range(n_boxes[0]):
        for j in range(n_boxes[1]):
            x = random.randint(0, im.size[0])
            y = random.randint(0, im.size[1])
            box = (x, y, x + box_size[0], y + box_size[1])
            region = im.crop(box)
            angle = random.randint(0, 3)*90
            region_resized = region.resize(final_size).rotate(angle)
            x_start = i*final_size[0]
            y_start = j*final_size[1]
            canvas.paste(region_resized, (x_start,
                                          y_start, 
                                          x_start + final_size[0], 
                                          y_start + final_size[1]))


    canvas.show()
