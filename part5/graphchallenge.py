# === starter_template_code ===
# === extended_graph_visualiser.py ===
import copy

from graph import Graph
import tkinter as tk
import math
import time
import threading


class GraphVisualizer(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.title("Graph Visualizer")
        self.geometry('650x650')

        self.graph = graph
        self.directed_graph = copy.deepcopy(graph)
        self.canvas = tk.Canvas(self, width=600, height=600, bg='white')
        self.canvas.pack(pady=10)

        self.vertex_positions = {}
        self.node_radius = 20
        self.spacing = 180
        self.center = (300, 300)

        self.vertex_circles = {}  # vertex -> circle id
        self.edge_lines = {}  # (v, nbr) -> line id

        control_frame = tk.Frame(self)
        control_frame.pack()

        btn_bfs = tk.Button(control_frame, text="Run BFS",
                            command=lambda: self.run_traversal("bfs"))
        btn_bfs.pack(side=tk.LEFT, padx=5)

        btn_dfs = tk.Button(control_frame, text="Run DFS",
                            command=lambda: self.run_traversal("dfs"))
        btn_dfs.pack(side=tk.LEFT, padx=5)

        btn_cycle_undirected = tk.Button(
            control_frame,
            text="Detect Undirected Cycle",
            command=self.run_cycle_detection
        )
        btn_cycle_undirected.pack(side=tk.LEFT, padx=5)

        btn_cycle_directed = tk.Button(
            control_frame,
            text="Detect Directed Cycle",
            command=self.run_directed_cycle_detection
        )
        btn_cycle_directed.pack(side=tk.LEFT, padx=5)

        btn_reset = tk.Button(control_frame, text="Reset Colors",
                              command=self.reset_colors)
        btn_reset.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(self, text="")
        self.info_label.pack(pady=5)

        self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")
        self.vertex_positions.clear()
        self.vertex_circles.clear()
        self.edge_lines.clear()

        vertices = list(self.graph.graph.keys())
        n = len(vertices)

        if n == 0:
            return

        angle_gap = 360 / n
        cx, cy = self.center

        # Position vertices in a circle
        for i, v in enumerate(vertices):
            angle = i * angle_gap
            x = cx + self.spacing * math.cos(math.radians(angle))
            y = cy + self.spacing * math.sin(math.radians(angle))

            self.vertex_positions[v] = (x, y)

            circle_id = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                fill='lightblue', outline='black', width=2
            )

            self.vertex_circles[v] = circle_id
            self.canvas.create_text(x, y, text=v, font=("Arial", 12, "bold"))

        # Draw edges
        for v in vertices:
            x1, y1 = self.vertex_positions[v]

            for nbr in self.graph.graph[v]:
                x2, y2 = self.vertex_positions[nbr]

                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx * dx + dy * dy)

                if dist == 0:
                    continue

                offset_x = dx / dist * self.node_radius
                offset_y = dy / dist * self.node_radius

                start = (x1 + offset_x, y1 + offset_y)
                end = (x2 - offset_x, y2 - offset_y)

                if self.graph.directed:
                    line_id = self.canvas.create_line(
                        start[0], start[1], end[0], end[1],
                        arrow=tk.LAST, width=2
                    )
                else:
                    line_id = self.canvas.create_line(
                        start[0], start[1], end[0], end[1],
                        width=2
                    )

                self.edge_lines[(v, nbr)] = line_id

                if self.graph.weighted:
                    w = self.graph.weights.get((v, nbr), '')
                    mid_x = (start[0] + end[0]) / 2
                    mid_y = (start[1] + end[1]) / 2

                    self.canvas.create_text(
                        mid_x, mid_y,
                        text=str(w),
                        fill="red",
                        font=("Arial", 10, "italic")
                    )

    def reset_colors(self):
        for circle_id in self.vertex_circles.values():
            self.canvas.itemconfig(circle_id, fill='lightblue')

        for edge_id in self.edge_lines.values():
            self.canvas.itemconfig(edge_id, fill='black', width=2)

        self.info_label.config(text="")

    def highlight_vertex(self, vertex, color):
        circle_id = self.vertex_circles.get(vertex)
        if circle_id:
            self.canvas.itemconfig(circle_id, fill=color)
            self.update()

    def highlight_edge(self, v1, v2, color):
        for edge in [(v1, v2), (v2, v1)]:
            line_id = self.edge_lines.get(edge)
            if line_id:
                self.canvas.itemconfig(line_id, fill=color, width=3)
        self.update()

    def run_traversal(self, method):
        def worker():
            self.reset_colors()
            visited = set()

            start_vertex = 'A' if 'A' in self.graph.graph else next(
                iter(self.graph.graph), None)

            if not start_vertex:
                self.info_label.config(text="Graph is empty")
                return

            if method == "bfs":
                queue = [start_vertex]
                self.info_label.config(text="Running BFS...")

                while queue:
                    vertex = queue.pop(0)

                    if vertex not in visited:
                        self.highlight_vertex(vertex, 'orange')
                        self.info_label.config(text=f"BFS visiting: {vertex}")

                        visited.add(vertex)
                        time.sleep(0.7)

                        for nbr in self.graph.graph[vertex]:
                            if nbr not in visited and nbr not in queue:
                                queue.append(nbr)
                                self.highlight_edge(vertex, nbr, 'green')
                                time.sleep(0.3)

                self.info_label.config(text="BFS complete.")

            elif method == "dfs":
                stack = [start_vertex]
                self.info_label.config(text="Running DFS...")

                while stack:
                    vertex = stack.pop()

                    if vertex not in visited:
                        self.highlight_vertex(vertex, 'purple')
                        self.info_label.config(text=f"DFS visiting: {vertex}")

                        visited.add(vertex)
                        time.sleep(0.7)

                        for nbr in reversed(self.graph.graph[vertex]):
                            if nbr not in visited:
                                stack.append(nbr)
                                self.highlight_edge(vertex, nbr, 'blue')
                                time.sleep(0.3)

                self.info_label.config(text="DFS complete.")

        threading.Thread(target=worker, daemon=True).start()

    def run_cycle_detection(self):
        self.reset_colors()
        self.info_label.config(text="Detecting cycles in undirected graph...")

        if self.graph.directed:
            # self.info_label.config(
            #     text="Cycle detection for directed graph is not implemented.")
            # return
            self.graph.directed_to_undirected_conversion()
            self.draw_graph()

        visited = set()

        def cycle_dfs(current, parent):
            visited.add(current)
            self.highlight_vertex(current, 'yellow')
            self.update()
            time.sleep(0.5)

            for nbr in self.graph.graph[current]:
                if nbr not in visited:
                    self.highlight_edge(current, nbr, 'orange')
                    self.update()
                    time.sleep(0.4)

                    if cycle_dfs(nbr, current):
                        return True
                elif parent != nbr:
                    self.highlight_edge(current, nbr, 'red')
                    self.highlight_vertex(current, 'red')
                    self.highlight_vertex(nbr, 'red')
                    self.update()
                    time.sleep(0.5)
                    return True

            return False

        for vertex in self.graph.graph:
            if vertex not in visited:
                if cycle_dfs(vertex, None):
                    self.info_label.config(text="Cycle detected in the graph!")
                    return

        self.info_label.config(text="No cycles found in the graph.")

    def run_directed_cycle_detection(self):
        self.reset_colors()

        if not self.graph.directed:
            # self.info_label.config(
            #     text="Directed cycle detection works only on directed graphs.")
            # return
            self.graph = self.directed_graph
            self.draw_graph()

        self.info_label.config(text="Detecting cycles in directed graph...")

        visited = set()
        rec_stack = set()

        def dfs(vertex):
            visited.add(vertex)
            rec_stack.add(vertex)

            self.highlight_vertex(vertex, 'yellow')
            self.update()
            time.sleep(0.5)

            for nbr in self.graph.graph[vertex]:
                if nbr not in visited:
                    self.highlight_edge(vertex, nbr, 'orange')
                    self.update()
                    time.sleep(0.5)

                    if dfs(nbr):
                        return True

                elif nbr in rec_stack:
                    self.highlight_edge(vertex, nbr, 'red')
                    self.highlight_vertex(vertex, 'red')
                    self.highlight_vertex(nbr, 'red')
                    self.update()
                    time.sleep(0.5)
                    return True

            rec_stack.remove(vertex)
            return False

        for vertex in self.graph.graph:
            if vertex not in visited:
                if dfs(vertex):
                    self.info_label.config(
                        text="Cycle detected in the directed graph!")
                    return

        self.info_label.config(text="No cycles found in the directed graph.")


# === Test Graph ===
if __name__ == "__main__":
    from collections import defaultdict


    class Graph:
        def __init__(self, directed=False, weighted=False):
            self.graph = defaultdict(list)
            self.weights = {}
            self.directed = directed
            self.weighted = weighted

        def add_vertex(self, v):
            if v not in self.graph:
                self.graph[v] = []

        def add_edge(self, v1, v2, weight=0):
            if v1 in self.graph and v2 in self.graph:
                self.graph[v1].append(v2)

                if self.weighted:
                    self.weights[(v1, v2)] = weight

                if not self.directed:
                    self.graph[v2].append(v1)

                    if self.weighted:
                        self.weights[(v2, v1)] = weight

        def directed_to_undirected_conversion(self):
            if self.directed:
                self.directed = False
                for key, val in self.graph.items():
                    for node in val:
                        if key not in self.graph[node]:
                            self.graph[node].append(key)


    # Example graph with a directed cycle
    g = Graph(directed=True)

    for v in ['A', 'B', 'C', 'D', 'E']:
        g.add_vertex(v)

    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    g.add_edge('A', 'E')
    g.add_edge('E', 'D')

    app = GraphVisualizer(g)
    app.mainloop()
