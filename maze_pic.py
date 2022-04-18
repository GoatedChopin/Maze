import numpy as np
import random as r
import time as t
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

class maze:
    
    def __init__(self, rows = 10, cols = 10, node_width = 10, node_height = 10, path_width = 0.8, path_height = 0.8):
        self.rows = rows
        self.cols = cols
        self.n_w = node_width
        self.n_h = node_height
        self.path_width = round(path_width * self.n_w)
        self.path_height = round(path_height * self.n_h)
        self.dims = [rows * node_height, cols * node_width, 4]
        self.matrix = np.zeros(self.dims)
        self.matrix[:,:] = [0, 0, 0, 255]
        self.im = Image.fromarray(self.matrix.astype(np.uint8))
        self.draw = ImageDraw.Draw(self.im)
        self.node_centers = [[(round(r * self.n_h + self.n_h / 2), round(c * self.n_w + self.n_w / 2)) for c in range(self.cols)] for r in range(self.rows)]
        
    def update_im(self):
        self.im = Image.fromarray(self.matrix.astype(np.uint8))

    def step(self, stack):
        if stack == None:
            return -1
        if len(stack) == 0:
            return -1
        neighbors = self.cardinal_neighbors(stack[-1])
        if neighbors != -1:
            s = r.choice(neighbors)
            self.visit(s, stack[-1])
            stack.append(s)
            return stack
        else:
            print("Backtracking...")
            stack.pop()
            return self.step(stack)
                
    def build(self, steptime = 0, show = True):
        point = self.pick_initial_point()
        stack = [point]
        while stack != -1:
            stack = self.step(stack)
            if show:
                imgplot = plt.imshow(self.im)
                plt.axis('off')
                plt.show()
            t.sleep(steptime)
        imgplot = plt.imshow(self.im)
        plt.axis('off')
        plt.show()
        
    def pick_initial_point(self):
        dirs = ["top", "right", "bottom", "left"]
        r.shuffle(dirs)
        side = dirs[0]
        colsample = r.sample(range(self.cols), 1)[0]
        rowsample = r.sample(range(self.rows), 1)[0]
        match = {"top":(0, colsample), 
                 "right":(self.cols - 1, rowsample), 
                 "bottom": (self.rows - 1, colsample), 
                 "left": (rowsample, 0)}
        return self.node_centers[match[side][0]][match[side][1]]
    
    def unvisited(self, pixel):
        return self.im.getpixel(pixel) == (0, 0, 0, 255)
     
    def in_bounds(self, pixel):
        ro = pixel[0]
        c = pixel[1]
        if ro >= 0 and ro < self.dims[0] and c >= 0 and c < self.dims[1]:
            return True
        else:
            return False

    def cardinal_neighbors(self, pixel):
        row = pixel[0]
        col = pixel[1]
        neighbors = []
        dirs = [(-self.n_h, 0), (0, self.n_w), (self.n_h, 0),(0, -self.n_w)]
        for d in dirs:
            new_pixel = (d[0] + row, d[1] + col)
            if self.in_bounds(new_pixel):
                if self.unvisited(new_pixel):
                    neighbors.append(new_pixel)
        # print(neighbors)
        if len(neighbors) > 0:
            return neighbors
        else:
            return -1
      
    def visit(self, new_pixel, origin_pixel):
        row_d = new_pixel[0] - origin_pixel[0]
        if row_d == 0:
            width = self.path_height
        else:
            width = self.path_width
        self.draw.line([new_pixel, origin_pixel], width = width)

        
if __name__ == "__main__":
    m = maze(rows = 100,
             cols = 100,
             node_width = 10,
             node_height = 10,
             path_width = 0.6,
             path_height = 0.6)
    m.build(steptime = 0,
            show = False)