import pygame

import palette

class Calibration():

	def __init__(self, screen):
		self.__screen = screen
		self.__x_screen, self.__y_screen = self.__screen.get_size()

	def calibrate(self):

        text_x_position = self.__x_screen // 2
        text_y_position = self.__y_screen // 2
        font_size = self.__y_screen // 10

        self.__screen.fill(palette.background_colour)
        pygame.display.set_caption('Kalibracja')
        self.__update()

        self.__screen.fill(palette.background_colour)
        text(self.__screen, palette.text_colour, 'KALIBRACJA', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(2)

        self.__screen.fill(palette.background_colour)
        text(self.__screen, palette.text_colour, 'ROZLUŹNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(1)

        self.__calibrate_value_min = self.__get_calib_samples()

        time.sleep(2)

        self.__screen.fill(palette.background_colour)
        text(self.__screen, palette.text_colour, 'ZACIŚNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()

        time.sleep(1)

        self.__calibrate_value_max = self.__get_calib_samples()
        self.__check_calib(text_x_position, text_y_position, font_size)
        self.__screen.fill(palette.background_colour)
        text(self.__screen, palette.text_colour, 'KONIEC KALIBRACJI', text_x_position, text_y_position, font_size=font_size)
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
            self.__screen.fill(palette.background_colour)
            text(self.__screen, palette.text_colour, 'POWTARZAM KALIBRACJĘ', text_x_position, text_y_position,
                 font_size=font_size)
            self.__update()
            time.sleep(2)
            self.calibrate()
	