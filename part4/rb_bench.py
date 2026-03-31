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


# ===== RB Node and RB Tree Class =====
class RBNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None
        self.parent = None
        self.color = "red"


class RBTree:
    def __init__(self):
        self.blank = RBNode(None, None)
        self.blank.color = "black"
        self.root = self.blank

    def left_rotate(self, z):
        y = z.right
        z.right = y.left
        if y.left != self.blank:
            y.left.parent = z
        y.parent = z.parent
        if z.parent is None:
            self.root = y
        elif z == z.parent.left:
            z.parent.left = y
        else:
            z.parent.right = y
        y.left = z
        z.parent = y

    def right_rotate(self, z):
        y = z.left
        z.left = y.right
        if y.right != self.blank:
            y.right.parent = z
        y.parent = z.parent
        if z.parent is None:
            self.root = y
        elif z == z.parent.right:
            z.parent.right = y
        else:
            z.parent.left = y
        y.right = z
        z.parent = y

    def insert(self, name, phone):
        node = RBNode(name, phone)
        node.parent = None
        node.left = self.blank
        node.right = self.blank
        node.color = "red"
        y = None
        x = self.root
        while x != self.blank:
            y = x
            if node.name < x.name:
                x = x.left
            elif node.name > x.name:
                x = x.right
            else:
                x.phone = phone
                return self.root
        node.parent = y
        if y is None:
            self.root = node
        elif node.name < y.name:
            y.left = node
        else:
            y.right = node
        if node.parent is None:
            node.color = "black"
            return self.root
        if node.parent.parent is None:
            return self.root
        self.fix_insert_mistakes(node)
        return self.root

    def fix_insert_mistakes(self, node):
        while node.parent.color == "red":
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color == "red":
                    uncle.color = "black"
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                if uncle.color == "red":
                    uncle.color = "black"
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = "black"

    def search(self, node, name):
        if node == self.blank or name == node.name:
            return node
        if name < node.name:
            return self.search(node.left, name)
        return self.search(node.right, name)

    def rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, name):
        z = self.search(self.root, name)
        if z == self.blank:
            return self.root
        y = z
        y_original_color = y.color
        if z.left == self.blank:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.blank:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self.fix_delete_mistakes(x)
        return self.root

    def minimum(self, node):
        while node.left != self.blank:
            node = node.left
        return node

    def fix_delete_mistakes(self, node):
        while node != self.root and node.color == "black":
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == "red":
                    sibling.color = "black"
                    node.parent.color = "red"
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                if sibling.left.color == "black" and sibling.right.color == "black":
                    sibling.color = "red"
                    node = node.parent
                else:
                    if sibling.right.color == "black":
                        sibling.left.color = "black"
                        sibling.color = "red"
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = "black"
                    sibling.right.color = "black"
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == "red":
                    sibling.color = "black"
                    node.parent.color = "red"
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                if sibling.right.color == "black" and sibling.left.color == "black":
                    sibling.color = "red"
                    node = node.parent
                else:
                    if sibling.left.color == "black":
                        sibling.right.color = "black"
                        sibling.color = "red"
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = "black"
                    sibling.left.color = "black"
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = "black"

    def inorder(self, node, result=None):
        if result is None:
            result = []
        if node != self.blank:
            self.inorder(node.left, result)
            result.append((node.name, node.phone))
            self.inorder(node.right, result)
        return result


