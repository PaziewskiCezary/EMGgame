import inspect
import math

import pygame

import emg_games.games as games

from emg_games.gui.components import palette
from emg_games.gui.components.button import Button
from emg_games.backbones import AbstractGame


list_of_games = [obj for name, obj in inspect.getmembers(games, inspect.isclass) if issubclass(obj, AbstractGame)]

print(list_of_games)


def get_game_name(args):
    return list_of_games[args['idx']]


def update():
    pygame.display.update()


def choose_game(screen_properties, kill_game):

    screen_size = screen_properties.screen_size
    x_screen = screen_properties.x_screen
    y_screen = screen_properties.y_screen

    screen = pygame.display.set_mode(screen_size)

    screen.fill(palette.BACKGROUND_COLOUR)

    pygame.display.flip()

    number_of_rows = round(math.sqrt(len(list_of_games)))
    number_of_columns = len(list_of_games) // number_of_rows

    if number_of_rows * number_of_columns < len(list_of_games):
        number_of_columns += 1

    button_width = x_screen / (1.5 * number_of_columns + 0.5)
    button_height = y_screen / (1.5 * number_of_rows + 0.5)
    button_dimension = [button_width, button_height]
    font_style = 'Teko'

    final_font_size = 200

    # make this a function
    for game in list_of_games:
        for font_size in range(final_font_size, 0, -1):
            text_width, _ = pygame.font.SysFont(font_style, font_size).size(game.game_name)
            if text_width < button_width:
                final_font_size = font_size
                break
    game_buttons = []

    for i in range(number_of_rows):
        for j in range(number_of_columns):
            x_position = button_width + j * 1.5 * button_width
            y_position = button_height + i * 1.5 * button_height
            index = i * number_of_columns + j
            if index >= len(list_of_games):
                break
            game_button = Button(screen, list_of_games[index].game_name, [x_position, y_position], button_dimension,
                                 palette.PINK_RGB, palette.YELLOW_RGB, get_game_name,
                                 final_font_size, {'idx':index})
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

