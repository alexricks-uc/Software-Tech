import pygame
import sys
from assignment2.part3 import task_3_1

WIDTH, HEIGHT = 800, 700
clock = pygame.time.Clock()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20


def graph_visualization():
    task_3_1.main()


def run(screen):
    font = pygame.font.SysFont(None, 28)

    menu_items = [
        "Graph Visualization (press enter)",
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

                    if choice == "Graph Visualization (press enter)":
                        pygame.display.set_mode((600, 550))
                        graph_visualization()
                        pygame.display.set_mode((WIDTH, HEIGHT))

                    elif choice == "Back":
                        running = False

        clock.tick(30)
