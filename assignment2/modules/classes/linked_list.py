import copy

"""
A class representation of a linked list, used for testing and benchmarking
"""


class Node:
    """
    Defines node in linked list, with value and next node
    """

    def __init__(self, value):
        """
        Initialises node with value and next node
        :param value: value of the node
        """
        self.value = value
        self.next = None


class LinkedList:
    """
    Defines a linked list with insert, delete and reverse methods
    """

    def __init__(self):
        """
        Initialises linked list with head node
        """
        self.head = None

    def insert(self, value, pos):
        """
        Traverses the linked list to a given position and inserts new node there
        :param value: value of new node
        :param pos: position to insert the node in
        """
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
        """
        Traverses to given position and deletes the node by linking its
        predecessor to its successor
        :param pos: position in the linked list of deleted node
        """
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
        """
        Reverses the linked list by adding all nodes to a list, popping from
        the end of the list, setting the popped node to be the head and popping
        and linking each node until the list is empty
        """
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
