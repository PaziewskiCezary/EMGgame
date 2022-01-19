import time
import numpy as np
import pygame

import pygame_textinput
from pygame_text import text
from types import SimpleNamespace
from calibration import Calibration



pygame.init()

NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class Player:

    def __init__(self, screen, use_keyboard, lock, sample_array): #, palette)"
        self.__use_keyboard = use_keyboard

        self.__name = ''
        self.__calibrate_value_min = 0
        self.__calibrate_value_max = float('inf')
        self.__input_type = None
        self.__screen = screen
        self.__lock = lock # TODO decouple this
        self.__sample_array = sample_array # TODO decouple this

        self.__x_screen, self.__y_screen = self.__screen.get_size()

        self.__get_name()
        self.__get_input_type()
        if not self.__use_keyboard:
            Calibration.calibrate

    def __bool__(self):
        return self.name != '' and self.calibrate_values != (0, float('inf')) and self.__input_type is not None

    @property
    def name(self):
        return self.__name

    @property
    def calibrate_value_min(self):
        return self.__calibrate_value_min

    @property
    def calibrate_value_max(self):
        return self.__calibrate_value_max
    
    @property
    def calibrate_values(self):
        return self.calibrate_value_min, self.calibrate_value_max


    @staticmethod
    def __update():
        pygame.display.update()

    def __get_name(self):

        input_name = pygame_textinput.TextInput(font_family=self.__palette.font_style, font_size=self.__y_screen // 13,
                                                text_color=self.__palette.text_colour, max_string_length=15)

        clock = pygame.time.Clock()
        is_input = True
        while is_input:

            self.__screen.fill(self.__palette.background_colour)
            text(self.__screen, self.__palette.text_colour, "PODAJ SWÓJ NICK:", self.__x_screen // 2, self.__y_screen // 4, font_size=self.__y_screen // 13)

            # TODO exiting
            events = pygame.event.get()
            # for event in events:
            #     if event.type == pygame.QUIT:
            #         self.__kill()

            input_name.update(events)
            text_length = input_name.font_object.size(input_name.get_text())[0]
            self.__screen.blit(input_name.get_surface(),
                               ((self.__x_screen - text_length) // 2, self.__y_screen // 2))

            self.__update()
            clock.tick(30)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__name = input_name.get_text()
                        is_input = False
                        break

    def __get_input_type(self):
        return
        raise NotImplemented

    

