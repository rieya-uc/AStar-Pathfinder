import pyglet.gl as ogl
import pyglet

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GridSquare:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.terrain_cost = 1       #e.g. swamp terrain will have a higher cost
        self.walkable = True
        
    def block(self):
        self.walkable = False
    
    def unblock(self):
        self.walkable = True
        
    def is_walkable(self):
        return self.walkable
    
    def compare(self,square):
        return self.i == square.i and self.j == square.j
    
    def print_me(self):
        print self.i,self.j

#divides the window up into squares, each square is gridSp in length      
class GridMap:
    def __init__(self, window_width, window_height, gridSp = 10, visible = False):
        self.gridSp = gridSp
        self.width = window_width
        self.height = window_height
        self.squares_across = window_width / self.gridSp
        self.squares_up = window_height / self.gridSp
        self.visible = visible
        
        self.grid = [[0 for _ in xrange(window_width)] for _ in xrange(window_height)]
        
        #use an array to keep track of each square of the grid, and whether that
        #square contains an object
        for i in range(self.squares_across):
            for j in range(self.squares_up):
                self.grid[i][j] = GridSquare(i,j)
        
    def draw(self):
        if self.visible:
            for x in range(0, self.width, self.gridSp):
                for y in range(0, self.height, self.gridSp):
                    pyglet.graphics.draw(2,ogl.GL_LINES,
                                         ('v2i',(0,y,self.width,y)),
                                         ('c3B',(205,201,201, 205,201,201)))
                pyglet.graphics.draw(2, ogl.GL_LINES,
                                     ('v2i', (x,0,x,self.height)),
                                     ('c3B', (205,201,201, 205,201,201)))
            
            p = self.gridSp
            for i in range(self.squares_across):
                for j in range(self.squares_up):
                    if not self.grid[i][j].is_walkable(): #is blocked
                        pyglet.graphics.draw(2, ogl.GL_LINES,
                                             ('v2i',(i*p,(j+1)*p,(i+1)*p,j*p)))
                

    #takes coordinates and returns the grid square of those coords
    def get_square(self, x=None, y=None, tuple=None):
        if tuple != None:
            x = tuple[0]
            y = tuple[1]
        sqx = int(x / self.gridSp)
        sqy = int(y / self.gridSp)
        return self.grid[sqx][sqy]

    
    #blocks square that contains the coords(x,y)
    def block_square(self, x, y):
        square = self.get_square(x,y)
        square.block()
        
    #when the user draws a square, that whole area is blocked off
    def block_area(self,sx,sy,ex,ey):
        if sx > ex:
            sx,ex = ex,sx
        if sy > ey:
            sy,ey = ey,sy     
        
        #need to round up to the nearest self.gridSp, so that all blocked squares are caught
        if ex % self.gridSp > 0:
            ex = ((ex / self.gridSp) * self.gridSp) + self.gridSp
        if ey % self.gridSp > 0:
            ey = ((ey / self.gridSp) * self.gridSp) + self.gridSp
            
        for i in range(sx,ex,self.gridSp):
            for j in range(sy,ey,self.gridSp):
                self.block_square(i, j)
                
    #returns a list of squares that are adjacent to a particular square
    def get_adjacent_squares(self, square):
        i = square.i
        j = square.j
        squares = []
        
        #left and middle
        if i > 0:
            if j < self.squares_up - 1:
                squares.append(self.grid[i-1][j+1])
            squares.append(self.grid[i-1][j])
            if j > 0:
                squares.append(self.grid[i-1][j-1])
                
        #middle
        if j < self.squares_up - 1:
            squares.append(self.grid[i][j+1])
        #squares.append(self.grid[i][j])
        if j > 0:
            squares.append(self.grid[i][j-1])
                
        #right
        if i < self.squares_across - 1:
            if j < self.squares_up - 1:
                squares.append(self.grid[i+1][j+1])
            squares.append(self.grid[i+1][j])
            if j > 0:
                squares.append(self.grid[i+1][j-1])
 
        return squares

    #get that square's centre coords
    #i.e converts square coords to screen coords
    def get_square_centre(self, sqx=0, sqy=0, square=None):
        if square!=None:
            sqx = square.i
            sqy = square.j
        x = (sqx * self.gridSp) + (self.gridSp/2)
        y = (sqy * self.gridSp) + (self.gridSp/2)
        return x,y
    
    #are the two squares immediately diagonal from each other
    def is_diagonal(self, sq1, sq2):
        return abs(sq1.i - sq2.i) == 1 and abs(sq1.j - sq2.j) == 1
    
