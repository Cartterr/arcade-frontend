import pygame

def draw_text_with_border(screen, font, text, position, text_color, border_color, border_thickness):
    x, y = position
    # Render the border
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx != 0 or dy != 0:  # Avoid the center
                border_surface = font.render(text, True, border_color)
                screen.blit(border_surface, (x + dx, y + dy))
    # Render the text
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, position)


def draw_text(screen, font_large, font_small, infoObject, text_y_offset, visible=True):
    if not visible:
        return
    # Rendering the title with a larger font
    draw_text_with_border(screen, font_large, 'DCCARCADE', 
                          (infoObject.current_w / 2 - font_large.size('DCCARCADE')[0] / 2, 220 + text_y_offset), 
                          pygame.Color('white'), pygame.Color('black'), 5)

    # Positions for "JUEGOS DE ESTUDIANTES" and "JUEGOS NORMALES"
    left_x = infoObject.current_w / 4
    right_x = 3 * infoObject.current_w / 4
    y_positions = infoObject.current_h / 2 + text_y_offset + 180

    # "JUEGOS DE ESTUDIANTES"
    draw_text_with_border(screen, font_small, 'JUEGOS', 
                          (left_x - font_small.size('JUEGOS')[0] / 2 + 230, 30 + y_positions), 
                          pygame.Color('white'), pygame.Color('black'), 4)
    draw_text_with_border(screen, font_small, 'ESTUDIANTES', 
                          (left_x - font_small.size('ESTUDIANTES')[0] / 2 + 230, 30 + y_positions + font_small.get_height()), 
                          pygame.Color('white'), pygame.Color('black'), 4)

    # "JUEGOS NORMALES"
    draw_text_with_border(screen, font_small, 'JUEGOS', 
                          (right_x - font_small.size('JUEGOS')[0] / 2 - 230, 30 + y_positions), 
                          pygame.Color('white'), pygame.Color('black'), 4)
    draw_text_with_border(screen, font_small, 'NORMALES', 
                          (right_x - font_small.size('NORMALES')[0] / 2 - 230, 30 + y_positions + font_small.get_height()), 
                          pygame.Color('white'), pygame.Color('black'), 4)