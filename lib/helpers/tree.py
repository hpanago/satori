# -*- coding: utf-8 -*-

__author__ = 'Hung Viet Nguyen'
__email__ = 'thegod1702@gmail.com'
__version__ = '0.1.0'


class Node:
    """
    Generic node class
    """
    def __init__(self, data, parent=None):
        """
        Constructor with input arguments is data of a Node
         and the parent node (if require)
        """
        self.__children = []
        self.__data = data
        self.__parent = parent

    def add_child(self, node):
        """
        Add a node child to the current node
        """
        if node in self.__children:
            raise ValueError('Node has already is children')
        else:
            self.__children.append(node)
            node.__parent = self

    def delete_child(self, node):
        """
        Delete a node child if it's in the current node
        """
        self.__children.remove(node)

    def is_root(self):
        """
        Check if the current node is the root node (has no parent)
        """
        return self.__parent is None

    def is_parent(self):
        """
        Check if the the current node is the parent node (has child & also has parent)
        """
        return self.__children > 0

    def is_leaf(self):
        """
        Check if the the current node is the leaf node (has no child)
        """
        return len(self.__children) == 0

    def at_level(self):
        """
        Return the level of current node is at
        """
        if self.__parent is not None:
            return 1 + self.__parent.at_level()
        else:
            return 1

    def get_child_list(self):
        """
        Get the list of children of the current node
        """
        return self.__children

    def get_data(self):
        """
        Get the data of children of the current node
        """
        return self.__data

    def set_data(self, data):
        """
        Set the data of children of the current node
        """
        self.__data = data

    def get_parent(self):
        """
        Get the parent node of children of the current node
        """
        return self.__parent

    def __str__(self, level=0):
        """
        Get presentation of node
        """
        ret = "\t" * level + "|---" + "{}".format(self.__data) + "\n"
        for child in self.__children:
            ret += child.__str__(level + 1)
        return ret


class OperatorNode(Node):
    def __init__(self, operator, data=None, parent=None):
        Node.__init__(self, data, parent)
        self.__operator = operator

    def set_operator(self, operator):
        self.__operator = operator

    def process_node(self):
        result = self.get_data()
        iterator = iter(self.get_child_list())
        for child in iterator:
            next_child = next(iterator)
            if next_child is None:
                self.__operator(child.process_node(), result)
            else:
                result = self.__operator(child.process_node(), next_child.process_node())
            self.delete_child(child)
        self.__operator = None
        self.set_data(result)
        return self.get_data()
