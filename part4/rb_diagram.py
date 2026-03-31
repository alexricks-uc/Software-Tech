from collections import deque
from tkinter import messagebox
import time
import random
import string
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


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


class RBApp:
    def __init__(self, master):
        self.tree = RBTree()
        self.master = master
        master.title("RB Tree Contact Directory")
        self.frame = tk.Frame(master)
        self.frame.pack(pady=10)
        tk.Label(self.frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1)
        tk.Label(self.frame, text="Phone:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.grid(row=1, column=1)
        self.btn_frame = tk.Frame(master)
        self.btn_frame.pack(pady=5)
        tk.Button(self.btn_frame, text="Insert",
                  command=self.insert_contact).grid(row=0, column=0, padx=5)
        tk.Button(self.btn_frame, text="Search",
                  command=self.search_contact).grid(row=0, column=1, padx=5)
        tk.Button(self.btn_frame, text="Delete",
                  command=self.delete_contact).grid(row=0, column=2, padx=5)
        tk.Button(self.btn_frame, text="Show All", command=self.show_all).grid(
            row=0, column=3, padx=5)
        self.output_text = tk.Text(master, height=10, width=60)
        self.output_text.pack(pady=10)
        self.canvas = tk.Canvas(master, width=800, height=400, bg="white")
        self.canvas.pack(pady=10)

    def insert_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Input Error",
                                   "Please enter both Name and Phone.")
            return
        self.tree.insert(name, phone)
        messagebox.showinfo("Success", f"Inserted/Updated contact: {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def search_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error",
                                   "Please enter Name to search.")
            return
        node = self.tree.search(self.tree.root, name)
        self.output_text.delete(1.0, tk.END)
        if node != self.tree.blank:
            self.output_text.insert(tk.END,
                                    f"Found Contact:\nName: {node.name}\nPhone: {node.phone}\n")
        else:
            self.output_text.insert(tk.END, "Contact not found.\n")

    def delete_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error",
                                   "Please enter Name to delete.")
            return
        self.tree.delete(name)
        messagebox.showinfo("Success", f"Deleted contact (if existed): {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def show_all(self):
        self.output_text.delete(1.0, tk.END)
        contacts = self.tree.inorder(self.tree.root)
        if not contacts:
            self.output_text.insert(tk.END, "No contacts found.\n")
        else:
            for n, p in contacts:
                self.output_text.insert(tk.END, f"Name: {n}, Phone: {p}\n")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def draw_tree(self):
        self.canvas.delete("all")
        if self.tree.root == self.tree.blank:
            return
        width = self.canvas.winfo_width()
        if width <= 1: width = 800
        self._draw_node(self.tree.root, width // 2, 30, width // 4)

    def _draw_node(self, node, x, y, x_offset):
        if node == self.tree.blank:
            return
        radius = 20
        if node.left != self.tree.blank:
            x_left = x - x_offset
            y_left = y + 70
            self.canvas.create_line(x, y + radius, x_left, y_left - radius)
            self._draw_node(node.left, x_left, y_left, x_offset // 2)
        if node.right != self.tree.blank:
            x_right = x + x_offset
            y_right = y + 70
            self.canvas.create_line(x, y + radius, x_right, y_right - radius)
            self._draw_node(node.right, x_right, y_right, x_offset // 2)
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=node.color)
        display_name = str(node.name) if len(str(node.name)) <= 10 else str(
            node.name)[:10] + "..."
        self.canvas.create_text(x, y, text=display_name,
                                font=("Arial", 10, "bold"), fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = RBApp(root)
    root.mainloop()
