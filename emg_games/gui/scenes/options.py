import pygame

from emg_games.gui.components import palette
from emg_games.gui.components.button import Button


def update():
    pygame.display.update()


def options_screen(screen_properties):
    is_waiting_for_option = True

    screen_properties.screen.fill(palette.BACKGROUND_COLOR)

    x_button = screen_properties.screen.x_screen / 4
    y_button = screen_properties.screen.y_screen / 5
    font_size = int(x_button // 5)

    new_player_button = Button(screen=screen_properties.screen,
                               label='Nowy gracz',
                               pos=(screen_properties.screen.x_screen / 2,
                                    screen_properties.screen.y_scree / 2 - 0.75 * y_button),
                               dims=(x_button, y_button),
                               button_color=palette.PINK_RGB,
                               label_color=palette.YELLOW_RGB,
                               func=lambda x: x,
                               font_size=font_size)

    exit_button = Button(screen=screen_properties.screen,
                         label='Wyjdź',
                         pos=(screen_properties.screen.x_screen / 2,
                              screen_properties.screen.y_scree / 2 - 0.75 * y_button),
                         dims=(x_button, y_button),
                         button_color=palette.PINK_RGB,
                         label_color=palette.YELLOW_RGB,
                         func=lambda x: x,
                         font_size=font_size)

    update()
    while is_waiting_for_option:
        for event in pygame.event.get():
            new_player_button.on_click(event)
            exit_button.on_click(event)
            # if event.type == pygame.QUIT:
            #     kill()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         kill()
