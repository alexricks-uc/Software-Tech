from collections import deque
from tkinter import messagebox
import time
import random
import string
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


# ===== BST Node and BST Class =====
class Node:
    def __init__(self, name, phone=None):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, name, phone):
        if root is None:
            return Node(name, phone)
        if name < root.name:
            root.left = self.insert(root.left, name, phone)
        elif name > root.name:
            root.right = self.insert(root.right, name, phone)
        else:
            root.phone = phone
        return root

    def search(self, root, name):
        if root is None or root.name == name:
            return root
        if name < root.name:
            return self.search(root.left, name)
        else:
            return self.search(root.right, name)

    def find_min(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def delete(self, root, name):
        if root is None:
            return root
        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            # Node with one or no children
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            # Node with two children
            temp = self.find_min(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)
        return root


# ===== AVL Node and AVL Tree Class =====
class AVLNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, node, name, phone):
        if not node:
            return AVLNode(name, phone)
        if name < node.name:
            node.left = self.insert(node.left, name, phone)
        elif name > node.name:
            node.right = self.insert(node.right, name, phone)
        else:
            node.phone = phone
            return node
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        balance = self.get_balance(node)
        # Rotations
        if balance > 1 and name < node.left.name:
            return self.right_rotate(node)
        if balance < -1 and name > node.right.name:
            return self.left_rotate(node)
        if balance > 1 and name > node.left.name:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and name < node.right.name:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, root, name):
        if not root:
            return root
        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.min_value_node(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.get_balance(root)
        # Balancing
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def search(self, node, name):
        if node is None or node.name == name:
            return node
        if name < node.name:
            return self.search(node.left, name)
        else:
            return self.search(node.right, name)


# Re-use BST and AVL classes from previous code
# Use BST and AVLTree classes already defined with
# insert/search/delete methods.

def run_benchmark_for_sizes(sizes, num_search=100, num_delete=50):
    bst_times = {'insert': [], 'search': [], 'delete': []}
    avl_times = {'insert': [], 'search': [], 'delete': []}
    rb_times = {'insert': [], 'search': [], 'delete': []}
    for n in sizes:
        names = [''.join(random.choices(string.ascii_lowercase, k=8)) for _ in
                 range(n)]
        phones = [''.join(random.choices(string.digits, k=10)) for _ in
                  range(n)]
        search_names = random.sample(names, min(num_search, n))
        delete_names = random.sample(names, min(num_delete, n))
        bst = BST()
        start = time.time()
        for i in range(n):
            bst.root = bst.insert(bst.root, names[i], phones[i])
        bst_times['insert'].append(time.time() - start)
        start = time.time()
        for name in search_names:
            bst.search(bst.root, name)
        bst_times['search'].append(time.time() - start)
        start = time.time()
        for name in delete_names:
            bst.root = bst.delete(bst.root, name)
        bst_times['delete'].append(time.time() - start)
        avl = AVLTree()
        start = time.time()
        for i in range(n):
            avl.root = avl.insert(avl.root, names[i], phones[i])
        avl_times['insert'].append(time.time() - start)
        start = time.time()
        for name in search_names:
            avl.search(avl.root, name)
        avl_times['search'].append(time.time() - start)
        start = time.time()
        for name in delete_names:
            avl.root = avl.delete(avl.root, name)
        avl_times['delete'].append(time.time() - start)
        rb = RBTree()
        start = time.time()
        for i in range(n):
            rb.root = rb.insert(names[i], phones[i])
        rb_times['insert'].append(time.time() - start)
        start = time.time()
        for name in search_names:
            rb.search(rb.root, name)
        rb_times['search'].append(time.time() - start)
        start = time.time()
        for name in delete_names:
            rb.root = rb.delete(name)
        rb_times['delete'].append(time.time() - start)

    # Plot results
    plt.figure(figsize=(10, 12))
    metrics = ['insert', 'search', 'delete']
    for i, metric in enumerate(metrics, 1):
        plt.subplot(3, 1, i)
        plt.plot(sizes, bst_times[metric], label=f'BST {metric.capitalize()}')
        plt.plot(sizes, avl_times[metric], label=f'AVL {metric.capitalize()}')
        plt.plot(sizes, rb_times[metric],
                 label=f'RB {metric.capitalize()}')
        plt.ylabel('Time (seconds)')
        plt.title(f'{metric.capitalize()} Time vs Input Size')
        plt.legend()
    plt.xlabel('Number of Nodes')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sizes_to_test = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
    run_benchmark_for_sizes(sizes_to_test)
