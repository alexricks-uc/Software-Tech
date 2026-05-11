import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
heap = []  # min-heap implemented as list


def draw_heap(heap, highlight_indices=[], event="", next=""):
    screen.fill((255, 255, 255))
    if event != "":
        event_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 45)
        pygame.draw.rect(screen, (200, 200, 200), event_rect)
        event_text = FONT.render(event, True, (0, 0, 0))
        event_text_rect = event_text.get_rect(center=event_rect.center)
        screen.blit(event_text, event_text_rect)
    if next != "":
        next_rect = pygame.Rect(0, HEIGHT - 45, WIDTH, 45)
        pygame.draw.rect(screen, (200, 200, 200), next_rect)
        next_text = FONT.render(next, True, (0, 0, 0))
        next_text_rect = next_text.get_rect(center=next_rect.center)
        screen.blit(next_text, next_text_rect)
    if not heap:
        text = FONT.render("Heap is empty", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.flip()
        return
    levels = int(math.log2(len(heap))) + 1
    max_nodes = 2 ** levels - 1
    node_positions = []
    for i in range(len(heap)):
        level = int(math.floor(math.log2(i + 1)))
        index_in_level = i - (2 ** level - 1)
        gap = WIDTH // (2 ** level + 1)
        x = gap * (index_in_level + 1)
        y = 60 + level * 70
        node_positions.append((x, y))
    # Draw edges
    for i in range(len(heap)):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap):
            pygame.draw.line(screen, (0, 0, 0), node_positions[i],
                             node_positions[left], 2)
        if right < len(heap):
            pygame.draw.line(screen, (0, 0, 0), node_positions[i],
                             node_positions[right], 2)
    # Draw nodes
    for i, val in enumerate(heap):
        color = (100, 200, 250)
        if i in highlight_indices:
            color = (255, 100, 100)
        pygame.draw.circle(screen, color, node_positions[i], 20)
        text = FONT.render(str(val), True, (0, 0, 0))
        text_rect = text.get_rect(center=node_positions[i])
        screen.blit(text, text_rect)
    pygame.display.flip()


def get_next_adding_event(heap, index, next_val):
    parent = (index - 1) // 2
    has_parent = True
    if index == 0:
        has_parent = False
    if heap[parent] > heap[index] and has_parent:
        text = f'Next event: Swap {heap[parent]} and {heap[index]}'
    elif next_val:
        text = f'Next event: Inserting {next_val}'
    else:
        text = f'Next event: Removing {heap[0]}'
    return text


def get_next_removing_event(heap, index):
    n = len(heap)
    left = 2 * index + 1
    right = 2 * index + 2
    smallest = index
    if left < n and heap[left] < heap[smallest]:
        smallest = left
    if right < n and heap[right] < heap[smallest]:
        smallest = right
    if smallest != index:
        text = f'Next event: Swapping {heap[index]} and {heap[smallest]}'
    elif index < n:
        text = f'Next event: Removing {heap[0]}'
    else:
        text = f'blah'
    return text


def heapify_up(heap, index, next_val, text, next):
    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] > heap[index]:
            text = f'Swapped {heap[parent]} and {heap[index]}'
            heap[parent], heap[index] = heap[index], heap[parent]
            next = get_next_adding_event(heap, parent, next_val)
            draw_heap(heap, [parent, index], text, next)
            pygame.time.wait(1000)
            index = parent
        else:
            break
    return text, next


def heapify_down(heap, index):
    n = len(heap)
    while True:
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right
        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            text = f'Swapped {heap[index]} and {heap[smallest]}'
            next = get_next_removing_event(heap, smallest)
            draw_heap(heap, [index, smallest], text, next)
            pygame.time.wait(1000)
            index = smallest
        else:
            break


def insert(heap, idx, insertions):
    val = insertions[idx]
    text = f'Inserted {val} to the heap'
    heap.append(val)
    if len(insertions) == idx + 1:
        next_val = None
    else:
        next_val = insertions[idx + 1]
    next = get_next_adding_event(heap, len(heap) - 1, next_val)
    draw_heap(heap, [len(heap) - 1], text, next)
    pygame.time.wait(1000)
    text, next = heapify_up(heap, len(heap) - 1, next_val, text, next)
    return text, next


def extract_min(heap):
    if len(heap) == 0:
        return None
    root = heap[0]
    text = f'Removed {root} from the heap'
    heap[0] = heap[-1]
    heap.pop()
    next = get_next_removing_event(heap, 0)
    if heap:
        draw_heap(heap, [0], text, next)
    else:
        draw_heap(heap, [0])
    pygame.time.wait(1000)
    heapify_down(heap, 0)
    return root


def main():
    running = True
    insertions = [random.randint(1, 100) for _ in range(10)]
    idx = 0
    gap = 0
    text, next = "", ""
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if idx < len(insertions):
            text, next = insert(heap, idx, insertions)
            idx += 1
        else:
            if gap == 0:
                draw_heap(heap, [], text, next)
                pygame.time.wait(1000)
                gap += 1
            if heap:
                extract_min(heap)
            else:
                running = False
        clock.tick(30)
    # pygame.time.wait(2000)
    # pygame.quit()


if __name__ == "__main__":
    main()
