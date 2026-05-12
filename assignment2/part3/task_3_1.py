import collections
import pygame

"""
Visualises graph traversals
"""

pygame.init()
WIDTH, HEIGHT = 600, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
# Graph nodes positioned manually
nodes_pos = {
    'A': (100, 100),
    'B': (250, 60),
    'C': (250, 200),
    'D': (400, 100),
    'E': (500, 150),
    'F': (400, 300)
}
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}


def draw_graph(visited=[], frontier=set(), current=None):
    """
    Draws the graph
    :param visited: list of nodes already traversed
    :param frontier: next nodes to be traversed
    :param current: current node being traversed
    :return: list of nodes, 2 buttons
    """
    screen.fill((240, 240, 240))
    nodes = []
    bfs_rect, dfs_rect = draw_rest(visited)
    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = nodes_pos[node]
        for n in neighbors:
            x2, y2 = nodes_pos[n]
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)
    # Draw nodes
    for node, (x, y) in nodes_pos.items():
        color = (200, 200, 200)
        if node in visited:
            color = (100, 200, 100)
        elif node in frontier:
            color = (255, 200, 100)
        if node == current:
            color = (255, 100, 100)
        circle = pygame.draw.circle(screen, color, (x, y), 25)
        nodes.append((circle, node))
        text = FONT.render(node, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
    pygame.display.flip()
    return nodes, bfs_rect, dfs_rect


def draw_rest(visited):
    """
    Draws the buttons and the text representation of the traversal
    :param visited: nodes already visited in traversal
    :return: 2 buttons
    """
    bfs_rect = pygame.Rect(0, HEIGHT - 100, WIDTH // 2 - 5, 100)
    pygame.draw.rect(screen, (200, 200, 200), bfs_rect)
    bfs_text = FONT.render("BFS", True, (0, 0, 0))
    bfs_text_rect = bfs_text.get_rect(center=bfs_rect.center)
    screen.blit(bfs_text, bfs_text_rect)

    dfs_rect = pygame.Rect(WIDTH // 2 + 5, HEIGHT - 100, WIDTH // 2 - 5, 100)
    pygame.draw.rect(screen, (200, 200, 200), dfs_rect)
    dfs_text = FONT.render("DFS", True, (0, 0, 0))
    dfs_text_rect = dfs_text.get_rect(center=dfs_rect.center)
    screen.blit(dfs_text, dfs_text_rect)

    traversal = ""
    for item in visited:
        traversal += f'{item} -> '
    traversal = traversal[:-4]

    trav = pygame.Rect(0, HEIGHT - 150, WIDTH, 40)
    pygame.draw.rect(screen, (200, 200, 200), trav)
    trav_text = FONT.render(traversal, True, (0, 0, 0))
    trav_text_rect = trav_text.get_rect(center=trav.center)
    screen.blit(trav_text, trav_text_rect)

    return bfs_rect, dfs_rect


def bfs(start):
    """
    Performs a breadth first search on the graph
    :param start: starting node
    """
    visited = []
    queue = collections.deque([start])
    while queue:
        current = queue.popleft()
        visited.append(current)
        draw_graph(visited=visited, frontier=set(queue), current=current)
        pygame.time.wait(700)
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)


def dfs(start):
    """
    Performs a depth first search on the graph
    :param start: starting node
    """
    visited = []
    stack = [start]
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
            for neighbor in reversed(graph[current]):
                if neighbor not in visited:
                    stack.append(neighbor)
            draw_graph(visited=visited, frontier=set(stack), current=current)
            pygame.time.wait(700)


def main():
    """
    Runs visualiser until user quits
    :return:
    """
    nodes, bfs_rect, dfs_rect = draw_graph()
    pygame.time.wait(1000)
    running = True
    choice = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bfs_rect.collidepoint(event.pos):
                    choice = True
                elif dfs_rect.collidepoint(event.pos):
                    choice = False
                else:
                    for node in nodes:
                        if node[0].collidepoint(event.pos):
                            draw_graph(current=node[1])
                            if choice:
                                bfs(node[1])
                            else:
                                dfs(node[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main()
