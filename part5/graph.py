from collections import deque


class Graph:
    def __init__(self, directed=False, weighted=False):
        self.graph = {}  # Initialize an empty dictionary to store the adjacency list
        self.weights = {}
        self.directed = directed
        self.weighted = weighted

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[
                vertex] = []  # Add a new vertex with an empty list of edges

    def add_edge(self, vertex1, vertex2, weight=0):
        if vertex1 in self.graph and vertex2 in self.graph:
            # Check that vertices are present
            # store vertex and weight as a tuple
            self.graph[vertex1].append(vertex2)
            if self.weighted:
                self.weights[(vertex1, vertex2)] = weight
            if not self.directed:  # In the case of an undirected graph, append in both directions
                self.graph[vertex2].append(vertex1)
                if self.weighted:
                    self.weights[(vertex2, vertex1)] = weight
        else:
            print("One or both vertices not found in graph.")

    def remove_edge(self, vertex1, vertex2):
        if self.weighted:
            for key, val in self.graph.items():
                if key == vertex1 and vertex2 in val:
                    val.remove(vertex2)
                    self.weights.pop((vertex1, vertex2))
                if key == vertex2 and vertex1 in val:
                    val.remove(vertex1)
                    self.weights.pop((vertex2, vertex1))
        else:
            for key, val in self.graph.items():
                if key == vertex1 and vertex2 in val:
                    val.remove(vertex2)
                if key == vertex2 and vertex1 in val:
                    val.remove(vertex1)

    def remove_vertex(self, vertex):
        if self.weighted:
            for key, val in self.graph.copy().items():
                if key == vertex:
                    self.graph.pop(vertex)
                    continue
                if vertex in val:
                    val.remove(vertex)
            for key in self.weights.copy().keys():
                if vertex in key:
                    self.weights.pop(key)
        else:
            for key, val in self.graph.copy().items():
                if key == vertex:
                    self.graph.pop(vertex)
                    continue
                if vertex in val:
                    val.remove(vertex)

    def print_graph(self):
        print(self.graph)
        if self.weighted:
            print(self.weights)

    def bfs(self, start):
        visited = []
        q = deque()
        visited.append(start)
        q.append(start)
        result = []
        while q:
            curr = q.popleft()
            result.append(curr)
            neighbours = self.graph[curr]
            for n in neighbours:
                if n not in visited:
                    visited.append(n)
                    q.append(n)
        return result

    def dfs(self, start):
        visited = []
        result = []
        stack = [start]
        while stack:
            curr = stack.pop()
            if curr in visited: continue
            visited.append(curr)
            result.append(curr)
            l = len(self.graph[curr])
            for i in range(l - 1, -1, -1):
                neighbour = self.graph[curr][i]
                if neighbour not in visited:
                    stack.append(neighbour)
        return result

    def cycle_helper(self, start, visited, parent):
        visited.append(start)
        neighbours = self.graph[start]
        for n in neighbours:
            if n not in visited:
                if self.cycle_helper(n, visited, start):
                    return True
            elif n != parent:
                return True
        return False

    def has_undirected_cycle(self):
        visited = []
        for key in self.graph.keys():
            if key not in visited:
                if self.cycle_helper(key, visited, None):
                    return True
        return False
