import pygame
import sys
import math

# =============================================================================
# AC'S POKÉMON ! RED 0.1 BETA - GAMEBOY ACCURATE GRAPHICS (Pallet Town Exact Palette)
# =============================================================================

pygame.init()
GB_WIDTH, GB_HEIGHT = 160, 144
WIDTH, HEIGHT = GB_WIDTH * 3, GB_HEIGHT * 3
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AC'S Pokémon ! Red 0.1 BETA")
CLOCK = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Pokémon Red/Blue Palette Town Colors ---
COLORS = {
    'bg': (155, 188, 15),         # background green
    'grass_dark': (48, 98, 48),   # dark grass
    'grass_light': (139, 172, 15),# light grass
    'path': (170, 215, 81),       # path/dirt
    'wall': (155, 188, 15),       # building walls
    'door': (202, 202, 114),      # doors
    'roof_dark': (91, 65, 37),    # roof shadow
    'roof_light': (139, 90, 43),  # roof highlight
    'window': (30, 58, 138),      # window
    'player': (255, 153, 0),      # hat
    'player_body': (224, 160, 80),# body
    'player_shadow': (0, 0, 0),   # outline/shadow
}

gb_surface = pygame.Surface((GB_WIDTH, GB_HEIGHT))
TILE_SIZE = 8
TILE_GRASS, TILE_PATH, TILE_WALL, TILE_DOOR, TILE_ROOF, TILE_WINDOW = range(6)
MAP_TILES_X, MAP_TILES_Y = 40, 36

# --- Pallet Town Map Layout ---
town_map = [[TILE_GRASS for _ in range(MAP_TILES_X)] for _ in range(MAP_TILES_Y)]
for y in range(MAP_TILES_Y):
    town_map[y][0] = town_map[y][MAP_TILES_X-1] = TILE_WALL
for x in range(MAP_TILES_X):
    town_map[0][x] = town_map[MAP_TILES_Y-1][x] = TILE_WALL

# Oak's Lab
for y in range(5, 12):
    for x in range(15, 25):
        town_map[y][x] = TILE_ROOF if y in [5,6] else TILE_WALL
town_map[8][20] = TILE_DOOR

# Player's house
for y in range(20, 28):
    for x in range(5, 13):
        town_map[y][x] = TILE_ROOF if y==20 else TILE_WALL
town_map[23][8] = TILE_DOOR

# Rival's house
for y in range(20, 28):
    for x in range(28, 36):
        town_map[y][x] = TILE_ROOF if y==20 else TILE_WALL
town_map[23][31] = TILE_DOOR

# Paths
for x in range(15, 25): town_map[14][x] = TILE_PATH
for y in range(14, 25): town_map[y][20] = TILE_PATH
for x in range(5, 13): town_map[25][x] = TILE_PATH
for x in range(28, 36): town_map[25][x] = TILE_PATH

# --- Tile Drawing Functions ---
def draw_tile_grass(surf, x, y):
    for py in range(8):
        for px in range(8):
            surf.set_at((x+px, y+py), COLORS['grass_dark'] if (px+py)%3==0 else COLORS['grass_light'])
def draw_tile_path(surf, x, y):
    for py in range(8):
        for px in range(8):
            surf.set_at((x+px, y+py), COLORS['grass_dark'] if px%2==0 and py%2==0 else COLORS['path'])
def draw_tile_wall(surf, x, y):
    for py in range(8):
        for px in range(8):
            surf.set_at((x+px, y+py), COLORS['wall'] if py%3==0 or (py%3==1 and px%2==0) else COLORS['door'])
def draw_tile_door(surf, x, y):
    for py in range(8):
        for px in range(8):
            surf.set_at((x+px, y+py), COLORS['door'] if 2<=px<=5 and 2<=py<=6 else COLORS['wall'])
    surf.set_at((x+5, y+4), COLORS['bg'])
