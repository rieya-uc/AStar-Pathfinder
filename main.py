import random, pyglet
import pyglet.gl as ogl
from misc import creep, wall
from pathfinder import grid, pathfinder

SWIDTH = 600
SHEIGHT = 300
class Window(pyglet.window.Window):
    def __init__(self):
        '''
        
        For testing my pathfinding code.
        Left click and drag to draw walls.
        Right click to set a destination point and start the sprite moving.

        '''
        pyglet.window.Window.__init__(self,SWIDTH,SHEIGHT,vsync=True)
        self.creep = creep.Creep((405,165),5.0,filename="misc/creep.png")
        self.tick = 0.02
        self.walls = []
        self.end_dot = None
        self.end = None
        self.grid = grid.GridMap(SWIDTH,SHEIGHT,50,False)
        self.pf = pathfinder.AStar(self.grid)

        #drag info
        self.startx = None
        self.starty = None
        self.endx = None
        self.endy = None
        self.drag_started = False

    def on_draw(self):
        self.clear()
        self.creep.draw()
        self.grid.draw()
        
        if self.end_dot != None:
            self.end_dot.draw()

        for w in self.walls:
            w.draw()
        
        if self.drag_started:
            pyglet.graphics.draw(2,ogl.GL_LINES,
                    ('v2i',(self.startx,self.starty,self.endx,self.endy)),
                    ('c3B',(0, 255, 0, 0, 255, 0)))
        
    def add_wall(self, lx, ly, rx, ry, colour=(255,0,0)):
        ''' 
        Draws a square between two points and blocks the area off 
        in the grid so the npc cannot walk over it.
        
        '''

        if lx > rx:
            lx,rx = rx,lx
        if ly > ry:
            ly,ry = ry,ly


        if lx < 0:
            lx = 0
        if ly < 0:
            ly = 0
        if rx > SWIDTH:
            rx = SWIDTH
        if ry > SHEIGHT:
            ry = SHEIGHT

        
        '''
        h = self.creep.height()
        w = self.creep.width()
        blx = lx - (w/2)
        bly = ly - (h/2)
        brx = rx + (w/2)
        bry = ry + (h/2)

        print "blocking area (", blx, ",", bly,") (",brx,",",bry,")"
        '''
        
        self.walls.append(wall.Wall(lx,ly,rx,ry,colour))       
        self.grid.block_area(lx, ly, rx, ry)

    def on_mouse_press(self, x, y, button, modifiers):
        '''
        Left button to draw a wall.
        Right button to start moving.

        '''
        if button == pyglet.window.mouse.RIGHT:
            self.creep.stop_moving()
            self.end = (x,y)
            path = self.pf.calculate_path(self.creep.pos(), self.end)
            self.creep.set_path(path)
            self.creep.start_moving(self.tick)
        elif button == pyglet.window.mouse.LEFT:
            self.creep.stop_moving()
            self.startx = x
            self.starty = y            

        
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        '''
        Creates a wall.
        
        '''
        if button == pyglet.window.mouse.LEFT:
            self.drag_started = True
            #self.creep.stop_moving()
            self.endx = x
            self.endy = y 

    def on_mouse_release(self, x, y, button, modifiers):
        if self.drag_started:
            #sx = self.startx
            #sy = self.starty
            #print "adding wall", self.startx,self.starty,self.endx,self.endy
            self.add_wall(self.startx, self.starty,self.endx,self.endy)
            #self.walls.append(shapes.square(vertices=('v2i',(sx,sy,x,sy,x,y,sx,y)),colour=self.colour))
            #self.grid.block_area(self.startx,self.starty,self.endx,self.endy)
            
            self.drag_started = False
            self.startx = self.endx = None
            self.starty = self.endy = None
            
            if self.creep.pos() != self.end and self.end != None:
                path = self.pf.calculate_path(self.creep.pos(),self.end)
                self.creep.set_path(path)
                self.creep.start_moving(self.tick)

if __name__ == "__main__":
    Window()
    pyglet.app.run()
