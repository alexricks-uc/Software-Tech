"""
A class representation of a BST, used for testing and benchmarking
"""


class BSTNode:
    """
    Defines node of a BST with value, left and right
    """

    def __init__(self, value):
        """
        Initialises the node with value, left and right
        :param value:
        """
        self.value = value
        self.left = None
        self.right = None


class BST:
    """
    Defines a BST with functions for inserting, deleting, searching and
    traversing, as well as for finding parent of a node of given value
    """

    def __init__(self):
        """
        Initialises the BST with root
        """
        self.root = None

    def insert(self, value):
        """
        Calls recursive _insert with the root and the value parameter
        :param value: value to be inserted
        """

        def _insert(node, value):
            """
            Recursively searches for a space to insert the new node
            :param node: current node
            :param value: value to be inserted
            :return: the inserted node
            """
            if not node:
                return BSTNode(value)
            if value < node.value:
                node.left = _insert(node.left, value)
            elif value > node.value:
                node.right = _insert(node.right, value)
            return node

        self.root = _insert(self.root, value)

    def search(self, value):
        """
        Searches for a given value and builds the path taken
        :param value: value to be found
        :return: whether the value was found and the path taken
        """
        node = self.root
        found = False
        path = []
        while node:
            path.append(node)
            if node.value == value:
                found = True
                break
            elif node.value < value:
                node = node.right
            else:
                node = node.left
        return found, path

    def find_parent(self, value):
        """
        Finds the parent of a node of the given value and which side of the
        parent the node is on
        :param value: value of
        """
        node = self.root
        parent = None
        current_side = "neither"
        while node:
            if node.value == value:
                return parent, current_side
            if node.value < value:
                parent = node
                node = node.right
                current_side = "right"
            if node.value > value:
                parent = node
                node = node.left
                current_side = "left"

    def delete(self, node, successor):
        """
        Determines which rotation to perform depending on the children and
        parent of the given node and successor, then removes the node
        :param node: node to be deleted
        :param successor: the node of the next largest value after the given node
        """
        if node:
            parent, side = self.find_parent(node.value)
            if not node.left and not node.right:
                if not parent:
                    self.root = None
                elif side == "left":
                    parent.left = None
                else:
                    parent.right = None
            elif not node.left:
                if not parent:
                    self.root = self.root.right
                elif side == "left":
                    parent.left = node.right
                else:
                    parent.right = node.right
            elif not node.right:
                if not parent:
                    self.root = self.root.left
                elif side == "left":
                    parent.left = node.left
                else:
                    parent.right = node.left
            else:
                successor_parent, side = self.find_parent(successor.value)
                node.value = successor.value
                if not successor.right:
                    if side == "left":
                        successor_parent.left = None
                    else:
                        successor_parent.right = None
                else:
                    if side == "left":
                        successor_parent.left = successor.right
                    else:
                        successor_parent.right = successor.right

    def inorder(self):
        """
        Calls the recursive _inorder function on the root
        :return: the list of nodes visited in order
        """
        result = []

        def _inorder(node):
            """
            Recursively traverses the tree from smallest to largest value
            :param node: current node being traversed
            """
            if node:
                _inorder(node.left)
                result.append(node)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder(self):
        """
        Calls the recursive _preorder function on the root
        :return: the list of nodes visited in order
        """
        result = []

        def _preorder(node):
            """
            Recursively traverses the tree, appending the root node followed by
            the left node and all subsequent left nodes, then the leftmost
            right node and so on
            :param node: current node being traversed
            """
            if node:
                result.append(node)
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder(self):
        """
        Calls the recursive _postorder function on the root
        :return: the list of nodes visited in order
        """
        result = []

        def _postorder(node):
            """
            Recursively traverses the tree from the lowest depth nodes of each
            subtree up to the root, starting on the left subtree
            :param node: current node being traversed
            """
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node)

        _postorder(self.root)
        return result
