
class Node:
    def __init__(self, name = "node", other_infos = {}):
        self.name = name
        self.next_nodes = []
        self.prev_node = None
        self.score = 0.0
        self.other_infos = other_infos

    def append(self, node_to_append):
        self.next_nodes.append(node_to_append)
        node_to_append.prev_node = self

    def remove(self):
        if(self.prev_node is None):
            return 

        self.prev_node.next_nodes.remove(self)
        self.prev_node = None

    def get_max_score_next_node(self):
        if(len(self.next_nodes) <= 0):
            return None

        max_score = self.next_nodes[0].score
        max_node = self.next_nodes[0]

        for node in self.next_nodes:
            if(max_score < node.score):
                max_score = node.score
                max_node = node

        return max_node



    



class GameTree:
    def __init__(self):
        self.root = None

    def print(self, depth = 0, node = None):
        if(node is None):
            node = self.root
        
        for i in range(depth):
            print(" ", end="")
        
        print("- " + node.name)

        depth += 1
        for i in range(len(node.next_nodes)):
            self.print(depth, node.next_nodes[i])



