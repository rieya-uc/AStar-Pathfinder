import pyglet
import math

#i may change entity to subclass Sprite instead of using composition
#so that i can use Batch drawing
class Creep:
    def __init__(self, position, speed=5.0, filename=None, image=None):
        '''
        Creates a movable npc.

        '''

        self.speed = speed
        (self.step_x,self.step_y) = (0.0,0.0)    # Distance to move in x and
                                                 # y directions at each step
        self.isMoving = False
        self.path = []      # List of waypoints needed to get from A to B
        self.pCount = 0     # self.path[self.pCount] is where we're moving to
        self.next_angle = None    # The direction we want the entity to face

        if filename != None:
            image = pyglet.image.load(filename)
            image.anchor_x = image.width/2
            image.anchor_y = image.height/2
        try:
            self.sprite = pyglet.sprite.Sprite(image, position[0],position[1])
        except AttributeError:
            print "AttributeError: Creep image has value None"
            raise

        
    def draw(self):
        ''' Displays the npc. '''
        self.sprite.draw()
    
    def width(self):
        ''' Returns the width of the npc. '''
        return self.sprite.width

    def height(self):
        ''' Returns the height of the npc. '''
        return self.sprite.height

    def pos(self):
        ''' Returns the position on screen of the npc. '''
        return self.sprite.position

    def set_pos(self, new_pos):
        ''' Moves the npc to the specified position. '''
        self.sprite.position = new_pos

    def rotation(self):
        ''' Returns the angle of the npc in degrees, with north being 0. '''
        return self.sprite.rotation

    def set_rot(self, angle):
        ''' Sets the npc at the specified angle. '''
        self.sprite.rotation = angle % 360
        
    def rotate(self, degree):
        ''' Rotates the npc by a certain number of degrees. '''
        self.set_rot(self.sprite.rotation + degree)
    
    def get_rect(self):
        pass

    def set_path(self, path):
        ''' 
        Sets the path list and resets pCount. As self.path[0] is the 
        starting position, pCount is set to 1 as the next position to move to.

        '''

        self.path = path
        self.pCount = 0

        if len(self.path) > 1:
            self.pCount = 1
            self.set_destination(self.path[self.pCount])
            #self.start_moving(0.02)
        else:
            print "no path!"

    def set_destination(self, dest):
        '''
        Given a destination, calculates angle between current and end position 
        and calculates step size (distance to move each tick, so speed is 
        maintained).

        '''

        (x,y) = self.pos()
        (tx,ty) = dest
        (dx,dy) = (float(tx-x),float(ty-y))
        
        angle = 0.0
        if dy != 0.0:
            angle = math.atan(dx/dy)
        elif x != tx:
            angle = math.pi/2
        if dy < 0.0:
            angle = math.pi + angle
        elif dx < 0.0:
            angle = (2*math.pi) - abs(angle)
        
        self.next_angle = math.degrees(angle)
        self.step_x = self.speed * math.sin(angle)
        self.step_y = self.speed * math.cos(angle)
    
    def start_moving(self, tick):
        ''' Start moving, taking a step each tick. '''
        if not self.isMoving and self.pCount < len(self.path):
            pyglet.clock.schedule_interval(self.move, tick)
            pyglet.clock.set_fps_limit(60)
            self.isMoving = True
    
    def stop_moving(self):
        ''' Stops the npc moving. '''
        if self.isMoving:
            pyglet.clock.unschedule(self.move)
            self.isMoving = False

    def move(self, tick):
        '''
        Calls take_step, then if the next step will 'overstep' the mark, 
        move directly to waypoint and increment pCount, or stop moving 
        if at final destination.

        '''

        pos = self.pos()
        dest = self.path[self.pCount]
        dist_x = abs(dest[0] - pos[0])
        dist_y = abs(dest[1] - pos[1])

        self.take_step()
        
        if dist_x <= abs(self.step_x):
            self.step_x = 0.0
        if dist_y <= abs(self.step_y):
            self.step_y = 0.0
        
        if self.step_x == 0.0 and self.step_y == 0.0:
            self.set_pos(self.path[self.pCount])
            if self.pCount < len(self.path)-1:
                self.pCount += 1
                self.set_destination(self.path[self.pCount])
            else:
                self.stop_moving()

    def take_step(self):
        ''' Either rotate a step, or move forward. '''
        rotStep = self.speed * 4.0
        curDir = self.rotation()
        destDir = self.next_angle

        # Calculate the distance going clockwise and counterclockwise
        if destDir > curDir:
            cw = destDir - curDir
            ccw = 360 - cw
        elif destDir < curDir:
            ccw = curDir - destDir
            cw = 360 - ccw
        else:
            cw = ccw = 0

        # Rotate going round the shortest direction
        if cw <= ccw:
            self.rotate(rotStep)
        else:
            self.rotate(-rotStep)
        
        # Check if moving another step will "overstep" the mark
        # If so, jump to destination direction
        if abs(destDir - curDir) < rotStep:
            self.set_rot(destDir)
        
        # If no rotation, move forward
        if cw == 0 and ccw == 0:
            (x,y) = self.pos()
            new_pos = (x + self.step_x, y + self.step_y)
            self.set_pos(new_pos)




