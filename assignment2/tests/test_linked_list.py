import unittest
import time

from assignment2.modules.classes.linked_list import *

"""
Please note that testing and benchmarking of any non-class-based programs was 
neglected, as discussed with tutor
"""


class TestLinkedList(unittest.TestCase):

    def test_insert_delete(self):
        ll = LinkedList()

        ll.insert(0, 0)
        for i in range(1000):
            ll.insert(i + 1, i)

        self.assertEqual(ll.head.value, 0)

        for _ in range(1001):
            ll.delete(0)

        self.assertTrue(ll.head is None)

    def test_reverse(self):
        ll = LinkedList()

        ll.insert(0, 0)
        for i in range(1000):
            ll.insert(i + 1, i)

        ll.reverse()
        current = ll.head
        for i in range(1001):
            self.assertEqual(current.value, 1000 - i)
            current = current.next

    def test_exceptions(self):
        ll = LinkedList()

        self.assertEqual(ll.delete(9), None)

        ll.insert(1, 0)

        with self.assertRaises(Exception):
            ll.insert(2, 1)

        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.head.next, None)

    def test_benchmark(self):
        ll = LinkedList()
        start = time.time()

        n = 10 ** 4

        ll.insert(0, 0)
        for i in range(n):
            ll.insert(i + 1, i)

        ll.reverse()

        for _ in range(n + 1):
            ll.delete(0)

        end = time.time()
        elapsed = end - start

        print(
            f"Benchmark insert/delete {n} items and reverse list: {elapsed:.4f} seconds")


if __name__ == "__main__":
    unittest.main()
