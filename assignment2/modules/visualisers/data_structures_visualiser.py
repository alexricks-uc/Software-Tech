import pygame
import sys
from assignment2.modules.classes.stack import Stack
from assignment2.part1 import task_1_3
from assignment2.part2 import task_2_1
from assignment2.part2 import task_2_2

WIDTH, HEIGHT = 800, 700
clock = pygame.time.Clock()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20


def stack_visualization(screen, font):
    stack = Stack()
    counter = 1
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stack.push(counter)
                    counter += 1

                elif event.key == pygame.K_BACKSPACE and not stack.is_empty():
                    stack.pop()

                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((50, 50, 50))

        for i, val in enumerate(stack._data):
            rect = pygame.Rect(
                START_X,
                BASE_Y - i * (BLOCK_HEIGHT + 5),
                BLOCK_WIDTH,
                BLOCK_HEIGHT
            )
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        info_text = font.render(
            "SPACE: Push, BACKSPACE: Pop, ESC: Return to menu",
            True,
            (200, 200, 200)
        )
        screen.blit(info_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)


def queue_visualization(font):
    task_1_3.main(font)


def linked_list_visualisation():
    task_2_1.main()


def bst_visualisation():
    task_2_2.main()


def run(screen):
    font = pygame.font.SysFont(None, 28)

    menu_items = [
        "Stack Visualization (press enter)",
        "Queue Visualization (press enter)",
        "Linked List Visualization (press enter)",
        "BST Visualization (press enter)",
        "Back"
    ]

    selected = 0
    running = True

    while running:
        screen.fill((220, 220, 220))

        for i, item in enumerate(menu_items):
            color = (255, 0, 0) if i == selected else (0, 0, 0)
            text = font.render(item, True, color)
            screen.blit(text, (100, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)

                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)

                elif event.key == pygame.K_RETURN:
                    choice = menu_items[selected]

                    if choice == "Stack Visualization (press enter)":
                        stack_visualization(screen, font)

                    if choice == "Queue Visualization (press enter)":
                        pygame.display.set_mode((800, 600))
                        queue_visualization(font)
                        pygame.display.set_mode((WIDTH, HEIGHT))

                    if choice == "Linked List Visualization (press enter)":
                        pygame.display.set_mode((1000, 300))
                        linked_list_visualisation()
                        pygame.display.set_mode((WIDTH, HEIGHT))

                    if choice == "BST Visualization (press enter)":
                        pygame.display.set_mode((1050, 750))
                        bst_visualisation()
                        pygame.display.set_mode((WIDTH, HEIGHT))

                    elif choice == "Back":
                        running = False

        clock.tick(30)
