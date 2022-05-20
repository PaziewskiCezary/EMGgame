import pygame

from emg_games.gui.components.pygame_textinput import TextInput
from emg_games.gui.components.pygame_text import text
from emg_games.backbones.components.calibration import Calibration
from emg_games.gui.components import palette
from emg_games.gui.components.button import Button
from emg_games.gui.scenes.utils import add_corner_button


class Player:

    def __init__(self, screen_properties, amplifier=None):

        self.__name = ''
        self._calibrate_value_min = 0
        self._calibrate_value_max = float('inf')
        self.__input_type = None

        self.__screen_properties = screen_properties
        self.__screen = self.__screen_properties.screen

        self.__x_screen, self.__y_screen = self.__screen.get_size()
        self._use_keyboard = True
        self.__get_name()

        self.amp = amplifier
        self._get_input_type()



        print('calibration done')

    def __bool__(self):
        return self.name != '' and self.calibrate_values != (0, float('inf')) and self.__input_type is not None

    def kill(self):
        if self.amp:
            self.amp.terminate()
        pygame.quit()
        exit()

    @property
    def name(self):
        return self.__name

    @property
    def calibrate_value_min(self):
        return self._calibrate_value_min

    @property
    def calibrate_value_max(self):
        return self._calibrate_value_max
    
    @property
    def calibrate_values(self):
        return self.calibrate_value_min, self.calibrate_value_max

    @staticmethod
    def __update():
        pygame.display.update()

    def _make_calib(self):
        calibrate = Calibration(self.__screen, self.amp, kill_game=self.kill)
        calibrate.calibrate(self)

    def __get_name(self):

        
        input_name = TextInput(font_family=palette.FONT_STYLE, font_size=self.__y_screen // 13,
                               text_color=palette.TEXT_COLOR, max_string_length=15)
        self.__screen.fill(palette.BACKGROUND_COLOR)
        #self.__update()
        clock = pygame.time.Clock()
        is_input = True
        while is_input:
            self.__screen.fill(palette.BACKGROUND_COLOR)
            exit_btn = add_corner_button(func=self.kill, text="Wyjdź", x_screen=self.__x_screen, y_screen=self.__y_screen, screen=self.__screen, loc='right')
            text(self.__screen, palette.TEXT_COLOR, "PODAJ SWÓJ NICK:", self.__x_screen // 2, self.__y_screen // 4,
                 font_size=self.__y_screen // 13)
        
            
            events = pygame.event.get()
            input_name.update(events)
            text_length = input_name.font_object.size(input_name.get_text())[0]
            self.__screen.blit(input_name.get_surface(),
                               ((self.__x_screen - text_length) // 2, self.__y_screen // 2))

            self.__update()
            clock.tick(30)
            
            for event in events:
                exit_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self.kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__name = input_name.get_text()
                        is_input = False
                        break

    def _set_input_type(self, args):
        self._use_keyboard = args['use_keyboard']
        self._is_waiting_for_option = False

    def _get_input_type(self):
     

        self._is_waiting_for_option = True

        self.__screen.fill(palette.BACKGROUND_COLOR)

        exit_btn = add_corner_button(func=self.kill, text="Wyjdź", x_screen=self.__x_screen, y_screen=self.__y_screen, screen=self.__screen, loc='right')
        self.__update()

        x_button = self.__x_screen / 4
        y_button = self.__y_screen / 5
        font_size = int(x_button // 5)

        muscle_button = Button(screen=self.__screen,
                               label='Mięsień',
                               pos=(self.__x_screen / 2, self.__y_screen / 2 - 0.75 * y_button),
                               dims=(x_button, y_button),
                               button_color=palette.PINK_RGB,
                               label_color=palette.YELLOW_RGB,
                               func=self._set_input_type,
                               func_args={'use_keyboard': False},
                               font_size=font_size)

        keyboard_button = Button(screen=self.__screen,
                                 label='Klawiatura',
                                 pos=(self.__x_screen / 2, self.__y_screen / 2 + 0.75 * y_button),
                                 dims=(x_button, y_button),
                                 button_color=palette.PINK_RGB,
                                 label_color=palette.YELLOW_RGB,
                                 func=self._set_input_type, func_args={'use_keyboard': True},
                                 font_size=font_size)

        self.__update()
        while self._is_waiting_for_option:
            for event in pygame.event.get():
                exit_btn.on_click(event)
                muscle_button.on_click(event)
                keyboard_button.on_click(event)
                
                if event.type == pygame.QUIT:
                    self.kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.kill()

        if self.amp and not self._use_keyboard:

            self._make_calib()