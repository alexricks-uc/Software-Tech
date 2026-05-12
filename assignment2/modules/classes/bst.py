class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        def _insert(node, value):
            if not node:
                return BSTNode(value)
            if value < node.value:
                node.left = _insert(node.left, value)
            elif value > node.value:
                node.right = _insert(node.right, value)
            return node

        self.root = _insert(self.root, value)

    def search(self, value):
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
        result = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder(self):
        result = []

        def _preorder(node):
            if node:
                result.append(node)
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder(self):
        result = []

        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node)

        _postorder(self.root)
        return result
