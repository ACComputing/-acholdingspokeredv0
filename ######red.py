import pygame
import sys

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 160 * 3, 144 * 3
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AC'S Pokémon Red v0.x[a]")
CLOCK = pygame.time.Clock()
FPS = 60

# --- Colors ---
GB_BG = (155, 188, 15)
GB_DARK = (48, 98, 48)
PATH = (200, 180, 120)
GRASS = (0, 150, 0)
HOUSE = (150, 75, 0)
DOOR = (139, 69, 19)
PLAYER_COLOR = (255, 0, 0)

# --- Fonts ---
FONT_TITLE = pygame.font.SysFont("arial", 24, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 16, bold=True)

# --- Tile size ---
TILE_SIZE = 16
SCALE = 3
TS = TILE_SIZE * SCALE

# --- Example maps dictionary ---
maps = {
    "pallet": {
        "layout": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 2, 0, 2, 0, 0, 1],
            [1, 0, 3, 0, 0, 3, 0, 3, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        "width": 11,
        "height": 8,
        "name": "Pallet Town"
    },
    "route1": {
        "layout": [
            [1] * 11,
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1] * 11,
        ],
        "width": 11,
        "height": 8,
        "name": "Route 1"
    },
}

# --- Player ---
player_map = "pallet"
player_pos = [2, 1]  # row, col

# --- Draw map ---
def draw_map():
    SCREEN.fill(GB_BG)
    layout = maps[player_map]["layout"]
    w, h = maps[player_map]["width"], maps[player_map]["height"]
    offset_x = (WIDTH - w * TS) // 2
    offset_y = (HEIGHT - h * TS) // 2
    for r in range(h):
        for c in range(w):
            tile = layout[r][c]
            color = GRASS
            if tile == 0:
                color = PATH
            elif tile == 2:
                color = HOUSE
            elif tile == 3:
                color = DOOR
            rect = pygame.Rect(offset_x + c * TS, offset_y + r * TS, TS, TS)
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, GB_DARK, rect, 1)
    # Draw player
    px = offset_x + player_pos[1] * TS + TS // 2
    py = offset_y + player_pos[0] * TS + TS // 2
    pygame.draw.circle(SCREEN, PLAYER_COLOR, (px, py), TS // 3)
    # Map name
    t = FONT_TITLE.render(maps[player_map]["name"], True, GB_DARK)
    SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, 10))
    pygame.display.flip()

# --- Main menu ---
def main_menu():
    blink = True
    timer = 0
    while True:
        CLOCK.tick(FPS)
        timer += 1
        if timer >= 30:
            blink = not blink
            timer = 0
        SCREEN.fill(GB_BG)
        t1 = FONT_TITLE.render("AC'S POKÉMON RED", True, GB_DARK)
        SCREEN.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 50))
        t2 = FONT_SMALL.render("v0.x[a]", True, GB_DARK)
        SCREEN.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 90))
        if blink:
            t3 = FONT_SMALL.render("PRESS START", True, GB_DARK)
            SCREEN.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 130))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return

# --- Game loop ---
def game_loop():
    global player_map, player_pos
    while True:
        CLOCK.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                r, c = player_pos
                layout = maps[player_map]["layout"]
                # Movement (prevent colliding with house/door)
                if e.key == pygame.K_UP and r > 0 and layout[r - 1][c] not in (2, 3):
                    player_pos[0] -= 1
                if e.key == pygame.K_DOWN and r < len(layout) - 1 and layout[r + 1][c] not in (2, 3):
                    player_pos[0] += 1
                if e.key == pygame.K_LEFT and c > 0 and layout[r][c - 1] not in (2, 3):
                    player_pos[1] -= 1
                if e.key == pygame.K_RIGHT and c < len(layout[0]) - 1 and layout[r][c + 1] not in (2, 3):
                    player_pos[1] += 1
                # Map transitions (fixed: compare individual coordinates)
                if player_map == "pallet" and player_pos[0] == 6 and player_pos[1] == 10:
                    player_map = "route1"
                    player_pos = [1, 1]
        draw_map()

# --- Intro ---
def intro_sequence():
    for t in ["GAME FREAK", "AC HOLDINGS", "NINTENDO"]:
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 1500:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            SCREEN.fill(GB_BG)
            r = FONT_TITLE.render(t, True, GB_DARK)
            SCREEN.blit(r, (WIDTH // 2 - r.get_width() // 2, HEIGHT // 2 - r.get_height() // 2))
            pygame.display.flip()
            CLOCK.tick(FPS)

# --- Run ---
if __name__ == "__main__":
    intro_sequence()
    main_menu()
    game_loop()
