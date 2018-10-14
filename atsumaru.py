import random

from PIL import Image

class Canvas():
    """Represents a canvas on which to place patches."""

    def __init__(self, size):
        self.size = size
        self.slots = []
        for i in range(self.size[0]):
            row = []
            for j in range(self.size[1]):
                row.append(None)
            self.slots.append(row)
        self.available = set([])
        self.filled = set([])


    def insert(self, contents, position):
        """Add something to the canvas."""
        self.slots[position[0]][position[1]] = contents
        self.filled.add(position)
        self.update_available(position)


    def update_available(self, position):
        """Update the set of available positions."""
        neighbourhood = ((-1, 0), (1, 0), (0, -1), (0, 1))

        for neighbour in neighbourhood:
            location = tuple(dx+x for dx,x in zip(neighbour, position))
            if self.within_canvas(location):
                self.available.add(location)
                content = self.slots[location[0]][location[1]]
                if not content:
                    self.slots[location[0]][location[1]] = 0

        self.available = self.available - self.filled


    def get_neighbours(self, position):
        """Return all neighbour contents of position."""
        neighbourhood = ((-1, 0), (1, 0), (0, -1), (0, 1))
        content_neighbours = []

        for neighbour in neighbourhood:
            location = tuple(dx+x for dx,x in zip(neighbour, position))
            if self.within_canvas(location):
                content = self.slots[location[0]][location[1]]
                if content:
                    content_neighbours.append(content)
        
        return content_neighbours


    def within_canvas(self, location):
        """Checks if position is within the canvas."""
        if all([x>=0 for x in location]) \
            and all([x<max for x,max in zip(location, self.size)]):
            return True
        else:
            return False
        

    def __repr__(self):
        line = ''
        for x in self.slots:
            for y in x:
                if y is None:
                    line += '-'
                elif y is 0:
                    line += '0'
                else:
                    line += 'x'
            line += '\n'
        return line
        
class Patch():
    """Respresents a small patch of image."""
    
    def __init__(self, data):
        self.data = data


class Matcher():
    """Measures fit of patch with neighbours."""

    def __init__(self):
        pass

    def match(self, patch, neighbours):
        return random.randint(1, 100)


class Artist():
    """Fills a canvas with image Patches."""

    def __init__(self, canvas_size):
        self.canvas = Canvas((canvas_size))
        self.patches = []
        self.matcher = Matcher()

        for i in range(20):
            self.patches.append(Patch([]))

        patch = self.patches.pop(0)
        self.canvas.insert(patch, (5, 5))
    
    def add_image(self, image):
        # TODO make patches
        # Add to list
        pass

    def step(self):
        patch = self.patches.pop(0)
        measure_list = []
        for position in self.canvas.available:
            neighbours = self.canvas.get_neighbours(position)
            distance = self.matcher.match(patch, neighbours)
            measure_list.append((position, distance))
        # Select best match
        measure_list.sort(key=lambda x: x[1])
        best_position = measure_list[0][0]
        self.canvas.insert(patch, best_position)

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