# ===== Benchmarking Function =====
def benchmark(n=1000, search_fraction=0.5, delete_count=100, verbose=True):
    # Generate test data
    names = [''.join(random.choices(string.ascii_lowercase, k=10)) for _ in
             range(n)]
    phones = [''.join(random.choices(string.digits, k=10)) for _ in
              range(n)]
    # --- BST benchmark ---
    bst = BST()
    bst.root = None
    # Insert
    start = time.time()
    for i in range(n):
        bst.root = bst.insert(bst.root, names[i], phones[i])
    bst_insert_time = time.time() - start
    # Search
    search_names = random.sample(names, int(n * search_fraction)) + [
        'notfoundname'] * int(n * (1 - search_fraction))
    start = time.time()
    found_bst = sum(
        1 for name in search_names if bst.search(bst.root, name))
    bst_search_time = time.time() - start
    # Delete
    delete_names = random.sample(names, delete_count)
    start = time.time()
    for name in delete_names:
        bst.root = bst.delete(bst.root, name)
    bst_delete_time = time.time() - start
    # --- AVL benchmark ---
    avl = AVLTree()
    avl.root = None
    # Insert
    start = time.time()
    for i in range(n):
        avl.root = avl.insert(avl.root, names[i], phones[i])
    avl_insert_time = time.time() - start
    # Search
    start = time.time()
    found_avl = sum(
        1 for name in search_names if avl.search(avl.root, name))
    avl_search_time = time.time() - start
    # Delete
    start = time.time()
    for name in delete_names:
        avl.root = avl.delete(avl.root, name)
    avl_delete_time = time.time() - start
    rb = RBTree()
    start = time.time()
    for i in range(n):
        rb.insert(names[i], phones[i])
    rb_insert_time = time.time() - start
    start = time.time()
    found_rb = sum(
        1 for name in search_names if rb.search(rb.root, name) != rb.blank)
    rb_search_time = time.time() - start
    start = time.time()
    for name in delete_names:
        rb.delete(name)
    rb_delete_time = time.time() - start
    # Prepare results
    results = {
        'Insertions': (bst_insert_time, avl_insert_time, rb_insert_time),
        'Searches': (bst_search_time, avl_search_time, rb_search_time),
        'Deletions': (bst_delete_time, avl_delete_time, rb_delete_time),
        'Found In Search': (found_bst, found_avl, found_rb)
    }
    if verbose:
        print(f"Benchmarking with {n} entries:\n")
        print("Operation BST Time (sec) AVL Time (sec)")
        print("---------------------------------------------")
        print(
            f"Insertions: {bst_insert_time:.6f} {avl_insert_time:.6f} {rb_insert_time:.6f}")
        print(
            f"Searches: {bst_search_time:.6f} {avl_search_time:.6f} {rb_search_time:.6f}")
        print(
            f"Deletions: {bst_delete_time:.6f} {avl_delete_time:.6f} {rb_delete_time:.6f}")
        print("---------------------------------------------")
        print(f"Contacts found in search:")
        print(f"BST: {found_bst} / {len(search_names)}")
        print(f"AVL: {found_avl} / {len(search_names)}")
        print(f"RB: {found_rb} / {len(search_names)}")
    return results


# ===== Tkinter GUI to show benchmark results =====
class BenchmarkApp:
    def __init__(self, master):
        self.master = master
        master.title("BST vs AVL Benchmark")
        self.label = tk.Label(master, text="Run benchmark with 1000 entries?")
        self.label.pack(pady=5)
        self.run_btn = tk.Button(master, text="Run Benchmark",
                                 command=self.run_benchmark)
        self.run_btn.pack(pady=5)
        self.result_text = tk.Text(master, height=15, width=50)
        self.result_text.pack(pady=10)
        self.tree = ttk.Treeview(master, columns=("BST", "AVL", "RB"),
                                 show='headings')
        self.tree.heading("BST", text="BST Time (s)")
        self.tree.heading("AVL", text="AVL Time (s)")
        self.tree.heading("RB", text="RB Time (s)")
        self.tree.pack(pady=10)

    def run_benchmark(self):
        self.result_text.delete(1.0, tk.END)
        results = benchmark(verbose=False)  # silent print
        # Display text summary
        summary = (
            f"Insertion Time: BST: {results['Insertions'][0]:.6f}s, AVL: {results['Insertions'][1]:.6f}s, RB: {results['Insertions'][2]:.6f}s\n"
            f"Search Time: BST: {results['Searches'][0]:.6f}s, AVL: {results['Searches'][1]:.6f}s, RB: {results['Searches'][2]:.6f}s\n"
            f"Deletion Time: BST: {results['Deletions'][0]:.6f}s, AVL: {results['Deletions'][1]:.6f}s, RB: {results['Deletions'][2]:.6f}s\n"
            f"Found in Search: BST: {results['Found In Search'][0]}, AVL: {results['Found In Search'][1]}, RB: {results['Found In Search'][2]} out of 1000\n"
        )
        self.result_text.insert(tk.END, summary)
        # Clear previous treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insert new data rows
        for op in ['Insertions', 'Searches', 'Deletions']:
            bst_time, avl_time = results[op]
            self.tree.insert('', tk.END,
                             values=(f"{bst_time:.6f}", f"{avl_time:.6f}"),
                             text=op)


# ===== Run the app =====
if __name__ == "__main__":
    root = tk.Tk()
    app = BenchmarkApp(root)
    root.mainloop()
