import pygame

def animate_elements(y_offset):
    # This function calculates new positions based on a sine wave for smooth oscillation
    import math
    period = 120*35  # Number of frames for one complete animation cycle
    amplitude = 10  # Vertical movement range (pixels)
    
    # Calculate vertical offset
    vertical_offset = math.sin(pygame.time.get_ticks() / (period / 2) * math.pi) * amplitude
    
    return y_offset + vertical_offset



