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
            n = self.matrix[stack[-1][0]][stack[-1][1]]
            self.matrix[s[0]][s[1]].visit(n)
            stack.append(s)
            return stack
        else:
            print("Backtracking...")
            stack.pop()
            return self.step(stack)
                
    def build(self, steptime = 0):
        self.reset()
        point = self.pick_initial_point()
        stack = [point]
        while stack != -1:
            stack = self.step(stack)
            print(self)
            t.sleep(steptime)
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
        n = self.matrix[row][col]
        if n.up and n.right and n.down and n.left:
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
            self.shape = ""
            self.up = True
            self.right = True
            self.down = True
            self.left = True
            
        def visit(self, origin_node):
            diff = (self.row - origin_node.row, self.col - origin_node.col)
            # {origin:[new_origin_string, new_visited_string]}
            if diff == (-1,0):
                origin_node.up = False
                self.down = False
            elif diff == (0,1):
                origin_node.right = False
                self.left = False
            elif diff == (1,0):
                origin_node.down = False
                self.up = False
            else:
                origin_node.left = False
                self.right = False
        
        def set_shape(self):
            s = ""
            if self.up:
                s = s + " __ \n"
            else:
                s = s + "\n"
            if self.left:
                s = s + r"|"
            else:
                s = s + " "
            if self.down:
                s = s + "__"
            else:
                s = s + "  "
            if self.right:
                s = s + r"|"
            else:
                s = s + " "
            self.shape = s
        
        def __str__(self):
            self.set_shape()
            return self.shape
        
        
    def __str__(self):
        s = ""
        dirs = ["top", "left-right"]
        for r in range(self.rows):
            for d in dirs:
                if d == "top":
                    for c in range(self.cols):
                        if self.matrix[r][c].up:
                            s = s + "____"
                        else:
                            s = s + "    "
                elif d == "left-right":
                    for c in range(self.cols):
                        if self.matrix[r][c].left:
                            s = s + "|"
                        else:
                            s = s + "_"
                        if self.matrix[r][c].down:
                            s = s + "__"
                        else:
                            s = s + "  "
                        if self.matrix[r][c].right:
                            s = s + "|"
                        else:
                            s = s + "_"
                s = s + "\n"
        return s
        
if __name__ == "__main__":
    m = maze()
    m.build(steptime = 0.1)