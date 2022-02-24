import pygame
import time
import numpy as np

from emg_games.gui.components import palette
from emg_games.gui.components import text

NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class Calibration:

    def __init__(self, screen, amp, kill_game):
        self.__screen = screen
        self.__x_screen, self.__y_screen = self.__screen.get_size()
        self.__amp = amp
        self.kill_game = kill_game

    @staticmethod
    def __update():
        pygame.display.update()

    def calibrate(self, player):
        self.player = player
        text_x_position = self.__x_screen // 2
        text_y_position = self.__y_screen // 2
        font_size = self.__y_screen // 10

        self.__screen.fill(palette.BACKGROUND_COLOR)
        pygame.display.set_caption('Kalibracja')
        self.__update()

        self.__screen.fill(palette.BACKGROUND_COLOR)
        text(self.__screen, palette.TEXT_COLOR, 'KALIBRACJA', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(2)

        self.__screen.fill(palette.BACKGROUND_COLOR)
        text(self.__screen, palette.TEXT_COLOR, 'ROZLUŹNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(1)

        self.__calibrate_value_min = self.__get_calib_samples()
        player._calibrate_value_min = self.__calibrate_value_min
        print("MIN", player._calibrate_value_min)
        time.sleep(2)

        self.__screen.fill(palette.BACKGROUND_COLOR)
        text(self.__screen, palette.TEXT_COLOR, 'ZACIŚNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()

        time.sleep(1)

        self.__calibrate_value_max = self.__get_calib_samples()
        player._calibrate_value_max = self.__calibrate_value_max

        self.__check_calib(text_x_position, text_y_position, font_size)
        self.__screen.fill(palette.BACKGROUND_COLOR)
        text(self.__screen, palette.TEXT_COLOR, 'KONIEC KALIBRACJI', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        self.player = None

    def __get_calib_samples(self):
        calibration_time = 5
        quit_time = 0.5
        samples = []
        start_time_calibration_min = time.time()

        while time.time() - start_time_calibration_min <= calibration_time:
            with self.__amp.lock:
                signal = self.__amp.data[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
            signal -= np.mean(signal)
            signal = np.abs(signal)

            samples.append(signal)
            start_quit_time = time.time()
            while time.time() - start_quit_time <= quit_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.kill_game()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.kill_game()
        samples_mean = np.mean(samples)
        del samples
        return samples_mean

    def __check_calib(self, text_x_position, text_y_position, font_size):

        minimum_difference_between_calibration_values = 50

        if self.__calibrate_value_min >= self.__calibrate_value_max or \
                self.__calibrate_value_max - self.__calibrate_value_min < minimum_difference_between_calibration_values:
            self.__screen.fill(palette.BACKGROUND_COLOR)
            text(self.__screen, palette.TEXT_COLOR, 'POWTARZAM KALIBRACJĘ', text_x_position, text_y_position,
                 font_size=font_size)
            self.__update()
            time.sleep(2)
            self.calibrate(self.player)