def draw_tile_roof(surf, x, y):
    for py in range(8):
        for px in range(8):
            surf.set_at((x+px, y+py), COLORS['roof_dark'] if (px+py)%3==0 else COLORS['roof_light'])
def draw_tile_window(surf, x, y):
    for py in range(8):
        for px in range(8):
            surf.set_at((x+px, y+py), COLORS['window'] if 2<=px<=5 and 2<=py<=5 else COLORS['wall'])
    for i in range(2,6):
        surf.set_at((x+4, y+i), COLORS['bg'])
        surf.set_at((x+i, y+4), COLORS['bg'])

tile_drawers = {
    TILE_GRASS: draw_tile_grass,
    TILE_PATH: draw_tile_path,
    TILE_WALL: draw_tile_wall,
    TILE_DOOR: draw_tile_door,
    TILE_ROOF: draw_tile_roof,
    TILE_WINDOW: draw_tile_window,
}

def draw_map_at(surf, cam_x, cam_y):
    start_tile_x, start_tile_y = cam_x//TILE_SIZE, cam_y//TILE_SIZE
    end_tile_x, end_tile_y = (cam_x+GB_WIDTH)//TILE_SIZE+1, (cam_y+GB_HEIGHT)//TILE_SIZE+1
    for ty in range(start_tile_y, end_tile_y):
        for tx in range(start_tile_x, end_tile_x):
            if 0<=tx<MAP_TILES_X and 0<=ty<MAP_TILES_Y:
                screen_x, screen_y = tx*TILE_SIZE - cam_x, ty*TILE_SIZE - cam_y
                tile_drawers.get(town_map[ty][tx], lambda s,x,y: pygame.draw.rect(s,COLORS['bg'],(x,y,TILE_SIZE,TILE_SIZE)))(surf, screen_x, screen_y)

# --- Player ---
player_x, player_y = 8*TILE_SIZE+4, 22*TILE_SIZE+4
player_speed = 1
def draw_player(surf, x, y):
    for py in range(8):
        for px in range(8):
            if py<2: surf.set_at((x+px, y+py), COLORS['player'] if px in [2,3,4,5] else COLORS['player_body'])
            elif py<5: surf.set_at((x+px, y+py), COLORS['player_body'] if px in [2,3,4,5] else COLORS['player_shadow'])
            else: surf.set_at((x+px, y+py), COLORS['player_body'] if px in [2,3,4,5] else COLORS['player_shadow'])
def check_collision(rect, dx, dy):
    test_rect = rect.move(dx, dy)
    left_tile, right_tile = test_rect.left//TILE_SIZE, (test_rect.right-1)//TILE_SIZE
    top_tile, bottom_tile = test_rect.top//TILE_SIZE, (test_rect.bottom-1)//TILE_SIZE
    for ty in range(top_tile, bottom_tile+1):
        for tx in range(left_tile, right_tile+1):
            if 0<=tx<MAP_TILES_X and 0<=ty<MAP_TILES_Y and town_map[ty][tx] in (TILE_WALL,TILE_ROOF,TILE_WINDOW):
                return True
    return False

# --- Fonts ---
FONT_LARGE = pygame.font.SysFont("arial", 32, bold=True)
FONT_MEDIUM = pygame.font.SysFont("arial", 24, bold=True)

