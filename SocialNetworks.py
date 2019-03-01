import numpy as np


class SocialNode:
    COUNT = 0

    def __init__(self, name, geo_position=(0, 0), layer=1, color="b", *args):
        self.name = name
        self.geo_position = geo_position
        self.layer = layer
        self.color = color
        for arg in args:
            print("Argument not handled: " + arg)


class SocialNetwork:

    def __init__(self, name):
        self.name = name
        self.Nodes = []
        self.couples_matrix = None
        self.social_matrix = None

    def add_node(self, new_node):
        self.Nodes.append(new_node)

        if not self.couples_matrix:
            self.couples_matrix = np.zeros([1, 1])
        else:
            new_matrix = np.zeros([len(self.Nodes), len(self.Nodes)])
            new_matrix[:len(self.Nodes)-1, :len(self.Nodes)-1] = self.couples_matrix
            self.couples_matrix = new_matrix

        if not self.social_matrix:
            self.social_matrix = np.zeros([1, 1])
        else:
            new_matrix = np.zeros([len(self.Nodes), len(self.Nodes)])
            new_matrix[:len(self.Nodes)-1, :len(self.Nodes)-1] = self.social_matrix
            self.social_matrix = new_matrix

    def get_social_neighbors(self, index = None, name =None, ID = None):
        if ID:
            raise NotImplemented("Function not yet implemented")
        elif name:
            raise NotImplemented("Function not yet implemented")
        elif index:
            raise NotImplemented("Function not yet implemented")
        else:
            return None
