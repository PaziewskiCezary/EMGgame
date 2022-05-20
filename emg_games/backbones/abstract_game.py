import pygame
import os
import time
import pickle
import numpy as np

from abc import ABC, abstractmethod
from pathlib import Path

from emg_games.gui.components import Button
from emg_games.gui.components import text

from emg_games.gui.scenes.screen_properties import ScreenProperties
from emg_games.gui.components import palette

from emg_games.gui.scenes.utils import add_corner_button 

from emg_games.backbones.utils import calc_font_size, is_key_pressed

import emoji
from pathlib import Path


MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class AbstractGame(ABC):
    """AbstractGame"""

    def __init__(self, full_screen, player, main_game):


        # TODO set full_screen
        self._full_screen = full_screen
        self._screen_properties = ScreenProperties(self._full_screen)
        self._screen = self._screen_properties.screen

        # fix for blank space when creating game object
        self._screen.fill(palette.PRIMARY_COLOR)
        pygame.display.flip()

        self._x_screen = self._screen_properties.x_screen
        self._y_screen = self._screen_properties.y_screen
        self._screen.fill(palette.PRIMARY_COLOR)
        # TODO move up

        self._max_lives = 1

        self.main_game = main_game

        self._clock = pygame.time.Clock()

        self._player = player

        self._max_shift = 5

        self._speed_rate = 0.0003

        self._backgrounds = None

        self._targets = []

        self._projectiles = []

        self._projectile = None

        if not hasattr(self, 'game_name'):
            raise ValueError(f'no "game_name" set as class variable for {self.__class__}')

    # TODO Move to utils
    def _kill(self):
        pygame.quit()
        exit()

    def _muscle_move(self, muscle_tension):
        calibration_difference = self._player.calibrate_value_max - self._player.calibrate_value_min
        number_of_movement_interval = 3
        movement_interval = calibration_difference / number_of_movement_interval
        second_movement_interval = 2 * movement_interval
        third_movement_interval = 3 * movement_interval

        if muscle_tension <= self._calibrate_value_min:
            return MOVE_LEFT
        elif muscle_tension >= self._calibrate_value_max:
            return MOVE_RIGHT
        else:
            actual_muscle_tension = muscle_tension - self._calibrate_value_min
            if actual_muscle_tension <= movement_interval:
                return (actual_muscle_tension - movement_interval) / movement_interval
            elif movement_interval < actual_muscle_tension <= second_movement_interval:
                return MOVE_DOWN
            elif second_movement_interval < actual_muscle_tension <= third_movement_interval:
                return (actual_muscle_tension - second_movement_interval) / movement_interval

    def _escape_game(self, event):

        play = True
        break_loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                play = False
                break_loop = True

        return play, break_loop

    def _keyboard_control(self, moving_function):

        if is_key_pressed(pygame.K_LEFT, pygame.K_a):
            moving_function(MOVE_LEFT)

        if is_key_pressed(pygame.K_RIGHT, pygame.K_d):
            moving_function(MOVE_RIGHT)

    def _muscle_control(self, moving_function):

        signal = self._player.amp.data[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
        signal -= np.mean(signal)
        signal = np.abs(signal)
        move_value = self._muscle_move(np.mean(signal)) / 10  # comm why 10?
        moving_function(move_value)

    @staticmethod
    def _update():
        pygame.display.update()

    def _start(self):
        self._calibrate_value_min, self._calibrate_value_max = self._player.calibrate_values

        self._name = self._player.name

        self._play()

    def _show_score(self):

        exit_btn = add_corner_button(func=self._kill, text="Wyjdź", x_screen=self._x_screen, y_screen=self._y_screen, screen=self._screen, loc='right')
        self._update()

        path = self.get_scores_path
        try:
            scores = pickle.load(open(path, 'rb'))
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))

        place = np.argmax(index) + 1

        self._screen.fill(palette.PRIMARY_COLOR)
        self._update()
        x_button, y_button = self._x_screen // 20, self._y_screen // 20
        button_font_size = self._y_screen // 18
        title_font_size = self._y_screen // 12
        subtitle_font_size = self._y_screen // 14
        points_font_size = self._y_screen // 16

        return_btn = Button(self._screen, 'Menu', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=palette.SECONDARY_COLOR, label_color=palette.PRIMARY_COLOR, func=self.menu,
                            font_size=button_font_size)
        again_btn = Button(self._screen, 'Zagraj jeszcze raz!', (self._x_screen // 2, 7 * self._y_screen // 8),
                           (x_button * 7, y_button * 3),
                           button_color=palette.SECONDARY_COLOR, label_color=palette.PRIMARY_COLOR, func=self._play,
                           font_size=button_font_size)

        text(self._screen, palette.SECONDARY_COLOR, 'WYNIK', self._x_screen // 2, self._y_screen // 4,
             font_size=title_font_size)
        text(self._screen, palette.SECONDARY_COLOR, 'Punkty', 3 * self._x_screen // 4, self._y_screen // 2,
             font_size=subtitle_font_size)
        text(self._screen, palette.SECONDARY_COLOR, 'Imię', 2 * self._x_screen // 4, self._y_screen // 2,
             font_size=subtitle_font_size)
        text(self._screen, palette.SECONDARY_COLOR, 'Pozycja', self._x_screen // 4, self._y_screen // 2,
             font_size=subtitle_font_size)

        def animate_sleep(seconds=1):
            start = time.time()

            while time.time() - start < seconds:
                for event in pygame.event.get():
                    exit_btn.on_click(event)
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        return False

                    if event.type == pygame.QUIT:
                        self._kill()

            return True

        animate = True
        # TODO allow for braking "animation"
        self._update()
        if animate:
            animate = animate_sleep(1)

        text(self._screen, palette.SECONDARY_COLOR, str(self._score), 3 * self._x_screen // 4,
             self._y_screen // 2 + 100, font_size=points_font_size)
        self._update()
        if animate:
            animate = animate_sleep(1)

        text(self._screen, palette.SECONDARY_COLOR, self._name, 2 * self._x_screen // 4, self._y_screen // 2 + 100,
             font_size=points_font_size)
        self._update()
        if animate:
            animate = animate_sleep(1)

        text(self._screen, palette.SECONDARY_COLOR, f' {str(place) if place < 10 else str(place)}.',
             self._x_screen // 4, self._y_screen // 2 + 100, font_size=points_font_size)
        self._update()

        return return_btn, again_btn

    def _make_health_text(self, emoji_name=':hearts:', emoji_color=palette.SECONDARY_COLOR):
        emoji_name = emoji_name if emoji_name else ':hearts:'
        emoji_color = emoji_color if emoji_color else palette.SECONDARY_COLOR

        # most of this code should run once
        font_size = self._y_screen // 24
        emoji_font_size = self._y_screen // 30
        score_text = "Punkty: " + str(self._score)
        lives_text = "Życia: "

        emoji_text = emoji.emojize(emoji_name, use_aliases=True)[0]

        emoji_font = Path(__file__).parent / 'components/NotoEmoji-Regular.ttf'
        emoji_font = pygame.freetype.Font(emoji_font, emoji_font_size)

        emoji_heart, emoji_heart = emoji_font.get_rect(emoji_text).size
        width_score, _ = pygame.font.SysFont(palette.FONT_STYLE, font_size).size(score_text)
        width_lives, _ = pygame.font.SysFont(palette.FONT_STYLE, font_size).size(lives_text)

        pygame.draw.rect(self._screen, palette.PRIMARY_COLOR,
                         (0, 0, self._x_screen * 19/10, self._y_screen // 10), False)

        MAGIC_NUMBER = 25  # why there was random 25  like 8 times!?!?!?

        text(self._screen, palette.SECONDARY_COLOR, score_text, width_score / 2, MAGIC_NUMBER, font_style=palette.FONT_STYLE,
             font_size=font_size)
        text(self._screen, palette.SECONDARY_COLOR, lives_text, self._x_screen // 2, MAGIC_NUMBER, font_style=palette.FONT_STYLE,
             font_size=font_size)

        # place emojis
        lives_text = emoji_text * self._lives
        lives_text_rect = emoji_font.get_rect(lives_text)
        lives_text_rect.center = self._x_screen // 2 + width_lives // 2 + 0.5 * self._lives * emoji_heart, MAGIC_NUMBER
        emoji_font.render_to(self._screen, lives_text_rect, lives_text, emoji_color, size=emoji_font_size)

        #self._update()

    # TODO find better name
    def _what_next(self):

        return_btn, again_btn = self._show_score()
        while True:
            for event in pygame.event.get():
                return_btn.on_click(event)
                again_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self._kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()

    @abstractmethod
    def _update_background(self):
        pass

    @abstractmethod
    def _set_targets(self):
        pass

    @abstractmethod
    def _set_new_projectile(self):
        pass

    @abstractmethod
    def _punctation(self):
        pass

    @abstractmethod
    def _play(self):

        self._lives = self._max_lives
        self._score = 0
        self._missed = 0

        self._background_idx = 0
        self._projectile_number = 0

        np.random.shuffle(self._projectiles)
        self._update_background()


    def add_exit_button(self):
        pass

    def _save_score(self):
        path = self.get_scores_path

        if not os.path.isfile(path):
            scores = []
            pickle.dump(scores, open(path, 'wb'))

        scores = pickle.load(open(path, 'rb'))
        scores.append((self._score, self._name))
        pickle.dump(scores, open(path, 'wb'))

    @property
    def get_scores_path(self):
        return Path().home() / f'{self.game_name} scores.pkl'

    def _scores(self):
        path = self.get_scores_path
        try:
            scores = pickle.load(open(path, 'rb'))
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        try:
            scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))
        except ValueError:
            scores, index = ['brak wyników'], [0]

        self._screen.fill(palette.PRIMARY_COLOR)
        

        # menu_btn = add_corner_button(func=self.menu, text="Menu", x_screen=self._x_screen, y_screen=self._y_screen, screen=self._screen, loc='left')
        self._update()

        exit_btn = add_corner_button(func=self._kill, text="Wyjdź", x_screen=self._x_screen, y_screen=self._y_screen, screen=self._screen, loc='right')
        self._update()

        '''x_button, y_button = self._x_screen // 20, self._y_screen // 20
                                button_font_size = self._y_screen // 18
                                return_btn = Button(self._screen, 'Wróć', (x_button, y_button), (x_button * 2, y_button * 2),
                                                    button_color=palette.SECONDARY_COLOR, label_color=palette.PRIMARY_COLOR, func=self.menu,
                                                    font_size=button_font_size)'''
        MAGIC_NUMBER = 25
        text(self._screen, palette.SECONDARY_COLOR, 'WYNIKI', self._x_screen // 2, self._y_screen // 10 - MAGIC_NUMBER,
             font_size=48)

        y_offset = 55
        for i in range(min(len(scores), 10)):
            text(self._screen, palette.SECONDARY_COLOR, f'{" " + str(i + 1) if i < 10 else str(i + 1)}.',
                 self._x_screen // 4,
                 self._y_screen // 10 + (i + 1) * y_offset)
            text(self._screen, palette.SECONDARY_COLOR, str(scores[i][1]), 2 * self._x_screen // 4,
                 self._y_screen // 10 + (i + 1) * y_offset)
            text(self._screen, palette.SECONDARY_COLOR, str(scores[i][0]), 3 * self._x_screen // 4,
                 self._y_screen // 10 + (i + 1) * y_offset)
            time.sleep(0.1)
            self._update()
        self._update()
        while True:
            for event in pygame.event.get():
                exit_btn.on_click(event)
                # menu_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self._kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()

    def change_game(self):
        return True

    def menu(self):

        self._screen.fill(palette.PRIMARY_COLOR)

        pygame.display.set_caption(self.game_name)

        x_button = self._x_screen / 4
        y_button = self._y_screen / 5
        list_of_buttons = ["Start", "Wyniki", 'Wyjdź', 'Zmień grę', 'Zmień gracza', 'Zmień sterowanie']
        font_size = calc_font_size(list_of_buttons, x_button)

        button_start = Button(self._screen, list_of_buttons[0], (self._x_screen / 4,
                                                                 self._y_screen / 2 - 1.5 * y_button),
                              (x_button, y_button), palette.SECONDARY_COLOR, palette.PRIMARY_COLOR, self._start,
                              font_size=font_size)
        button_scores = Button(self._screen, list_of_buttons[1], (self._x_screen / 4, self._y_screen / 2), (x_button,
                                                                                                            y_button),
                               palette.SECONDARY_COLOR, palette.PRIMARY_COLOR, self._scores, font_size=font_size)
        
        button_exit = Button(self._screen, list_of_buttons[2], (self._x_screen / 4,
                                                                self._y_screen / 2 + 1.5 * y_button),
                             (x_button, y_button), palette.SECONDARY_COLOR, palette.PRIMARY_COLOR, self._kill,
                             font_size=font_size)

        button_change_game = Button(self._screen, list_of_buttons[3], (self._x_screen - self._x_screen / 4,
                                                                       self._y_screen / 2 - 1.5 * y_button),
                                    (x_button, y_button), palette.SECONDARY_COLOR, palette.PRIMARY_COLOR,
                                    self.main_game._new_game, font_size=font_size)

        button_change_player = Button(self._screen, list_of_buttons[4], (self._x_screen - self._x_screen / 4,
                                                                     self._y_screen / 2), (x_button, y_button),
                                      palette.SECONDARY_COLOR, palette.PRIMARY_COLOR, self.main_game._new_player,
                                      font_size=font_size)
        
        button_change_input_type = Button(self._screen, list_of_buttons[5], (self._x_screen - self._x_screen / 4,
                                                                             self._y_screen / 2 + 1.5 * y_button),
                                          (x_button, y_button), palette.SECONDARY_COLOR, palette.PRIMARY_COLOR,
                                          self.main_game._new_input_type, font_size=font_size)

        self._update()
        while True:
            for event in pygame.event.get():

                button_start.on_click(event)
                button_scores.on_click(event)
                button_exit.on_click(event)
                button_change_game.on_click(event)
                button_change_player.on_click(event)
                button_change_input_type.on_click(event)

                if event.type == pygame.QUIT:
                    self._kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._kill()
