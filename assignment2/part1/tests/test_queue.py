import unittest
import time

from assignment2.part1.modules.my_queue import Queue


class TestStack(unittest.TestCase):

    def test_enq_deq(self):
        q = Queue(1000)

        for i in range(1000):
            q.insert(i)

        self.assertEqual(q.nItems, 1000)

        for i in range(1000):
            v = q.remove()
            self.assertEqual(v, i)

        self.assertTrue(q.nItems == 0)

    def test_exceptions(self):
        q = Queue(1000)

        with self.assertRaises(Exception):
            q.remove()

        for i in range(1000):
            q.insert(i)

        with self.assertRaises(Exception):
            q.insert(1001)

        self.assertEqual(q.nItems, 1000)
        self.assertEqual(q.front, 1)
        self.assertEqual(q.rear, 0)

    def test_benchmark(self):
        q = Queue(1000000)
        start = time.time()

        n = 10 ** 6

        for i in range(n):
            q.insert(i)

        for i in range(n):
            q.remove()

        end = time.time()
        elapsed = end - start

        print(f"Benchmark enqueue/dequeue {n} items: {elapsed:.4f} seconds")


if __name__ == "__main__":
    unittest.main()
