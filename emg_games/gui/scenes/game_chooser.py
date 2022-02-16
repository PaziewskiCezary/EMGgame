import inspect
import math

import pygame
import emg_games.games

from emg_games.gui.components import palette
from emg_games.gui.components.button import Button
import emg_games.backbones


def update():
    pygame.display.update()


def _calc_font_size(list_of_games, width):
    '''finds best fitting font size'''
    width = int(width)
    max_font_size = 200
    font = pygame.font.SysFont(palette.FONT_STYLE, max_font_size)
    names = [game.game_name for game in list_of_games]
    widths = [font.size(name)[0] for name in names]
    longest_name_idx = max(range(len(widths)), key=widths.__getitem__)
    longest_name = names[longest_name_idx]

    for font_size in range(max_font_size, 0, -1):
        text_width, _ = pygame.font.SysFont(palette.FONT_STYLE, font_size).size(longest_name)
        if text_width < width:
            return font_size


def choose_game(screen_properties, kill_game):
    list_of_games = [obj for name, obj in inspect.getmembers(emg_games.games, inspect.isclass) if
                     issubclass(obj, emg_games.backbones.AbstractGame)]

    screen_size = screen_properties.screen_size
    x_screen = screen_properties.x_screen
    y_screen = screen_properties.y_screen

    screen = pygame.display.set_mode(screen_size)

    screen.fill(palette.BACKGROUND_COLOUR)

    number_of_rows = round(math.sqrt(len(list_of_games)))
    number_of_columns = math.ceil(len(list_of_games) / number_of_rows)

    button_width = x_screen / (1.5 * number_of_columns + 0.5)
    button_height = y_screen / (1.5 * number_of_rows + 0.5)
    button_dimension = [button_width, button_height]

    width = button_width * 0.9
    font_size = _calc_font_size(list_of_games, width)

    # place buttons
    game_buttons = []
    for index, game in enumerate(list_of_games):
        i, j = index // number_of_columns, index % number_of_columns
        x_position = button_width + j * 1.5 * button_width
        y_position = button_height + i * 1.5 * button_height

        game_name = list_of_games[index].game_name
        game_button = Button(screen, game_name, (x_position, y_position), button_dimension,
                             palette.PINK_RGB, palette.YELLOW_RGB, lambda idx=index: game_name,
                             font_size)
        game_buttons.append(game_button)

    update()

    while True:
        for event in pygame.event.get():
            for idx, game_button in enumerate(game_buttons):
                game_button.on_click(event)
                if game_button.pressed:
                    return list_of_games[idx]

            if event.type == pygame.QUIT:
                kill_game()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         self._menu()
