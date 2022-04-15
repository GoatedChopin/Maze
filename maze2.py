import numpy as np
import random as r
import time as t

class maze:
    
    def __init__(self, rows = 10, cols = 10):
        self.rows = rows
        self.cols = cols
        self.matrix = []
        for r in range(rows):
            self.matrix.append([self.node(r,c) for c in range(cols)])
        
    def step(self, stack):
        if stack == None:
            return -1
        if len(stack) == 0:
            return -1
        neighbors = self.cardinal_neighbors(stack[-1])
        if neighbors != -1:
            r.shuffle(neighbors)
            s = neighbors[0]
            # self.matrix[s[0]][s[1]] = 1.0
            self.matrix[s[0]][s[1]].visit(stack[-1])
            stack.append(s)
            return stack
        else:
            stack.pop()
            return self.step(stack)
                
    def build(self):
        self.reset()
        point = self.pick_initial_point()
        stack = [point]
        while stack != -1:
            stack = self.step(stack)
            print(self)
            t.sleep(0.5)
        print(self)
    
    def reset(self):
        for r in range(self.rows):
            self.matrix.append([self.node(r,c) for c in range(self.cols)])

        
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
        return match[side]
    
    def unvisited(self, coord):
        row = coord[0]
        col = coord[1]
        if self.matrix[row][col].shape == r"|__|":
            return True
        else:
            return False
    
    def neighbors(self, coord):
        row = coord[0]
        col = coord[1]
        neighbors = []
        for ro in range(row-1,row+2):
            for c in range(col-1,col+2):
                if ro >= 0 and ro < self.rows and c >= 0 and c < self.cols:
                    if self.unvisited((ro,c)):
                        neighbors.append((ro,c))
        # print(neighbors)
        if len(neighbors) > 0:
            return neighbors
        else:
            return -1
    
    def in_bounds(self, coord):
        ro = coord[0]
        c = coord[1]
        if ro >= 0 and ro < self.rows and c >= 0 and c < self.cols:
            return True
        else:
            return False

    def cardinal_neighbors(self, coord):
        row = coord[0]
        col = coord[1]
        neighbors = []
        dirs = [(-1,0),(0,1),(1,0),(0,-1)]
        for d in dirs:
            new_coord = (d[0] + row, d[1] + col)
            if self.in_bounds(new_coord):
                if self.unvisited(new_coord):
                    neighbors.append(new_coord)
        # print(neighbors)
        if len(neighbors) > 0:
            return neighbors
        else:
            return -1
      
    class node:
        def __init__(self, row, col):
            self.row = row
            self.col = col
            self.coord = (row, col)
            self.shape = r"|__|"
            
        def visit(self, origin):
            diff = (self.row - origin[0], self.col - origin[1])
            if diff == (1,0) or diff == (-1,0):
                self.shape = r"|   "
            else:
                self.shape = r"____"
        
        def __str__(self):
            return self.shape
        
        
    def __str__(self):
        s = ""
        for r in range(self.rows):
            for c in range(self.cols):
                s = s + self.matrix[r][c].shape
            s = s + "\n"
        return s
        
if __name__ == "__main__":
    m = maze()
    m.build()