def fade_text(text, font, color, y_pos, duration=1.0):
    surf = font.render(text, True, color)
    surf.set_alpha(0)
    alpha, fade_out = 0, False
    fade_speed = 255/(duration*FPS/2)
    while True:
        SCREEN.fill(BLACK)
        SCREEN.blit(surf, (WIDTH//2 - surf.get_width()//2, y_pos))
        pygame.display.flip()
        if not fade_out:
            alpha += fade_speed
            if alpha >= 255: alpha, fade_out = 255, True; pygame.time.delay(400)
        else:
            alpha -= fade_speed
            if alpha<=0: break
        surf.set_alpha(int(alpha))
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
        CLOCK.tick(FPS)

def gengar_fight_animation():
    gengar_rect = pygame.Rect(WIDTH//2-40, HEIGHT//2-40, 80, 80)
    player_rect = pygame.Rect(50, HEIGHT-100, 40, 40)
    dx, attack_phase = 5, True
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks()-start_ticks<3000:
        SCREEN.fill(BLACK)
        gengar_rect.y = HEIGHT//2 + int(20*math.sin(pygame.time.get_ticks()/150))
        pygame.draw.ellipse(SCREEN, (103, 58, 183), gengar_rect)
        if attack_phase: player_rect.x += dx; attack_phase=False if player_rect.x>WIDTH//2-20 else True
        else: player_rect.x -= dx
        pygame.draw.rect(SCREEN, (255,153,0), player_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
        CLOCK.tick(FPS)

def main_menu():
    menu_items, selected = ["START GAME", "OPTIONS", "QUIT"], 0
    while True:
        SCREEN.fill(BLACK)
        title_surf = FONT_LARGE.render("AC'S POKÉMON ! RED", True, WHITE)
        SCREEN.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))
        for i, item in enumerate(menu_items):
            color = WHITE if i==selected else (150,150,150)
            surf = FONT_MEDIUM.render(item, True, color)
            SCREEN.blit(surf, (WIDTH//2 - surf.get_width()//2, 200+i*40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_DOWN: selected=(selected+1)%len(menu_items)
                elif event.key==pygame.K_UP: selected=(selected-1)%len(menu_items)
                elif event.key==pygame.K_RETURN:
                    if menu_items[selected]=="START GAME": return
                    elif menu_items[selected]=="QUIT": pygame.quit(); sys.exit()
        CLOCK.tick(FPS)

# --- Intro and Menu ---
fade_text("GAME FREAK PRESENTS", FONT_LARGE, WHITE, HEIGHT//2-40)
fade_text("AC HOLDING PRESENTS", FONT_LARGE, WHITE, HEIGHT//2-40)
fade_text("NINTENDO PRESENTS", FONT_LARGE, WHITE, HEIGHT//2-40)
gengar_fight_animation()
main_menu()

# --- Camera ---
camera_x = max(0, min(player_x - GB_WIDTH//2 + 4, MAP_TILES_X*TILE_SIZE - GB_WIDTH))
camera_y = max(0, min(player_y - GB_HEIGHT//2 + 4, MAP_TILES_Y*TILE_SIZE - GB_HEIGHT))

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False

    keys = pygame.key.get_pressed()
    dx = (-player_speed if keys[pygame.K_LEFT] else player_speed if keys[pygame.K_RIGHT] else 0)
    dy = (-player_speed if keys[pygame.K_UP] else player_speed if keys[pygame.K_DOWN] else 0)

    player_rect = pygame.Rect(player_x, player_y, 8, 8)
    if dx != 0 and not check_collision(player_rect, dx, 0): player_x += dx
    if dy != 0 and not check_collision(player_rect, 0, dy): player_y += dy

    player_x = max(0, min(player_x, MAP_TILES_X*TILE_SIZE - 8))
    player_y = max(0, min(player_y, MAP_TILES_Y*TILE_SIZE - 8))

    camera_x = max(0, min(player_x - GB_WIDTH//2 + 4, MAP_TILES_X*TILE_SIZE - GB_WIDTH))
    camera_y = max(0, min(player_y - GB_HEIGHT//2 + 4, MAP_TILES_Y*TILE_SIZE - GB_HEIGHT))

    gb_surface.fill(COLORS['bg'])
    draw_map_at(gb_surface, camera_x, camera_y)
    draw_player(gb_surface, player_x - camera_x, player_y - camera_y)
    scaled_surface = pygame.transform.scale(gb_surface, (WIDTH, HEIGHT))
    SCREEN.blit(scaled_surface, (0,0))
    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
sys.exit()
