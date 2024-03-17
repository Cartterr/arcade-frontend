import pygame

def load_fonts():
    font_path = pygame.font.match_font('Arcade Normal')
    font_large = pygame.font.Font(font_path, 64)
    font_small = pygame.font.Font(font_path, 36)
    return font_large, font_small