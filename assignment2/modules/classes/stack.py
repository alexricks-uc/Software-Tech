"""
A class representation of a stack, used for testing and benchmarking
"""


class Stack:
    """
    Defines a stack with push, pop and peek methods, as well as methods to return
    the size, whether the list is empty, and a string representation
    """

    def __init__(self):
        """
        Initialises the stack with a list of the data in it
        """
        self._data = []

    def push(self, val):
        """
        Appends an item to the end of the list
        :param val: item appended
        """
        self._data.append(val)

    def pop(self):
        """
        Pops a value from the stack
        :return: the value popped
        """
        if not self.is_empty():
            return self._data.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        """
        Peeks the item at the end of the list
        :return: item at end of list
        """
        if not self.is_empty():
            return self._data[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        """
        Checks if the stack is empty
        :return: boolean for whether the stack is empty
        """
        return len(self._data) == 0

    def size(self):
        """
        Returns size of stack
        :return: length of data list
        """
        return len(self._data)

    def __repr__(self):
        """
        Returns string representation of data list
        :return: string representation of data list
        """
        return f"Stack({self._data})"
