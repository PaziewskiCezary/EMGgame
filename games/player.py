import time
import numpy as np
import pygame

import pygame_textinput
from pygame_text import text
from types import SimpleNamespace

COLOR_PALETTE = SimpleNamespace()
COLOR_PALETTE.yellow_rgb = (255, 239, 148)
COLOR_PALETTE.pink_rgb = (232, 98, 203)
COLOR_PALETTE.font_style = 'DejaVu Sans Mono'
COLOR_PALETTE.text_colour = COLOR_PALETTE.pink_rgb
COLOR_PALETTE.background_colour = COLOR_PALETTE.yellow_rgb

pygame.init()

NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class Player:

    def __init__(self, screen, use_keyboard, lock, sample_array): #, color_PALETTE)"
        self.__use_keyboard = use_keyboard

        self.__name = ''
        self.__calibrate_value_min = 0
        self.__calibrate_value_max = float('inf')
        self.__input_type = None
        # self.__color_palette = color_palette
        self.__color_palette = COLOR_PALETTE
        self.__screen = screen
        self.__lock = lock # TODO decouple this
        self.__sample_array = sample_array # TODO decouple this

        self.__x_screen, self.__y_screen = self.__screen.get_size()

        self.__get_name()
        self.__get_input_type()
        if not self.__use_keyboard:
            self.__calibrate()

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

        input_name = pygame_textinput.TextInput(font_family=self.__color_palette.font_style, font_size=self.__y_screen // 13,
                                                text_color=self.__color_palette.text_colour, max_string_length=15)

        clock = pygame.time.Clock()
        is_input = True
        while is_input:

            self.__screen.fill(self.__color_palette.background_colour)
            text(self.__screen, self.__color_palette.text_colour, "PODAJ SWÓJ NICK:", self.__x_screen // 2, self.__y_screen // 4, font_size=self.__y_screen // 13)

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

    def __calibrate(self):

        text_x_position = self.__x_screen // 2
        text_y_position = self.__y_screen // 2
        font_size = self.__y_screen // 10

        self.__screen.fill(self.__color_palette.background_colour)
        pygame.display.set_caption('Kalibracja')
        self.__update()

        self.__screen.fill(self.__color_palette.background_colour)
        text(self.__screen, self.__color_palette.text_colour, 'KALIBRACJA', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(2)

        self.__screen.fill(self.__color_palette.background_colour)
        text(self.__screen, self.__color_palette.text_colour, 'ROZLUŹNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(1)

        self.__calibrate_value_min = self.__get_calib_samples()

        time.sleep(2)

        self.__screen.fill(self.__color_palette.background_colour)
        text(self.__screen, self.__color_palette.text_colour, 'ZACIŚNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()

        time.sleep(1)

        self.__calibrate_value_max = self.__get_calib_samples()
        self.__check_calib(text_x_position, text_y_position, font_size)
        self.__screen.fill(self.__color_palette.background_colour)
        text(self.__screen, self.__color_palette.text_colour, 'KONIEC KALIBRACJI', text_x_position, text_y_position, font_size=font_size)
        self.__update()

    def __get_calib_samples(self):
        calibration_time = 5
        quit_time = 0.5
        samples = []
        start_time_calibration_min = time.time()

        while time.time() - start_time_calibration_min <= calibration_time:
            self.__lock.acquire()
            signal = self.__sample_array[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
            signal -= np.mean(signal)
            signal = np.abs(signal)
            self.__lock.release()
            samples.append(signal)
            start_quit_time = time.time()
            while time.time() - start_quit_time <= quit_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # self.__kill()
                        pass
                        # return 0
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # self._menu()
                            pass
                            # return 1
        samples_mean = np.mean(samples)
        del samples
        return samples_mean

    def __check_calib(self, text_x_position, text_y_position, font_size):

        minimum_difference_between_calibration_values = 50

        if self.__calibrate_value_min >= self.__calibrate_value_max or \
                self.__calibrate_value_max - self.__calibrate_value_min < minimum_difference_between_calibration_values:
            self.__screen.fill(self.__color_palette.background_colour)
            text(self.__screen, self.__color_palette.text_colour, 'POWTARZAM KALIBRACJĘ', text_x_position, text_y_position,
                 font_size=font_size)
            self.__update()
            time.sleep(2)
            self.__calibrate()

