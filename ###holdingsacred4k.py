import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 160*3, 144*3
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Red 0.1")
CLOCK = pygame.time.Clock()
FPS = 60

# Colors (Game Boy-ish palette)
GB_BG = (155, 188, 15)
GB_DARK = (48, 98, 48)
GB_LIGHT = (139, 172, 15)
WHITE = (255, 255, 255)

# Fonts (approximate Game Boy style)
FONT_TITLE = pygame.font.SysFont("arial", 36, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 20, bold=True)

def draw_main_menu(blink):
    SCREEN.fill(GB_BG)
    
    # Draw Pokémon title
    title_text = FONT_TITLE.render("POKÉMON", True, GB_DARK)
    SCREEN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
    
    # Version text
    version_text = FONT_SMALL.render("RED VERSION", True, GB_DARK)
    SCREEN.blit(version_text, (WIDTH//2 - version_text.get_width()//2, 90))
    
    # PRESS START blinking
    if blink:
        start_text = FONT_SMALL.render("PRESS START", True, GB_DARK)
        SCREEN.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 130))
    
    pygame.display.flip()

def main_menu():
    blink_timer = 0
    blink = True
    while True:
        CLOCK.tick(FPS)
        blink_timer += 1
        if blink_timer >= 30:  # blink every half-second at 60FPS
            blink = not blink
            blink_timer = 0
        
        draw_main_menu(blink)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return  # start game

# Show menu
main_menu()
