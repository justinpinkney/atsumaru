import random
import math

from PIL import Image
from PIL import ImageStat
from tqdm import tqdm

import numpy as np

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


    def get(self, position):
        """Retrieve an item from a position."""
        return self.slots[position[0]][position[1]]


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
        """Return all neighbour contents of position.
        
        returned neighbours is a dictionary with each element of neighbourhood
        as a key. The value is the neighbour or None if no neighbour.
        """
        neighbourhood = ((-1, 0), (1, 0), (0, -1), (0, 1))
        content_neighbours = dict()

        for neighbour in neighbourhood:
            content_neighbours[neighbour] = None
            location = tuple(dx+x for dx,x in zip(neighbour, position))
            if self.within_canvas(location):
                content = self.slots[location[0]][location[1]]
                if content:
                    content_neighbours[neighbour] = content
        
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
                    line += '_'
                else:
                    if y.data < 10:
                        line += str(y.data)
                    else:
                        line += '#'
            line += '\n'
        return line
        

class Patch():
    """Respresents a small patch of image."""
    orientations = ('UP', 'RIGHT', 'DOWN', 'LEFT')
    
    def __init__(self, data):
        self._data = data
        self.orientation = random.choice(Patch.orientations)

    @property
    def data(self):
        if self.orientation == 'UP':
            rotation = 0
        elif self.orientation == 'RIGHT':
            rotation = 1
        elif self.orientation == 'DOWN':
            rotation = 2
        elif self.orientation == 'LEFT':
            rotation = 3
        else:
            raise ValueError('Invalid orientation')
        return np.rot90(self._data, -rotation)


class MeanMatcher():
    """Measures fit of patch with neighbours."""

    def __init__(self):
        pass

    def match(self, patch, neighbours):
        distances = []
        for neighbour in neighbours.values():
            if neighbour:
                distance = abs(np.mean(patch.data, axis=(0, 1)) - 
                                np.mean(neighbour.data, axis=(0,1)))
                distance = np.sum(distance)
                distances.append(distance)
        return min(distances)


class PositionMatcher():
    """Checks fit based on position of neighbours."""

    def __init__(self):
        self.neighbourhood = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def match(self, patch, neighbours):
        distance = 0
        for index, position in enumerate(self.neighbourhood):
            neighbour = neighbours[position]
            if neighbour:
                if index == 0: # left
                    patch_row = patch.data[:10,:]
                    neighbour_row = neighbour.data[-10,:]
                if index == 1: # right
                    patch_row = patch.data[-10:,:]
                    neighbour_row = neighbour.data[:10,:]
                if index == 2: # up
                    patch_row = patch.data[:,:10]
                    neighbour_row = neighbour.data[:,-10:]
                if index == 3: # down
                    patch_row = patch.data[:,-10:]
                    neighbour_row = neighbour.data[:,:10]
                difference = np.mean(patch_row, axis=(0, 1)) - \
                                np.mean(neighbour_row, axis=(0, 1))
                distance += np.sum(abs(difference))
        return distance


class Artist():
    """Fills a canvas with image Patches."""

    def __init__(self, canvas_size=None):
        self.patches = []
        self.matcher = PositionMatcher()
        self.tile_size = 50

        self.from_image("data/test.JPG")
        if canvas_size:
            self.canvas = Canvas((canvas_size))
        else:
            canvas_size = math.floor(math.sqrt(len(self.patches)))
            self.canvas = Canvas((canvas_size, canvas_size))
        patch = self.patches.pop(0)
        self.canvas.insert(patch, (5, 5))
        patch = self.patches.pop(0)
        self.canvas.insert(patch, (7, 10))
    
    def add_random(self, random_size):
        """Adds patches with random data."""
        for x in range(random_size):
            self.patches.append(Patch(random.randint(0, 255)))

    def from_image(self, image):
        im = Image.open(image)
        [width, height] = im.size
        tile_size = self.tile_size
        n_tiles = [math.floor(x/tile_size) for x in im.size]
        for i in range(n_tiles[0] - 1):
            for j in range(n_tiles[1] - 1):
                box = (i*tile_size, j*tile_size, (i+1)*tile_size, (j+1)*tile_size)
                patch = Patch(im.crop(box))
                self.patches.append(patch)
        random.shuffle(self.patches)

    def fill(self):
        """Fill the canvas with patches."""

        num_iterations = len(self.patches)
        for i in tqdm(range(num_iterations)):
            self.step()


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

    def show(self):
        tile_size = self.tile_size
        output = Image.new('RGB', [tile_size*x for x in self.canvas.size])
        for x in range(self.canvas.size[0]):
            for y in range(self.canvas.size[1]):
                im = self.canvas.slots[x][y].data
                box = (x*tile_size, y*tile_size, (x+1)*tile_size, (y+1)*tile_size)
                output.paste(Image.fromarray(im), box)
        output = output.resize((math.floor(x/4) for x in output.size))
        output.save("output.jpg")
        output.show()

