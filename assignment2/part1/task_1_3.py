import pygame

from assignment2.part1.modules.my_queue import Queue

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

new_queue = Queue(100)

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20


def draw_queue(font, counter=0, enq_counter=0):
    screen.fill((50, 50, 50))
    j = 0

    for i, val in enumerate(new_queue.q):
        if not val:
            j += 1
        else:
            if enq_counter != 0 and (i - j) == new_queue.nItems - 1:
                rect = pygame.Rect(START_X,
                                   BASE_Y - (i - j) * (
                                           BLOCK_HEIGHT + 5) + enq_counter,
                                   BLOCK_WIDTH, BLOCK_HEIGHT)
                pygame.draw.rect(screen, (100, 150, 250), rect)

                text = FONT.render(str(val), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                continue
            rect = pygame.Rect(START_X,
                               BASE_Y - (i - j) * (BLOCK_HEIGHT + 5) - counter,
                               BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = FONT.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    info_text = font.render(
        "SPACE: Enqueue, BACKSPACE: Dequeue, ESC: Return to menu",
        True,
        (200, 200, 200)
    )
    screen.blit(info_text, (10, 10))


def keyboard_clicks(counter, anim, font):
    up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, counter, anim

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_queue.insert(counter)
                counter += 1
                anim = 100
                up = True

            if event.key == pygame.K_BACKSPACE and new_queue:
                new_queue.remove()
                anim = 40

            elif event.key == pygame.K_ESCAPE:
                return False, counter, anim

    clock.tick(30)
    for _ in range(400):
        if anim != 0:
            if up:
                draw_queue(font, 0, -anim)
                pygame.display.flip()
                anim -= 0.25
            else:
                draw_queue(font, anim)
                pygame.display.flip()
                anim -= 0.25
    return True, counter, anim


def main(font):
    counter = 1
    anim = 40
    running = True
    draw_queue(font)
    while running:
        running, new_counter, new_anim = keyboard_clicks(counter, anim, font)
        counter = new_counter
        anim = new_anim


if __name__ == "__main__":
    main(FONT)
