import pygame
import sys
from assignment2.part2 import task_2_3

"""
Menu screen for sorting visualiser
"""

WIDTH, HEIGHT = 800, 700
clock = pygame.time.Clock()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20


def sorting_visualisation():
    """
    Calls main of task_2_3
    """
    task_2_3.main()


def run(screen):
    """
    Calls main of task_2
    :param screen: pygame window
    """
    font = pygame.font.SysFont(None, 28)

    menu_items = [
        "Sorting Visualization (press enter)",
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

                    if choice == "Sorting Visualization (press enter)":
                        pygame.display.set_mode((600, 500))
                        sorting_visualisation()
                        pygame.display.set_mode((WIDTH, HEIGHT))

                    elif choice == "Back":
                        running = False

        clock.tick(30)
