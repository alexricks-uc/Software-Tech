import pygame

"""
Visualises a table showing the number of different ways a money value can be 
reached with the given coins
"""

pygame.init()
WIDTH, HEIGHT = 600, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()
cells = {}
obstacles = []
desc = "esc: quit, return: find new combos. Type below"


def draw_table(n, combos, entered="", invalid=False):
    """
    Draws the table alongside a description, an input box and some warning text
    :param n: value which can be found by a certain number of combinations
    :param combos: number of ways any value can be reached
    :param entered: text entered by user
    :param invalid: whether the value is too large to display the full table
    :return: input box
    """
    screen.fill((255, 255, 255))

    desc_rect = pygame.Rect(0, 0, WIDTH, 50)
    pygame.draw.rect(screen, (200, 200, 200), desc_rect)
    desc_text = FONT.render(desc, True, (0, 0, 0))
    desc_text_rect = desc_text.get_rect(center=desc_rect.center)
    screen.blit(desc_text, desc_text_rect)

    input_rect = pygame.Rect(200, 55, WIDTH - 400, 40)
    pygame.draw.rect(screen, (200, 200, 200), input_rect)
    input_text = FONT.render(entered, True, (0, 0, 0))
    input_text_rect = input_text.get_rect(center=input_rect.center)
    screen.blit(input_text, input_text_rect)

    if invalid:
        warning_rect1 = pygame.Rect(0, 100, WIDTH, 50)
        pygame.draw.rect(screen, (200, 200, 200), warning_rect1)
        warning_rect2 = pygame.Rect(0, 150, WIDTH, 50)
        pygame.draw.rect(screen, (200, 200, 200), warning_rect2)
        invalid_text = FONT.render("Please enter a valid integer", True,
                                   (0, 0, 0))
        invalid_text_rect = invalid_text.get_rect(center=warning_rect1.center)
        screen.blit(invalid_text, invalid_text_rect)

    row = 10
    if n == -1:
        big = pygame.Rect(0, 200, WIDTH, 550)
        pygame.draw.rect(screen, (200, 200, 200), big)
        col = 0
    elif n < 50:
        row = n // 5 + 1
        col = 2
    elif n < 100:
        col = 4
    elif n < 150:
        col = 6
    elif n < 200:
        col = 8
    else:
        col = 8
        if not invalid:
            warning_rect1 = pygame.Rect(0, 100, WIDTH, 50)
            pygame.draw.rect(screen, (200, 200, 200), warning_rect1)
            warning_rect2 = pygame.Rect(0, 150, WIDTH, 50)
            pygame.draw.rect(screen, (200, 200, 200), warning_rect2)
            warning = f"This number is too big for this visualiser. You can reach this amount with {combos[-1]} combinations."
            warning_text1 = FONT.render(warning[:43], True, (0, 0, 0))
            warning_text_rect1 = warning_text1.get_rect(
                center=warning_rect1.center)
            screen.blit(warning_text1, warning_text_rect1)
            warning_text2 = FONT.render(warning[43:], True, (0, 0, 0))
            warning_text_rect2 = warning_text2.get_rect(
                center=warning_rect2.center)
            screen.blit(warning_text2, warning_text_rect2)
    for i in range(col):
        for j in range(row):
            rect = pygame.Rect(i * WIDTH // col,
                               200 + j * ((HEIGHT - 200) // row), WIDTH // col,
                               (HEIGHT - 200) // row)
            if i // 2 * 10 + j > len(combos) - 1:
                break
            if i % 2 == 0:
                color = (200, 200, 200)
                num = str(i // 2 * 50 + j * 5)
            else:
                color = "white"
                num = str(combos[i // 2 * 10 + j])
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            text = FONT.render(num, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    pygame.display.flip()
    return input_rect


def get_number_of_ways(n, tender):
    """
    Find number of ways values can be reached
    :param n: maximum value for combinations to be found
    :param tender: different coins that are being used
    :return: maximum value and the combinations that values equal or less than
    the maximum value can be found
    """
    combinations = [0] * ((n + 5) // 5)
    combinations[0] = 1

    for i in range(len(tender)):
        for j in range(0, len(combinations) * 5, 5):
            if tender[i] <= j:
                combinations[j // 5] += combinations[(j // 5) - tender[i] // 5]
    return n, combinations


def main():
    """
    Runs visualiser until the user quits
    """
    tender = [5, 10, 20, 50, 100, 200]  # coins only, given in cents
    n, combos = -1, []
    input_rect = draw_table(n, combos)
    running = True
    textbox = False
    entry = ""
    invalid = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    textbox = True
                else:
                    textbox = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif textbox:
                    if event.key == pygame.K_RETURN:
                        if entry.isnumeric():
                            invalid = False
                            n, combos = get_number_of_ways(int(entry), tender)
                            entry = ""
                        else:
                            entry = ""
                            invalid = True
                            draw_table(n, combos, entry, invalid)
                    elif event.key == pygame.K_BACKSPACE and entry != '':
                        entry = entry[:-1]
                    else:
                        entry += event.unicode
        draw_table(n, combos, entry, invalid)


if __name__ == '__main__':
    main()
