import pygame

import pygame_textinput
from pygame_text import text
from types import SimpleNamespace

COLOR_PALETTE = SimpleNamespace()
COLOR_PALETTE.yellow_rgb = (255, 239, 148)
COLOR_PALETTE.pink_rgb = (232, 98, 203)
COLOR_PALETTE.font_style = (232, 98, 203)
COLOR_PALETTE.text_colour = COLOR_PALETTE.pink_rgb
COLOR_PALETTE.background_colour = COLOR_PALETTE.yellow_rgb
pygame.init()

class Player:

    def __init__(self, screen): #, color_PALETTE)"
        self.__name = ''
        self.__calib_min = 0
        self.__calib_max = float('inf')
        # self.__color_palette = color_palette
        self.__color_palette = COLOR_PALETTE
        self.__screen = screen

        self__x_screen, self.__y_screen = self.screen.get_size()

    def __bool__(self):
        return self.name != '' and self.calibrate_values != (0, float('inf'))

    @property
    def name(self):
        return self.__name

    @property
    def calibrate_min(self):
        return self.__calib_min

    @property
    def calibrate_max(self):
        return self.__calib_max
    
    @property
    def calibrate_values(self):
        return self.calibrate_min, self.calibrate_max


    def __get_name(self):

        input_name = pygame_textinput.TextInput(font_family=self.__color_palette.font_style, font_size=self.__y_screen // 13,
                                                text_color=self.__color_palette.text_colour, max_string_length=15)

        clock = pygame.time.Clock()
        is_input = True
        while is_input:

            screen.fill(self.__color_palette.background_colour)
            text("PODAJ SWÓJ NICK:", self.__x_screen // 2, self.__y_screen // 4, font_size=self.__y_screen // 13)

            # TODO exiting
            events = pygame.event.get()
            # for event in events:
            #     if event.type == pygame.QUIT:
            #         self.__kill()

            input_name.update(events)
            text_length = input_name.font_object.size(input_name.get_text())[0]
            self.__screen.blit(input_name.get_surface(),
                               ((self.__x_screen - text_length) // 2, self.__y_screen // 2))

            pygame.display.update()
            clock.tick(30)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__name = input_name.get_text()
                        is_input = False
                        break