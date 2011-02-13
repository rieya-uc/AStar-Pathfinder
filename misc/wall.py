import shapes
import pyglet.gl as ogl

class Wall:
    def __init__(self, lx, ly, rx, ry, colour):
        self.square = shapes.square(
                vertices=('v2i', (lx, ly, rx, ly, rx, ry, lx, ry)),
                colour=colour)
        
    def draw(self):
        self.square.render()

