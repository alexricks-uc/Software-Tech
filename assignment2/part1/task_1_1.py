import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 600, 290
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
numbers = [5, 3, 9, 1, 7, 4]
cell_width = WIDTH // len(numbers)


def draw_grid(comparisons, found, highlight_index=None, selected=False,
              entered_text=''):
    screen.fill((30, 30, 30))

    for i, num in enumerate(numbers):
        color = (200, 200, 200)
        if i == highlight_index:
            color = (255, 100, 100)
        vis_rect = pygame.Rect(i * cell_width, 0, cell_width - 2, 100)
        pygame.draw.rect(screen, color, vis_rect)
        text = FONT.render(str(num), True, (0, 0, 0))
        text_rect = text.get_rect(center=vis_rect.center)
        screen.blit(text, text_rect)

        comp_rect = pygame.Rect(0, vis_rect.bottom + 2, WIDTH, 48)
        pygame.draw.rect(screen, (200, 200, 200), comp_rect)
        if found == -1:
            finding_text = f"Not found in {comparisons} comparisons!"
            comp_text = FONT.render(finding_text, True,
                                    (0, 0, 0))
            comp_text_rect = comp_text.get_rect(center=comp_rect.center)
            screen.blit(comp_text, comp_text_rect)
        elif found:
            finding_text = f'Found in {comparisons} comparisons!'
        else:
            finding_text = f'Comparisons: {comparisons}'
        comp_text = FONT.render(finding_text, True,
                                (0, 0, 0))
        comp_text_rect = comp_text.get_rect(center=comp_rect.center)
        screen.blit(comp_text, comp_text_rect)

    label_rect_1 = pygame.Rect(0, comp_rect.bottom + 2, WIDTH, 48)
    pygame.draw.rect(screen, (200, 200, 200), label_rect_1)
    label_text_1 = FONT.render(
        "Press 'A' to use the given numbers, or",
        True, (0, 0, 0))
    label_text_rect_1 = label_text_1.get_rect(
        center=label_rect_1.center)
    screen.blit(label_text_1, label_text_rect_1)

    label_rect_2 = pygame.Rect(0, label_rect_1.bottom, WIDTH, 30)
    pygame.draw.rect(screen, (200, 200, 200), label_rect_2)
    label_text_2 = FONT.render(
        "type a number below and press enter",
        True, (0, 0, 0))
    label_text_rect_2 = label_text_2.get_rect(
        center=label_rect_2.center)
    screen.blit(label_text_2, label_text_rect_2)

    input_rect = pygame.Rect(200, label_rect_2.bottom + 10, 200, 38)
    pygame.draw.rect(screen, (200, 200, 200), input_rect)
    input_text = FONT.render(entered_text, True, (0, 0, 0))
    input_text_rect = input_text.get_rect(center=input_rect.center)
    screen.blit(input_text, input_text_rect)
    pygame.display.flip()

    active = False
    number = ''
    while not selected:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return True, 'A'
                elif active:
                    if event.key == pygame.K_RETURN:
                        return True, number
                    elif event.key == pygame.K_BACKSPACE and number != '':
                        number = number[:-1]
                    else:
                        number += event.unicode
                    draw_grid(comparisons, found, highlight_index, True, number)


def linear_search(target, entry=''):
    comparisons = 0
    found = False
    for i, num in enumerate(numbers):
        comparisons += 1
        draw_grid(comparisons, found, i, True, entry)
        pygame.display.flip()
        if num == target:
            found = True
            return comparisons, found, i
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(0.5)
    return comparisons, -1, -1


def main():
    targets = [10, 3, 4]
    selected, number = draw_grid(0, False)
    if number == 'A':
        for target in targets:
            time.sleep(1)
            comps, found, idx = linear_search(target)
            draw_grid(comps, found, idx, selected, '')
    else:
        comps, found, idx = linear_search(int(number), number)
        draw_grid(comps, found, idx, selected, number)
        pygame.display.flip()
    time.sleep(2)
    pygame.quit()


if __name__ == "__main__":
    main()
