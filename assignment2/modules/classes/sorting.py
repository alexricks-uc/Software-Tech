import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
ARRAY_SIZE = 8
array = [random.randint(10, 350) for _ in range(ARRAY_SIZE)]
unsorted_array = array

bar_width = WIDTH // ARRAY_SIZE


def draw_array(array, color_positions=None, highlight_range=None,
               merge_range=None):
    screen.fill((30, 30, 30))
    bubble, selection, merge = draw_buttons()
    for i, val in enumerate(array):
        color = (100, 200, 250)
        if highlight_range and highlight_range[0] <= i <= highlight_range[1]:
            color = (100, 100, 255)
        if merge_range and merge_range[0] <= i <= merge_range[1]:
            color = (255, 255, 100)
        if color_positions and i in color_positions.get('compare', []):
            color = (255, 100, 100)
        if color_positions and i in color_positions.get('swap', []):
            color = (100, 255, 100)
        pygame.draw.rect(screen, color,
                         (i * bar_width, HEIGHT - val, bar_width - 2, val))
    pygame.display.flip()
    return bubble, selection, merge


def draw_buttons():
    bubble = pygame.Rect(0, 0, WIDTH // 3 - 10, 100)
    pygame.draw.rect(screen, (200, 200, 200), bubble)
    bubble_text = FONT.render("Bubble", True, (0, 0, 0))
    bubble_text_rect = bubble_text.get_rect(center=bubble.center)
    screen.blit(bubble_text, bubble_text_rect)

    selection = pygame.Rect(WIDTH // 3 + 5, 0, WIDTH // 3 - 10, 100)
    pygame.draw.rect(screen, (200, 200, 200), selection)
    selection_text = FONT.render("Selection", True, (0, 0, 0))
    selection_text_rect = selection_text.get_rect(center=selection.center)
    screen.blit(selection_text, selection_text_rect)

    merge = pygame.Rect(2 * WIDTH // 3 + 10, 0, WIDTH // 3 - 10, 100)
    pygame.draw.rect(screen, (200, 200, 200), merge)
    merge_text = FONT.render("Merge", True, (0, 0, 0))
    merge_text_rect = merge_text.get_rect(center=merge.center)
    screen.blit(merge_text, merge_text_rect)

    return bubble, selection, merge


def bubble_sort_visualize(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_array(array, {'compare': [j, j + 1], 'swap': []})
            # pygame.time.wait(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_array(array, {'compare': [], 'swap': [j, j + 1]})
                # pygame.time.wait(50)
    draw_array(array)


def selection_sort_visualize(array):
    n = len(array)
    for i in range(n - 1):
        k = i
        for j in range(i + 1, n):
            draw_array(array, {'compare': [j, k], 'swap': []})
            # pygame.time.wait(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if array[j] < array[k]:
                k = j
        if k != i:
            draw_array(array, {'compare': [], 'swap': [i, k]})
            # pygame.time.wait(100)
            array[i], array[k] = array[k], array[i]
            draw_array(array, {'compare': [], 'swap': [i]})
            # pygame.time.wait(50)
    draw_array(array)


def merge_sort(array, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(array) - 1
    if left < right:
        draw_array(array, highlight_range=(left, right))
        # pygame.time.wait(100)
        mid = (left + right) // 2
        merge_sort(array, left, mid)
        merge_sort(array, mid + 1, right)
        draw_array(array, merge_range=(left, right))
        # pygame.time.wait(100)
        merge_sort_visualize(array, left, mid, right)
        draw_array(array)


def merge_sort_visualize(array, left, mid, right):
    left_array = array[left:mid + 1]
    right_array = array[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_array) and j < len(right_array):
        draw_array(array,
                   {'compare': [left + i, mid + 1 + j], 'swap': []},
                   merge_range=(left, right))
        # pygame.time.wait(50)
        if left_array[i] <= right_array[j]:
            array[k] = left_array[i]
            i += 1
        else:
            array[k] = right_array[j]
            j += 1
        draw_array(array,
                   {'compare': [], 'swap': [k]},
                   merge_range=(left, right))
        # pygame.time.wait(50)
        k += 1
    while i < len(left_array):
        array[k] = left_array[i]
        draw_array(array,
                   {'compare': [], 'swap': [k]},
                   merge_range=(left, right))
        # pygame.time.wait(50)
        i += 1
        k += 1
    while j < len(right_array):
        array[k] = right_array[j]
        draw_array(array,
                   {'compare': [], 'swap': [k]},
                   merge_range=(left, right))
        # pygame.time.wait(50)
        j += 1
        k += 1


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        yield event


def main():
    running = True
    bubble, selection, merge = draw_array(array)
    # pygame.time.wait(1000)
    while running:
        unsorted_array = array.copy()
        for event in handle_events():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bubble.collidepoint(event.pos):
                    bubble_sort_visualize(unsorted_array)
                if selection.collidepoint(event.pos):
                    selection_sort_visualize(unsorted_array)
                if merge.collidepoint(event.pos):
                    merge_sort(unsorted_array)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main()
