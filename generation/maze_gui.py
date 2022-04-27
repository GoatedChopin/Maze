import random as r
import time as t
import pyautogui as gui

class maze:
    
    def __init__(self, rows = 10, cols = 10, h_pix = 20, v_pix = 20, random_start = False):
        self.rows = rows
        self.cols = cols
        self.h_pix = 10
        self.v_pix = 10
        self.random_start = random_start
        self.matrix = []
        for r in range(rows):
            self.matrix.append([self.node(r,c,h_pix,v_pix) for c in range(cols)])
        
    def step(self, stack):
        if stack == None:
            return -1
        if len(stack) == 0:
            return -1
        neighbors = self.cardinal_neighbors(stack[-1])
        if neighbors != -1:
            r.shuffle(neighbors)
            s = neighbors[0]
            n = self.matrix[stack[-1][0]][stack[-1][1]]
            self.move_to(n, self.matrix[s[0]][s[1]])
            self.matrix[s[0]][s[1]].visit(n)
            stack.append(s)
            return stack
        else:
            print("Backtracking...")
            self.move_to(stack[-1], stack[-2])
            stack.pop()
            return self.step(stack)
                
    def draw(self, steptime = 0):
        self.reset()
        
        # Change Tabs to MS Paint
        # gui.press("win", pause = 1)
        # gui.press(["p","a","i","n","t"])
        # gui.press("enter")
        
        t.sleep(5)
        
        # Move to initial point
        # Pick initial Maze Point, move to that
        if self.random_start:
            point = self.pick_initial_point()
            gui.moveRel(point[0] * self.h_pix, point[1] * self.v_pix)
        else:
            point = (0,0)
        stack = [point]
        while stack != -1:
            stack = self.step(stack)
            print(self)
            t.sleep(steptime)
        print(self)
        
        # Invert colors of the Drawing    
    
    def reset(self):
        for r in range(self.rows):
            self.matrix.append([self.node(r,c, self.h_pix, self.v_pix) for c in range(self.cols)])

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
    
    def move_to(self, old_node, new_node):
        if type(old_node) == tuple:
            old_node = self.matrix[old_node[0]][old_node[1]]
        if type(new_node) == tuple:
            new_node = self.matrix[new_node[0]][new_node[1]]
        gui.mouseDown()
        x_diff = new_node.pixel[0] - old_node.pixel[0]
        y_diff = new_node.pixel[1] - old_node.pixel[1]
        gui.moveRel(x_diff, y_diff)
        gui.mouseUp()
    
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
        def __init__(self, row, col, h_pix, v_pix):
            self.row = row
            self.col = col
            self.coord = (row, col)
            self.pixel = (row * h_pix, col * v_pix)
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
    m = maze(rows = 40, cols = 40, h_pix = 10, v_pix = 10)
    m.draw(steptime = 0)