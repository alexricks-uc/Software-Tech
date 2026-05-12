"""
A class representation of a queue, used for testing and benchmarking
"""


class Queue(object):
    """
    Defines a queue with a maximum size, a list representation, front and rear
    positions in the list representation and a number of items
    """

    def __init__(self, size):
        """
        Initialises the queue
        :param size:
        """
        self.max_size = size
        self.q = [None] * size
        self.front = 1
        self.rear = 0
        self.nItems = 0

    def insert(self, item):
        """
        Adds an item to the end of the queue
        :param item:
        :return: True for successful insertion
        """
        if self.nItems == self.max_size:
            raise Exception("Queue overflow")
        self.rear += 1
        if self.rear == self.max_size:
            self.rear = 0
        self.q[self.rear] = item
        self.nItems += 1
        return True

    def remove(self):
        """
        Removes the first item in the queue
        :return: the item at the front of the queue which was removed
        """
        if self.nItems == 0:
            raise Exception("Queue underflow")
        front = self.q[self.front]
        self.q[self.front] = None
        self.front += 1
        if self.front == self.max_size:
            self.front = 0
        self.nItems -= 1
        return front
