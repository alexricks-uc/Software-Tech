import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 6, 6
CELL_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()
cells = {}
obstacles = []
desc = "esc: quit, return: show path. Click to add/remove obstacles"


def draw_grid(dp, obstacles=[], path=None):
    screen.fill((255, 255, 255))
    path_rect = pygame.Rect(0, 0, WIDTH, 50)
    pygame.draw.rect(screen, (200, 200, 200), path_rect)
    path_text = FONT.render(desc, True, (0, 0, 0))
    path_text_rect = path_text.get_rect(center=path_rect.center)
    screen.blit(path_text, path_text_rect)
    found_text = ""
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + 50, CELL_SIZE,
                               CELL_SIZE)
            cells[(r, c)] = rect
            color = (200, 200, 200)
            if (r, c) in obstacles:
                color = (255, 180, 180)
            if path is not None:
                if path:
                    if (r, c) in path:
                        color = (180, 255, 180)
                    found_text = "Path found"
                else:
                    found_text = "No path possible"
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            val = dp[r][c]
            if val is not None:
                text = FONT.render(str(val), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    path_rect = pygame.Rect(0, 650, WIDTH, 50)
    pygame.draw.rect(screen, (200, 200, 200), path_rect)
    path_text = FONT.render(found_text, True, (0, 0, 0))
    path_text_rect = path_text.get_rect(center=path_rect.center)
    screen.blit(path_text, path_text_rect)
    pygame.display.flip()


def count_paths(obstacles=[]):
    dp = [[None] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) in obstacles and not (r == 0 and c == 0):
                dp[r][c] = 0
            elif r == 0 and c == 0 and (r, c) not in obstacles:
                dp[r][c] = 1
            else:
                up = dp[r - 1][c] if r > 0 else 0
                left = dp[r][c - 1] if c > 0 else 0
                dp[r][c] = up + left
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    draw_grid(dp, obstacles)
    return dp


def find_path(dp, obstacles):
    if dp[ROWS - 1][COLS - 1] == 0:
        return []
    r = ROWS - 1
    c = COLS - 1
    p = []
    while (r, c) != (0, 0):
        p.append((r, c))
        if r > 0 and dp[r - 1][c] > 0:
            r -= 1
        elif c > 0 and dp[r][c - 1] > 0:
            c -= 1
    p.append((0, 0))
    p.reverse()
    return p


def main():
    dp = count_paths()
    pygame.time.wait(1000)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    path = find_path(dp, obstacles)
                    draw_grid(dp, obstacles, path)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for coord, rect in cells.items():
                    if rect.collidepoint(event.pos):
                        if coord in obstacles:
                            obstacles.remove(coord)
                        else:
                            obstacles.append(coord)
                        dp = count_paths(obstacles)
        clock.tick(30)


if __name__ == "__main__":
    main()
