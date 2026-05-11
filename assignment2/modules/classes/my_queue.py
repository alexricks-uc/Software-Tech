class Queue(object):
    def __init__(self, size):
        self.max_size = size
        self.q = [None] * size
        self.front = 1
        self.rear = 0
        self.nItems = 0

    def insert(self, item):
        if self.nItems == self.max_size:
            raise Exception("Queue overflow")
        self.rear += 1
        if self.rear == self.max_size:
            self.rear = 0
        self.q[self.rear] = item
        self.nItems += 1
        return True

    def remove(self):
        if self.nItems == 0:
            raise Exception("Queue underflow")
        front = self.q[self.front]
        self.q[self.front] = None
        self.front += 1
        if self.front == self.max_size:
            self.front = 0
        self.nItems -= 1
        return front
