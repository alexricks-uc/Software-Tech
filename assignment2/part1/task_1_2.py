from collections import deque
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

stack = deque()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20


def draw_stack(counter=0, enq_counter=0):
    screen.fill((50, 50, 50))
    for i, val in enumerate(stack):
        if enq_counter != 0 and i == len(stack) - 1:
            rect = pygame.Rect(START_X,
                               BASE_Y - i * (BLOCK_HEIGHT + 5) + enq_counter,
                               BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = FONT.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            continue
        rect = pygame.Rect(START_X,
                           BASE_Y - i * (BLOCK_HEIGHT + 5) - counter,
                           BLOCK_WIDTH, BLOCK_HEIGHT)
        pygame.draw.rect(screen, (100, 150, 250), rect)

        text = FONT.render(str(val), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    enq_rect = pygame.Rect(2, 2, 196, 100)
    pygame.draw.rect(screen, (100, 150, 250), enq_rect)
    enq_text = FONT.render("Enqueue", True, (0, 0, 0))
    enq_text_rect = enq_text.get_rect(center=enq_rect.center)
    screen.blit(enq_text, enq_text_rect)

    deq_rect = pygame.Rect(enq_rect.right + 2, 2, 196, 100)
    pygame.draw.rect(screen, (100, 150, 250), deq_rect)
    deq_text = FONT.render("Dequeue", True, (0, 0, 0))
    deq_text_rect = deq_text.get_rect(center=deq_rect.center)
    screen.blit(deq_text, deq_text_rect)

    q_rect = pygame.Rect(deq_rect.right + 2, 2, 196, 100)
    pygame.draw.rect(screen, (100, 150, 250), q_rect)
    q_text = FONT.render("Quit", True, (0, 0, 0))
    q_text_rect = q_text.get_rect(center=q_rect.center)
    screen.blit(q_text, q_text_rect)

    return enq_rect, deq_rect, q_rect


def button_clicks(counter, enq_rect, deq_rect, q_rect, anim):
    up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, counter, anim

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if enq_rect.collidepoint(event.pos):
                stack.append(counter)
                counter += 1
                anim = 40
                up = True

            if deq_rect.collidepoint(event.pos) and stack:
                stack.popleft()
                anim = 40

            elif q_rect.collidepoint(event.pos):
                return False, counter, anim

    clock.tick(30)
    for _ in range(400):
        if anim != 0:
            if up:
                draw_stack(0, -anim)
                pygame.display.flip()
                anim -= 0.25
            else:
                draw_stack(anim)
                pygame.display.flip()
                anim -= 0.25
    return True, counter, anim


def main():
    counter = 1
    anim = 40
    running = True

    enq, deq, q = draw_stack()
    while running:
        running, new_counter, new_anim = button_clicks(counter, enq, deq, q,
                                                       anim)
        counter = new_counter
        anim = new_anim

    pygame.quit()


if __name__ == "__main__":
    main()
