import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1050, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

NODE_RADIUS = 20


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        def _insert(node, value):
            if not node:
                return BSTNode(value)
            if value < node.value:
                node.left = _insert(node.left, value)
            elif value > node.value:
                node.right = _insert(node.right, value)
            return node

        self.root = _insert(self.root, value)

    def search(self, value):
        node = self.root
        found = False
        path = []
        while node:
            path.append(node)
            if node.value == value:
                found = True
                break
            elif node.value < value:
                node = node.right
            else:
                node = node.left
        return found, path

    def find_parent(self, value):
        node = self.root
        parent = None
        current_side = "neither"
        while node:
            if node.value == value:
                return parent, current_side
            if node.value < value:
                parent = node
                node = node.right
                current_side = "right"
            if node.value > value:
                parent = node
                node = node.left
                current_side = "left"

    def delete(self, node, successor):
        if node:
            parent, side = self.find_parent(node.value)
            if not node.left and not node.right:
                if not parent:
                    self.root = None
                elif side == "left":
                    parent.left = None
                else:
                    parent.right = None
            elif not node.left:
                if not parent:
                    self.root = self.root.right
                elif side == "left":
                    parent.left = node.right
                else:
                    parent.right = node.right
            elif not node.right:
                if not parent:
                    self.root = self.root.left
                elif side == "left":
                    parent.left = node.left
                else:
                    parent.right = node.left
            else:
                successor_parent, side = self.find_parent(successor.value)
                node.value = successor.value
                if not successor.right:
                    if side == "left":
                        successor_parent.left = None
                    else:
                        successor_parent.right = None
                else:
                    if side == "left":
                        successor_parent.left = successor.right
                    else:
                        successor_parent.right = successor.right

    def highlight_current(self, highlight_idx, inorder_nodes):
        # while highlight_idx < len(inorder_nodes):
        node = inorder_nodes[highlight_idx]
        x, y = WIDTH // 2, 50
        # We need to find node position (roughly)
        # For simplicity, redraw tree and highlight the node:
        nodes_pos = {}

        def store_positions(node, x, y, x_offset,
                            parent_pos=None):
            if node:
                nodes_pos[node] = (x, y)
                store_positions(node.left, x - x_offset, y
                                + 80, x_offset // 2, (x, y))
                store_positions(node.right, x + x_offset, y
                                + 80, x_offset // 2, (x, y))

        store_positions(self.root, WIDTH // 2, 50, 150)
        if node in nodes_pos:
            draw_node(*nodes_pos[node], node.value,
                      highlight=True)
        pygame.display.flip()

    def inorder(self):
        result = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder(self):
        result = []

        def _preorder(node):
            if node:
                result.append(node)
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder(self):
        result = []

        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node)

        _postorder(self.root)
        return result


def draw_node(x, y, value, found=False, highlight=False):
    if highlight:
        if found:
            color = "green3"
        else:
            color = (255, 150, 150)
    else:
        color = (100, 200, 250)
    pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
    text = FONT.render(str(value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def draw_edge(start_pos, end_pos, found=False, highlight=False):
    if highlight:
        if found:
            color = "green3"
        else:
            color = (255, 150, 150)
    else:
        color = (100, 200, 250)
    pygame.draw.line(screen, color, start_pos, end_pos, 3)


def draw_buttons(entered):
    long_text = "s: search, esc: quit, d: delete, left/right: traverse in order, return: insert. Click box to type or press buttons"

    desc = pygame.Rect(0, HEIGHT - 250, WIDTH, 40)
    pygame.draw.rect(screen, (200, 200, 200), desc)
    desc_text = FONT.render(long_text, True, (0, 0, 0))
    desc_text_rect = desc_text.get_rect(center=desc.center)
    screen.blit(desc_text, desc_text_rect)

    input_rect = pygame.Rect(2 * WIDTH // 5, HEIGHT - 200, WIDTH // 5, 90)
    pygame.draw.rect(screen, (200, 200, 200), input_rect)
    input_text = FONT.render(entered, True, (0, 0, 0))
    input_text_rect = input_text.get_rect(center=input_rect.center)
    screen.blit(input_text, input_text_rect)

    inorder = pygame.Rect(0, HEIGHT - 100, WIDTH // 3 - 10, 100)
    pygame.draw.rect(screen, (200, 200, 200), inorder)
    inorder_text = FONT.render("Inorder", True, (0, 0, 0))
    inorder_text_rect = inorder_text.get_rect(center=inorder.center)
    screen.blit(inorder_text, inorder_text_rect)

    preorder = pygame.Rect(WIDTH // 3 + 5, HEIGHT - 100, WIDTH // 3 - 10, 100)
    pygame.draw.rect(screen, (200, 200, 200), preorder)
    preorder_text = FONT.render("Preorder", True, (0, 0, 0))
    preorder_text_rect = preorder_text.get_rect(center=preorder.center)
    screen.blit(preorder_text, preorder_text_rect)

    postorder = pygame.Rect(2 * WIDTH // 3 + 10, HEIGHT - 100, WIDTH // 3 - 10,
                            100)
    pygame.draw.rect(screen, (200, 200, 200), postorder)
    postorder_text = FONT.render("Postorder", True, (0, 0, 0))
    postorder_text_rect = postorder_text.get_rect(center=postorder.center)
    screen.blit(postorder_text, postorder_text_rect)
    return input_rect, inorder, preorder, postorder


def draw_tree(node, x, y, x_offset, nodes_pos, entered, found=False, path=None,
              parent_pos=None, full_redraw=True):
    if full_redraw:
        screen.fill((240, 240, 240))
    input_rect, inorder, preorder, postorder = draw_buttons(entered)
    if node:
        nodes_pos[node] = (x, y)
        if parent_pos:
            if path:
                if found:
                    if node in path:
                        draw_edge(parent_pos, (x, y), True, True)
                    else:
                        draw_edge(parent_pos, (x, y))
                else:
                    if node in path:
                        draw_edge(parent_pos, (x, y), False, True)
                    else:
                        draw_edge(parent_pos, (x, y))
            else:
                draw_edge(parent_pos, (x, y))
            # Draw left subtree
        draw_tree(node.left, x - x_offset, y + 80, x_offset //
                  2, nodes_pos, entered, found, path, (x, y), False)
        # Draw right subtree
        draw_tree(node.right, x + x_offset, y + 80, x_offset //
                  2, nodes_pos, entered, found, path, (x, y), False)
        if path:
            if found:
                if node in path:
                    draw_node(x, y, node.value, True, True)
                else:
                    draw_node(x, y, node.value)
            else:
                if node in path:
                    draw_node(x, y, node.value, False, True)
                else:
                    draw_node(x, y, node.value)
        else:
            draw_node(x, y, node.value)
    return input_rect, inorder, preorder, postorder


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        yield event


def main():
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80, 90, 100]
    for v in values:
        bst.insert(v)
    running = True
    textbox = True
    text_input = ''
    highlight_idx = 0
    nodes = bst.inorder()
    input_field, inorder_button, preorder_button, postorder_button = draw_tree(
        bst.root,
        WIDTH // 2,
        50, 150, {}, text_input)
    while running:
        for event in handle_events():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_tree(bst.root, WIDTH // 2, 50, 150, {}, text_input)
                if input_field.collidepoint(event.pos):
                    textbox = True
                else:
                    textbox = False
                    if inorder_button.collidepoint(event.pos):
                        nodes = bst.inorder()
                        highlight_idx = 0
                        while highlight_idx < len(nodes):
                            bst.highlight_current(highlight_idx, nodes)
                            highlight_idx += 1
                            clock.tick(1)
                        highlight_idx = 0
                    if preorder_button.collidepoint(event.pos):
                        nodes = bst.preorder()
                        highlight_idx = 0
                        while highlight_idx < len(nodes):
                            bst.highlight_current(highlight_idx, nodes)
                            highlight_idx += 1
                            clock.tick(1)
                        highlight_idx = 0
                        nodes = bst.inorder()
                    if postorder_button.collidepoint(event.pos):
                        nodes = bst.postorder()
                        highlight_idx = 0
                        while highlight_idx < len(nodes):
                            bst.highlight_current(highlight_idx, nodes)
                            highlight_idx += 1
                            clock.tick(1)
                        highlight_idx = 0
                        nodes = bst.inorder()
            if event.type == pygame.KEYDOWN:
                draw_tree(bst.root, WIDTH // 2, 50, 150, {}, text_input)
                if textbox:
                    if event.key == pygame.K_RETURN:
                        if text_input.isnumeric():
                            bst.insert(int(text_input))
                            nodes = bst.inorder()
                    elif event.key == pygame.K_BACKSPACE and text_input != '':
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    draw_tree(bst.root, WIDTH // 2, 50, 150, {}, text_input)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    draw_tree(bst.root, WIDTH // 2, 50, 150, {}, text_input)
                    if event.key == pygame.K_s and text_input.isnumeric():
                        found, path = bst.search(int(text_input))
                        draw_tree(bst.root, WIDTH // 2, 50, 150, {}, text_input,
                                  found,
                                  path)
                    if event.key == pygame.K_d:
                        if len(nodes) > 0:
                            deleting_node = nodes[highlight_idx]
                            if highlight_idx == len(nodes) - 1:
                                successor = nodes[0]
                            else:
                                successor = nodes[highlight_idx + 1]
                            bst.delete(deleting_node, successor)
                            highlight_idx = 0
                            nodes = bst.inorder()
                            draw_tree(bst.root, WIDTH // 2, 50, 150, {},
                                      text_input)
                    if event.key == pygame.K_LEFT:
                        if highlight_idx == 0:
                            highlight_idx = len(nodes) - 1
                        else:
                            highlight_idx -= 1
                        if len(nodes) > 0:
                            bst.highlight_current(highlight_idx, nodes)
                    if event.key == pygame.K_RIGHT:
                        if highlight_idx == len(nodes) - 1:
                            highlight_idx = 0
                        else:
                            highlight_idx += 1
                        if len(nodes) > 0:
                            bst.highlight_current(highlight_idx, nodes)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
