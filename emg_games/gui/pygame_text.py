import pygame

def text(screen, color, caption, x_position, y_position, *,
         font_style='DejaVu Sans Mono', font_size=30, rectangle_color=None):
    """blit generator from text"""

    font = pygame.font.SysFont(font_style, font_size)
    text_render = font.render(caption, True, color)

    text_rect = text_render.get_rect()
    if rectangle_color:
        pygame.draw.rect(screen, rectangle_color, text_rect, True)

    text_rect.center = (x_position, y_position)
    screen.blit(text_render, text_rect)
