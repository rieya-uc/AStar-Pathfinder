import pyglet.gl as ogl
import pyglet

import heap
class Node:
    def __init__(self, gridsquare, parent):
        self.gridsquare = gridsquare
        self.parent = parent
        self.cost = 0
        self.g_cost = 0
        self.h_cost = 0
        
    #Compare this node with another node. 
    #Returns true if both contain the same gridsquare
    def compare(self,square):
        return self.gridsquare.compare(square)
    
class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.path_cache = []             #TODO
    
    def _in_list(self,list,square):
        for node in list:
            if node.compare(square):
                return True
   
        return False
    
    #the sum of g_cost and h_cost
    def calculate_f(self,node):
        return node.g_cost + node.h_cost
    
    #the movement cost to move from the starting point to a given square on the path,
    #via a specified square  
    def calculate_g(self,start,end,parent_g = 0):
        G = parent_g
        #work out if to_node is diagonally placed
        if self.grid.is_diagonal(start,end):
            return (14 * start.terrain_cost) + G
        else:
            return (10 * start.terrain_cost) + G
        
    #using the Manhattan method         
    def calculate_h(self,start,end):
        horizontal_squares = abs(end.i - start.i)            
        vertical_squares = abs(end.j - start.j)

        return (vertical_squares + horizontal_squares) * 10
                
    #create node and sets the node's costs            
    def create_node(self,square,parent,end_sq):
        new_node = Node(square,parent)
        new_node.h_cost = self.calculate_h(square,end_sq)
        if parent != None:
            new_node.g_cost = self.calculate_g(square,parent.gridsquare,parent.g_cost)
        else:
            new_node.g_cost = 0
        new_node.cost = new_node.h_cost + new_node.g_cost
        
        return new_node
                            
    #this is the main part of AStar, contains the algorithm
    def calculate_path(self, start, end):
        open_list = heap.Heap() 
        closed_list = []
        cur_sq = self.grid.get_square(tuple=start)       #the square we're currently on
        end_sq = self.grid.get_square(tuple=end)         #where we want to be
        #1. add the starting square to open list - Note: I don't bother with this
        starting_node = self.create_node(cur_sq,None,end_sq)
        
        #2. get adjacent walkable squares and add those to the open list
        #using the starting square as the parent
        adjacent = self.grid.get_adjacent_squares(cur_sq)
        for sq in adjacent:
            if sq.is_walkable():
                new_node = self.create_node(sq, starting_node,end_sq)
                open_list.push(new_node)
                    
        #3. Drop the starting square from your open list and add it to a closed list
        closed_list.append(starting_node)
        
        path_available = True
        #throws an error if a path does not exist
        while cur_sq != end_sq and open_list.len() > 0:
            #4.find the square with the lowest F score, remove it from the
            #open list and add it to the closed list
            '''
            print "Closed List:"
            for n in closed_list:
                print n.gridsquare.i,n.gridsquare.j
            print "Open List:"
            for n in open_list.nodes:
                print n.gridsquare.i,n.gridsquare.j, n.cost
            '''

            lowest_node = open_list.pop()
            closed_list.append(lowest_node)

            #5. Check adjacent squares, ignore squares already on closed list or unwalkable
            #and add to open list if not already there  
            #6. If already in the open list, check to see if G cost is lower, and 
            #replace if it is (the heap takes care of all of this)
            adjacent = self.grid.get_adjacent_squares(lowest_node.gridsquare)
            path_available = False
            for sq in adjacent:
                if sq.is_walkable() and not self._in_list(closed_list,sq):
                    path_available=True
                    new_node = self.create_node(sq,lowest_node,end_sq)
                    open_list.push(new_node)
           
            #print open_list.len()
            if (open_list.len() <= 0 and cur_sq != end_sq) or not path_available:
                closed_list = []
                break

            cur_sq = lowest_node.gridsquare

        #reconstruct the path - start from the last node in closed_list and follow its parent
        path = []

        if path_available:
            node = closed_list.pop()    
            while node != None:
                path.append(self.grid.get_square_centre(square=node.gridsquare))
                node = node.parent
            
            path.reverse()  
            path.pop()
            path.append(end)

        return path
    
