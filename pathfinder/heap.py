import heapq

class Heap:
    def __init__(self):
        self.heap = []
        self.set = {}
        self.nodes = []
        self.free_spaces = []
        self.next_free = 0

    def len(self):
        return len(self.nodes)

    def push(self, node):
        if node.gridsquare in self.set:
            index = self.set[node.gridsquare]
            old_node = self.nodes[index]
            if node.g_cost < old_node.g_cost:
                self.nodes[index] = node
                
        else:
            if len(self.free_spaces) == 0:
                index = self.next_free
                self.next_free += 1
                self.nodes.append(node)
            else:
                index = self.free_spaces.pop()
                self.nodes[index] = node

            heapq.heappush(self.heap, (node.cost, index))
            self.set[node.gridsquare] = index

    #removes and returns the item with the smallest key from the heap
    def pop(self):
        if self.len() <= 0:
            return None
        else:
            (cost, index) = heapq.heappop(self.heap)
            self.free_spaces.append(index)
            return self.nodes[index]
    


