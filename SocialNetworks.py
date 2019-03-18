"""
The idea is that all the 
"""

import numpy as np


class SocialNode:
    COUNT = 0

    def __init__(self, name, geo_position=(0, 0), layer=1, color="b", node_id=None, *args):
        self.name = name
        self.geo_position = geo_position
        self.layer = layer
        self.color = color
        self.node_id = node_id
        for arg in args:
            print("Argument not handled: " + arg)


class SocialNetwork:

    def __init__(self, name):
        self.name = name
        self.Nodes = []
        self.couples_matrix = None
        self.social_matrix = None
        self.coupled_nodes = []

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

    def add_social_edges(self, edge_list, weights = None):
        if weights:
            if len(edge_list) != weights:
                raise Exception("The edge list and the weight list don't have the same length")
            for i in range(len(edge_list)):
                if edge_list[i][0] < edge_list[i][1]:
                    self.social_matrix[edge_list[i][0], edge_list[i][1]] = weights[i]
                else:
                    self.social_matrix[edge_list[i][1], edge_list[i][0]] = weights[i]
        else:
            for i in range(len(edge_list)):
                if edge_list[i][0] < edge_list[1][1]:
                    self.social_matrix[edge_list[i][0], edge_list[i][1]] = 1
                else:
                    self.social_matrix[edge_list[i][1], edge_list[i][0]] = 1

    def remove_social_edges(self, edge_list):
        for edge in edge_list:
            if edge[0] < edge[1]:
                self.social_matrix[edge[0], edge[1]] = 0
            else:
                self.social_matrix[edge[1], edge[0]] = 0

    def add_couple_edges(self, edge_list, weights = None):
        if weights:
            if len(edge_list) != weights:
                raise Exception("The edge list and the weight list don't have the same length")
            for i in range(len(edge_list)):
                if edge_list[i][0] < edge_list[i][1]:
                    self.couples_matrix[edge_list[i][0], edge_list[i][1]] = weights[i]
                else:
                    self.couples_matrix[edge_list[i][1], edge_list[i][0]] = weights[i]

                self.coupled_nodes.append(edge_list[i][0])
                self.coupled_nodes.append(edge_list[i][1])
        else:
            for i in range(len(edge_list)):
                if edge_list[i][0] < edge_list[1][1]:
                    self.couples_matrix[edge_list[i][0], edge_list[i][1]] = 1
                else:
                    self.couples_matrix[edge_list[i][1], edge_list[i][0]] = 1

                self.coupled_nodes.append(edge_list[i][0])
                self.coupled_nodes.append(edge_list[i][1])

    def remove_couple_edges(self, edge_list):
        for edge in edge_list:
            if edge[0] < edge[1]:
                self.couples_matrix[edge[0], edge[1]] = 0
            else:
                self.couples_matrix[edge[1], edge[0]] = 0

            self.coupled_nodes.remove(edge[0])
            self.coupled_nodes.remove(edge[1])

    def get_social_neighbors(self, index=None, name=None, node_id=None):
        node_number = len(self.Nodes)
        if node_id:
            # TODO Check if this works
            index = [i for i in range(node_number) if self.Nodes[i].node_id == node_id][0]
            return [1 if (self.social_matrix[index][i] or self.social_matrix[i][index]) else 0
                    for i in range(node_number)]
        elif name:
            index = [i for i in range(node_number) if self.Nodes[i].name == name][0]
            return [1 if (self.social_matrix[index][i] or self.social_matrix[i][index]) else 0
                    for i in range(node_number)]
        elif index:
            return [1 if (self.social_matrix[index][i] or self.social_matrix[i][index]) else 0
                    for i in range(node_number)]
        else:
            return None

    def add_random_couple(self):
        available_nodes = [index for index in range(len(self.Nodes)) if index not in self.coupled_nodes]
        first_node = available_nodes[np.random.randint(len(available_nodes))]
        available_nodes.remove(first_node)
        second_node = available_nodes[np.random.randint(len(available_nodes))]
        self.add_couple_edges([(first_node, second_node)])