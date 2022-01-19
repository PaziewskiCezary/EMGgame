from button import Button
import color_palette
from screen_properties import ScreenProperties

import pygame
import math

full_screen = False
pygame.init()

screen_properties = ScreenProperties(full_screen)

screen_size = screen_properties.screen_size
x_screen = screen_properties.x_screen
y_screen = screen_properties.y_screen

screen = pygame.display.set_mode(screen_size)

screen.fill(color_palette.BACKGROUND_COLOUR)

pygame.display.flip()

list_of_games = ["ŚMIECI", "FIGURY", "KOLORY", "WODA", "ADA", "MARTYNA", "CEZARY", "ŻÓŁW", "DELFIN", "KOT",
                 "ALA MA KOTA"]


def kill(self):
    self.__queue.put(1)
    pygame.quit()
    exit()


def get_game_name(index):
    print(list_of_games[index])


def update():
    pygame.display.update()


number_of_rows = round(math.sqrt(len(list_of_games)))
number_of_columns = len(list_of_games) // number_of_rows

if number_of_rows * number_of_columns < len(list_of_games):
    number_of_columns += 1

button_width = x_screen / (1.5 * number_of_columns + 0.5)
button_height = y_screen / (1.5 * number_of_rows + 0.5)
button_dimension = [button_width, button_height]
font_style = 'Teko'

final_font_size = 200

for game in list_of_games:
    for font_size in range(final_font_size, 0, -1):
        text_width, _ = pygame.font.SysFont(font_style, font_size).size(game)
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
        game_button = Button(screen, list_of_games[index], [x_position, y_position], button_dimension,
                             color_palette.PINK_RGB, color_palette.YELLOW_RGB, lambda idx=index: get_game_name(idx),
                             final_font_size)
        game_buttons.append(game_button)
update()

while True:
    for event in pygame.event.get():
        for game_button in game_buttons:
            game_button.on_click(event)
        if event.type == pygame.QUIT:
            kill()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         self._menu()

