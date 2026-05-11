import copy


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value, pos):
        if not self.head:
            self.head = Node(value)
            return

        current = self.head
        for _ in range(pos):
            current = current.next
        pos += 1
        temp = current.next
        current.next = Node(value)
        current.next.next = temp

    def delete(self, pos):
        if not self.head:
            return
        current = self.head
        prev = None
        for _ in range(pos):
            prev = current
            current = current.next
        if prev:
            prev.next = current.next
        else:
            self.head = current.next

    def reverse(self):
        current = self.head
        unconnected = []
        while current:
            temp = copy.copy(current)
            temp.next = None
            unconnected.append(temp)
            current = current.next
        if unconnected:
            new_head = unconnected.pop()
            self.head = new_head
            self.head.next = None
            current = self.head
            while unconnected:
                new = unconnected.pop()
                current.next = new
                current = current.next
