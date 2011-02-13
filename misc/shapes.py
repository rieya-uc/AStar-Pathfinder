'''
    Anthony Todd - November 2010
'''

import pyglet
import pyglet.gl as ogl
import math

        
class drawable(object):
    def __init__(self, cp = (0.0,0.0), vis = True):
        self._cp = cp
        self._visible = vis
        
    def render(self):
        ogl.glPushMatrix()
        ogl.glTranslatef(self._cp[0], self._cp[1],0.0)
        self.draw()
        ogl.glPopMatrix()
        
    def draw(self):
        raise NotImplementedError

class square(drawable):
        
    def __init__(self, cp=(0,0), width=0.0, height=0.0, colour=(255,255,255), vertices=[]):
        drawable.__init__(self,cp,True)
        if vertices == []:
            self._width = width
            self._height = height
            hWidth = width*0.5
            hHeight = height*0.5
            self.vertices = ('v2f',(-hWidth,-hHeight,hWidth,-hHeight,hWidth,+hHeight,-hWidth,hHeight))
        else:
            self.vertices = vertices
            
        self.colours = ('c3B',(colour[0],colour[1],colour[2],colour[0],colour[1],colour[2],colour[0],colour[1],colour[2],colour[0],colour[1],colour[2]))
        self.vertex_list = pyglet.graphics.vertex_list(4, self.vertices, self.colours)
        
    def draw(self):
        self.vertex_list.draw(ogl.GL_QUADS)

class circle(drawable):
    def __init__(self, cp, radius, edges, colour):
        drawable.__init__(self,cp,True)
        self.radius = radius
        self.step = math.radians(360)/edges
        verts = []
        cols = []
        edge = 0
        verts.append(0)
        verts.append(0)
        cols.append(colour[0])
        cols.append(colour[1])
        cols.append(colour[2])
        while(edge <= edges):
            s = (self.step*edge)
            x , y = math.sin(s)*self.radius, math.cos(s)*self.radius
            #print s, x, y
            verts.append(x)
            verts.append(y)
            edge = edge+1
            cols.append(colour[0])
            cols.append(colour[1])
            cols.append(colour[2])
       # print verts
        self.vertices = ('v2f',verts)
        self.colours = ('c3B',cols)
        self.vertex_list = pyglet.graphics.vertex_list(edges+2, self.vertices, self.colours)
        
    def draw(self):
        self.vertex_list.draw(ogl.GL_TRIANGLE_FAN)#
        
    def move(self, new_x, new_y):
        self._cp = (new_x,new_y)
