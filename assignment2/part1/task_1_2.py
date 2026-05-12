from collections import deque
import pygame

"""
Visualises operations on a queue
"""

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

queue = deque()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20


def draw_queue(counter=0, enq_counter=0):
    """
    Displays the queue with animations for enqueue/dequeue along with buttons
    :param counter: value for next item in queue
    :param enq_counter: value to manipulate position of rectangle when enqueueing
    :return: the three buttons
    """
    screen.fill((50, 50, 50))
    for i, val in enumerate(queue):
        if enq_counter != 0 and i == len(queue) - 1:
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
    """
    Event handler for buttons clicks
    :param counter: current value for next queue item
    :param enq_rect: enqueue button
    :param deq_rect: dequeue button
    :param q_rect: quit button
    :param anim: value for adjusting position of queue rects
    :return: whether the program is still running, value of new queue item and
    animation translation value
    """
    up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, counter, anim

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if enq_rect.collidepoint(event.pos):
                queue.append(counter)
                counter += 1
                anim = 40
                up = True

            if deq_rect.collidepoint(event.pos) and queue:
                queue.popleft()
                anim = 40

            elif q_rect.collidepoint(event.pos):
                return False, counter, anim

    clock.tick(30)
    for _ in range(400):
        if anim != 0:
            if up:
                draw_queue(0, -anim)
                pygame.display.flip()
                anim -= 0.25
            else:
                draw_queue(anim)
                pygame.display.flip()
                anim -= 0.25
    return True, counter, anim


def main():
    """
    Creates display and maintains it until program closed
    """
    counter = 1
    anim = 40
    running = True

    enq, deq, q = draw_queue()
    while running:
        running, new_counter, new_anim = button_clicks(counter, enq, deq, q,
                                                       anim)
        counter = new_counter
        anim = new_anim

    pygame.quit()


if __name__ == "__main__":
    main()
