import random
import time
import unittest

from assignment2.modules.classes.bst import *


class TestBST(unittest.TestCase):

    def test_insert_search(self):

        bst = BST()

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        found, path = bst.search(70)

        self.assertTrue(found)
        self.assertEqual(path[-1].value, 70)

    def test_inorder(self):

        bst = BST()

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)

        result = bst.inorder()

        values = []

        for node in result:
            values.append(node.value)

        self.assertEqual(values, [20, 30, 40, 50, 70])

    def test_preorder(self):

        bst = BST()

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        result = bst.preorder()

        values = []

        for node in result:
            values.append(node.value)

        self.assertEqual(values, [50, 30, 70])

    def test_postorder(self):

        bst = BST()

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        result = bst.postorder()

        values = []

        for node in result:
            values.append(node.value)

        self.assertEqual(values, [30, 70, 50])

    def test_find_parent(self):

        bst = BST()

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        parent, side = bst.find_parent(30)

        self.assertEqual(parent.value, 50)
        self.assertEqual(side, "left")

    def test_delete(self):

        bst = BST()

        bst.insert(50)
        bst.insert(30)
        bst.insert(70)

        node = bst.search(30)[1][-1]

        bst.delete(node, None)

        result = bst.inorder()

        values = []

        for node in result:
            values.append(node.value)

        self.assertEqual(values, [50, 70])

    def test_benchmark(self):
        bst = BST()
        start = time.time()
        to_insert = [random.randint(1, 10000) for _ in range(10000)]

        for item in to_insert:
            bst.insert(item)

        for item in to_insert:
            bst.search(item)

        for item in to_insert:
            found, path = bst.search(item)
            if found:
                node = path[-1]
                successor = None
                if node.left and node.right:
                    successor = node.right
                    while successor.left:
                        successor = successor.left
                bst.delete(node, successor)

        end = time.time()
        elapsed = end - start

        print(
            f"Benchmark insert/search/delete 10000 items: {elapsed:.4f} seconds")


if __name__ == "__main__":
    unittest.main()
