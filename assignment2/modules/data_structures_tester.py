import pygame
import sys
from assignment2.modules.visualisers import puzzles_visualiser, \
    data_structures_visualiser, heap_visualiser, graph_visualiser, \
    sorting_visualiser

pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Explorer")

FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)


def main_menu():
    screen.fill((200, 200, 250))
    draw_text("Algorithm Explorer", (WIDTH // 3, 50))

    buttons = {
        'Data Structures': pygame.Rect(300, 150, 200, 50),
        'Sorting': pygame.Rect(300, 230, 200, 50),
        'Graphs': pygame.Rect(300, 310, 200, 50),
        'Heap': pygame.Rect(300, 390, 200, 50),
        'Puzzles': pygame.Rect(300, 470, 200, 50),
        'Exit': pygame.Rect(300, 550, 200, 50),
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 20, rect.y + 10))

    pygame.display.flip()
    return buttons


def main():
    running = True
    current_module = None

    while running:
        if current_module is None:
            buttons = main_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    for name, rect in buttons.items():
                        if rect.collidepoint(pos):
                            if name == "Exit":
                                running = False

                            if name == "Data Structures":
                                current_module = name

                            if name == "Sorting":
                                current_module = name

                            if name == "Graphs":
                                current_module = name

                            if name == "Heap":
                                current_module = name

                            if name == "Puzzles":
                                current_module = name
        else:
            try:
                if current_module == "Data Structures":
                    data_structures_visualiser.run(screen)
                elif current_module == "Sorting":
                    sorting_visualiser.run(screen)
                elif current_module == "Graphs":
                    graph_visualiser.run(screen)
                elif current_module == "Heap":
                    heap_visualiser.run(screen)
                elif current_module == "Puzzles":
                    puzzles_visualiser.run(screen)

            except SystemExit:
                running = False
                break

            finally:
                current_module = None

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

# questions: how much commenting is required?
# is my implementation of the heap visualiser legitimate?
# do i need to implement testing of tasks without classes (eg. sorting)
