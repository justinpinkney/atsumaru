import random

from PIL import Image

im = Image.open("data/test.JPG")
box_size = (400, 400)
final_size = (100, 100)
canvas_size = (1800, 1000)
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
