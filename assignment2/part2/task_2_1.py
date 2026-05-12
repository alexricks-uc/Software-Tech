from copy import deepcopy

import pygame
import sys

"""
Visualises linked list operations
"""

pygame.init()
WIDTH, HEIGHT = 1000, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

NODE_RADIUS = 25


class Node:
    """
    Defines a node in a linked list
    """

    def __init__(self, value):
        """
        Initialises a node with value and next node
        :param value:
        """
        self.value = value
        self.next = None


class LinkedList:
    """
    Defines a linked list with insert, delete, reverse and list conversion methods
    """

    def __init__(self):
        """
        Initialises linked list with a head node
        """
        self.head = None

    def insert(self, value, pos):
        """
        Traverses to a given position and inserts node of given value there
        :param value: value of node
        :param pos: position to be inserted
        """
        if not self.head:
            self.head = Node(value)
            return

        current = self.head
        for _ in range(pos):
            current = current.next
        pos += 1
        temp = current.next
        current.next = Node(value)
        current.next.next = temp

    def delete(self, pos):
        """
        Deletes the node at given position by linking predecessor to successor
        :param pos: position of deleted node
        """
        if not self.head:
            return
        current = self.head
        prev = None
        for _ in range(pos):
            prev = current
            current = current.next
        if prev:
            prev.next = current.next
        else:
            self.head = current.next

    def reverse(self):
        """
        Reverses the linked list by adding nodes to a list, popping the end of
        the list, setting it to be the head and then repeatedly popping until
        list is empty and linked list is reversed
        """
        current = self.head
        unconnected = []
        while current:
            temp = deepcopy(current)
            temp.next = None
            unconnected.append(temp)
            current = current.next
        if unconnected:
            new_head = unconnected.pop()
            self.head = new_head
            self.head.next = None
            current = self.head
            while unconnected:
                new = unconnected.pop()
                current.next = new
                current = current.next

    def to_list(self):
        """
        Creates a list of all values in the linked list
        :return: the list of linked list values
        """
        elems = []
        current = self.head

        while current:
            elems.append(current.value)
            current = current.next

        return elems


def draw_node(x, y, value, highlight=False):
    """
    Draws a node
    :param x: x position
    :param y: y position
    :param value: value of node being drawn
    :param highlight: different colour based on whether the node is
    currently selected
    """
    color = (255, 100, 100) if highlight else (100, 200, 250)
    pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)

    text = FONT.render(str(value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def draw_arrow(start_pos, end_pos):
    """
    Draws an arrow between nodes
    :param start_pos: start coordinates
    :param end_pos: end coordinates
    """
    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 3)

    # Draw a simple arrow head
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    angle = pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0))

    arrow_head = [
        (end_pos[0] - 10, end_pos[1] - 5),
        end_pos,
        (end_pos[0] - 10, end_pos[1] + 5),
    ]
    pygame.draw.polygon(screen, (0, 0, 0), arrow_head)


def draw_linked_list(linked_list, y_offset=0,
                     highlight_index=None, entered=''):
    """
    Draws the linked list with entry box and instruction text
    :param linked_list: the linked list object
    :param y_offset: value for offset position of list when animating
    :param highlight_index: index of selected node which will be highlighted
    :param entered: textbox entry
    :return: textbox rect
    """
    screen.fill((240, 240, 240))

    nodes = []
    current = linked_list.head
    x, y = 80, HEIGHT // 2 + y_offset
    idx = 0

    long_text = "return: insert, esc: quit, r: reverse, d: delete, left/right: change selection. Click below to type entry"

    desc_rect = pygame.Rect(0, 0, WIDTH, 40)
    pygame.draw.rect(screen, (200, 200, 200), desc_rect)
    desc_text = FONT.render(long_text, True, (0, 0, 0))
    desc_text_rect = desc_text.get_rect(center=desc_rect.center)
    screen.blit(desc_text, desc_text_rect)

    input_rect = pygame.Rect(WIDTH // 4, HEIGHT - 40, WIDTH // 2, 40)
    pygame.draw.rect(screen, (200, 200, 200), input_rect)
    input_text = FONT.render(entered, True, (0, 0, 0))
    input_text_rect = input_text.get_rect(center=input_rect.center)
    screen.blit(input_text, input_text_rect)

    while current:
        nodes.append((x, y, current.value, idx == highlight_index))
        x += 150
        current = current.next
        idx += 1

    for i, (x, y, val, highlight) in enumerate(nodes):
        draw_node(x, y, val, highlight)

        if i < len(nodes) - 1:
            draw_arrow(
                (x + NODE_RADIUS, y),
                (x + 150 - NODE_RADIUS, y)
            )
    return input_rect


def handle_events():
    """
    Handles program events
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        yield event


def main():
    """
    Runs visualiser until user quits
    """
    ll = LinkedList()
    running = True
    textbox = False
    insert = ''
    initial = 0

    input_rect = draw_linked_list(ll, highlight_index=initial)

    animating = False
    anim_offset = 0
    anim_direction = 1

    while running:
        for event in handle_events():
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
                        if insert != '':
                            ll.insert(insert, initial)
                            insert = ''
                    elif event.key == pygame.K_BACKSPACE and insert != '':
                        insert = insert[:-1]
                    else:
                        insert += event.unicode
                else:
                    if event.key == pygame.K_RIGHT:
                        if initial == len(ll.to_list()) - 1:
                            initial = 0
                        else:
                            initial += 1
                    if event.key == pygame.K_LEFT:
                        if initial == 0:
                            initial = len(ll.to_list()) - 1
                        else:
                            initial -= 1
                    if event.key == pygame.K_d:
                        ll.delete(initial)
                    if event.key == pygame.K_r:
                        animating = True
                        anim_offset = 0
                        anim_direction = 1

        if animating:
            anim_offset += anim_direction * 2
            if anim_offset > 180:
                ll.reverse()
                initial = len(ll.to_list()) - 1 - initial
                anim_direction = -1
            if anim_offset <= 0 and anim_direction == -1:
                animating = False
                anim_offset = 0
        draw_linked_list(ll, anim_offset, initial, insert)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
