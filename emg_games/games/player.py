import pygame

from emg_games.gui.components.pygame_textinput import TextInput
from emg_games.gui.components.pygame_text import text
#from emg_games.games.calibration import Calibration
from emg_games.gui.components import palette
from emg_games.gui.components.button import Button

pygame.init()

NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class Player:

    def __init__(self, screen_properties, use_keyboard, lock, sample_array):

        self.__use_keyboard = use_keyboard

        self.__name = ''
        self.__calibrate_value_min = 0
        self.__calibrate_value_max = float('inf')
        self.__input_type = None

        self.__screen_properties = screen_properties
        self.__screen = self.__screen_properties.screen
        self.__lock = lock # TODO decouple this
        self.__sample_array = sample_array # TODO decouple this


        self.__x_screen, self.__y_screen = self.__screen.get_size()

        self.__get_name()
        self.__get_input_type()
        print(2132312)
        if not self.__use_keyboard:
            calibrate = Calibration(self.__screen)
            calibrate.calibrate()

    def __bool__(self):
        return self.name != '' and self.calibrate_values != (0, float('inf')) and self.__input_type is not None

    def kill(self):
        self.__queue.put(1)
        pygame.quit()
        exit()

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
        print('starting get name')
        input_name = TextInput(font_family=palette.FONT_STYLE, font_size=self.__y_screen // 13,
                               text_color=palette.TEXT_COLOUR, max_string_length=15)

        clock = pygame.time.Clock()
        is_input = True
        while is_input:

            self.__screen.fill(palette.BACKGROUND_COLOUR)
            text(self.__screen, palette.TEXT_COLOUR, "PODAJ SWÓJ NICK:", self.__x_screen // 2, self.__y_screen // 4,
                 font_size=self.__y_screen // 13)

            # TODO exiting
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.__kill()

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

    def __use_keyboard_true(self):
        self.__use_keyboard = True
        self._is_waiting_for_option = False

    def __use_keyboard_false(self):
        self.__use_keyboard = False
        self._is_waiting_for_option = False

    def __get_input_type(self):

        print('start input type')
        self._is_waiting_for_option = True

        self.__screen.fill(palette.BACKGROUND_COLOUR)

        x_button = self.__x_screen / 4
        y_button = self.__y_screen / 5
        font_size = int(x_button // 5)


        muscle_button = Button(self.__screen, 'Mięsień', (self.__x_screen / 2, self.__y_screen / 2 - 0.75 * y_button),
                               (x_button, y_button), palette.PINK_RGB, palette.YELLOW_RGB, self.__use_keyboard_false,
                               font_size=font_size)
        keyboard_button = Button(self.__screen, 'Klawiatura', (self.__x_screen / 2, self.__y_screen / 2 + 0.75 * y_button),
                                (x_button, y_button), palette.PINK_RGB, palette.YELLOW_RGB, self.__use_keyboard_true,
                                 font_size=font_size)

        self.__update()
        while self._is_waiting_for_option:
            for event in pygame.event.get():
                muscle_button.on_click(event)
                keyboard_button.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__kill()
