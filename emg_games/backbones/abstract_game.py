import pygame
import os
import time
import pickle
import numpy as np
import math

from abc import ABC, abstractmethod

from emg_games.gui.components import Button
from emg_games.gui.components import text
from emg_games.gui.scenes.screen_properties import ScreenProperties
from emg_games.gui.components import palette

MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0


class AbstractGame(ABC):
    """AbstractGame"""

    def __init__(self, app, full_screen, player):
        self.app = app
        self._player = player

        self._background_colour = palette.YELLOW_RGB
        self._text_colour = palette.PINK_RGB
        self._button_colour = palette.PINK_RGB
        self._button_text_colour = palette.YELLOW_RGB

        # TODO set full_screen
        self._full_screen = full_screen
        self._screen_properties = ScreenProperties(self._full_screen)
        self._screen = self._screen_properties.screen
        self._x_screen = self._screen_properties.x_screen
        self._y_screen = self._screen_properties.y_screen
        self._screen.fill(self._background_colour)
        # TODO move up

        pygame.init()

        self._max_lives = 3

        pygame.display.flip()

        self._clock = pygame.time.Clock()

        self._font_style = 'DejaVu Sans Mono'
        self._font_size = 30

        self._player = player

        self._max_shift = 10

        self._backgrounds = None

        self._targets = None

        self._projectiles = []

        self._game_name = ''

        self._projectile = None
        self._score = math.inf

        self._lives = math.inf

    def _kill(self):
        pygame.quit()
        exit()

    def _move_projectile(self, shift):
        if not self._projectile:
            raise ValueError('self.__projectile not set')
        if abs(shift) > 1:
            raise ValueError('arg must be between -1 and 1')

        self._projectile.x_position += self._max_shift * shift

    def _muscle_move(self, muscle_tension):

        calibration_difference = self._calibrate_value_max - self._calibrate_value_min
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

    @staticmethod
    def _update():
        pygame.display.update()

    def _start(self):
        self._calibrate_value_min, self._calibrate_value_max = self._player.calibrate_values

        self._name = self._player.name

        self._play()

    def _show_score(self):

        try:
            scores = pickle.load(open(f'../{self._game_name}_scores.pkl', 'rb'))
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))

        place = np.argmax(index) + 1

        self._screen.fill(self._background_colour)
        self._update()
        x_button, y_button = self._x_screen // 20, self._y_screen // 20
        button_font_size = self._y_screen // 18
        title_font_size = self._y_screen // 12
        subtitle_font_size = self._y_screen // 14
        points_font_size = self._y_screen // 16

        return_btn = Button(self._screen, 'Menu', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=self._button_colour, label_color=self._button_text_colour, func=self.menu,
                            font_size=button_font_size)
        again_btn = Button(self._screen, 'Zagraj jeszcze raz!', (self._x_screen // 2, 7 * self._y_screen // 8),
                           (x_button * 7, y_button * 3),
                           button_color=self._button_colour, label_color=self._button_text_colour, func=self._play,
                           font_size=button_font_size)

        text(self._screen, self._text_colour, 'WYNIK', self._x_screen // 2, self._y_screen // 4,
             font_size=title_font_size)
        text(self._screen, self._text_colour, 'Punkty', 3 * self._x_screen // 4, self._y_screen // 2,
             font_size=subtitle_font_size)
        text(self._screen, self._text_colour, 'Imię', 2 * self._x_screen // 4, self._y_screen // 2,
             font_size=subtitle_font_size)
        text(self._screen, self._text_colour, 'Pozycja', self._x_screen // 4, self._y_screen // 2,
             font_size=subtitle_font_size)

        self._update()
        time.sleep(1)

        text(self._screen, self._text_colour, str(self._score), 3 * self._x_screen // 4, self._y_screen // 2 + 100,
             font_size=points_font_size)
        self._update()
        time.sleep(1)

        text(self._screen, self._text_colour, self._name, 2 * self._x_screen // 4, self._y_screen // 2 + 100,
             font_size=points_font_size)
        self._update()
        time.sleep(1)

        text(self._screen, self._text_colour, f' {str(place) if place < 10 else str(place)}.', self._x_screen // 4,
             self._y_screen // 2 + 100,
             font_size=points_font_size)
        self._update()

        return return_btn, again_btn

    def _make_health_text(self):

        font_size = self._y_screen // 24
        font_size_heart = self._y_screen // 20
        score_text = "Punkty: " + str(self._score)
        lives_text = "Życia: "
        health_text = u"♥"
        width_heart, height_heart = pygame.font.SysFont(self._font_style, font_size_heart).size(health_text)
        width_score, _ = pygame.font.SysFont(self._font_style, font_size).size(score_text)
        width_lives, _ = pygame.font.SysFont(self._font_style, font_size).size(lives_text)
        # 'DejaVu Sans Mono'
        pygame.draw.rect(self._screen, self._background_colour,
                         (0, 0, self._x_screen, self._y_screen // 14), False)
        text(self._screen, self._text_colour, score_text, width_score / 2, 25, font_style=self._font_style,
             font_size=font_size)
        text(self._screen, self._text_colour, lives_text, self._x_screen // 2, 25, font_style=self._font_style,
             font_size=font_size)
        text(self._screen, self._text_colour, health_text * self._lives,
             self._x_screen // 2 + width_lives // 2 + 0.5 * self._lives * width_heart,
             25, font_style=self._font_style, font_size=font_size_heart)

        self._update()

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
    def _set_targets(self):
        pass

    @abstractmethod
    def _play(self):
        pass

    @abstractmethod
    def _update_background(self):
        pass

    def _save_score(self):
        if not os.path.isfile(f'../{self._game_name}_scores.pkl'):
            scores = []
            pickle.dump(scores, open(f'../{self._game_name}_scores.pkl', "wb"))

        scores = pickle.load(open(f'../{self._game_name}_scores.pkl', "rb"))
        scores.append((self._score, self._name))
        pickle.dump(scores, open(f'../{self._game_name}_scores.pkl', "wb"))

    def _scores(self):
        try:
            scores = pickle.load(open(f'../{self._game_name}_scores.pkl', "rb"))

        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        try:
            scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))
        except ValueError:
            scores, index = ['brak wyników'], [0]

        self._screen.fill(self._background_colour)
        self._update()
        x_button, y_button = self._x_screen // 20, self._y_screen // 20
        button_font_size = self._y_screen // 18
        return_btn = Button(self._screen, 'Wróć', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=self._button_colour, label_color=self._button_text_colour, func=self.menu,
                            font_size=button_font_size)
        text(self._screen, self._text_colour, 'WYNIKI', self._x_screen // 2, self._y_screen // 10 - 25,
             font_size=48)
        y_offset = 55
        for i in range(min(len(scores), 10)):
            text(self._screen, self._text_colour, f'{" " + str(i + 1) if i < 10 else str(i + 1)}.',
                 self._x_screen // 4,
                 self._y_screen // 10 + (i + 1) * y_offset)
            text(self._screen, self._text_colour, str(scores[i][1]), 2 * self._x_screen // 4,
                 self._y_screen // 10 + (i + 1) * y_offset)
            text(self._screen, self._text_colour, str(scores[i][0]), 3 * self._x_screen // 4,
                 self._y_screen // 10 + (i + 1) * y_offset)
            time.sleep(0.1)
            self._update()
        self._update()
        while True:
            for event in pygame.event.get():
                return_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self._kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()

    def menu(self):

        self._screen.fill(self._background_colour)

        pygame.display.set_caption('Segreguj smieci')

        x_button = self._x_screen / 4
        y_button = self._y_screen / 5
        font_size = int(x_button // 5)

        b_s = Button(self._screen, 'Start', (self._x_screen / 2, self._y_screen / 2 - 1.5 * y_button),
                     (x_button, y_button), self._button_colour, self._button_text_colour, self._start,
                     font_size=font_size)
        b_w = Button(self._screen, 'Wyniki', (self._x_screen / 2, self._y_screen / 2), (x_button, y_button),
                     self._button_colour, self._button_text_colour, self._scores, font_size=font_size)
        b_e = Button(self._screen, 'Wyjdź', (self._x_screen / 2, self._y_screen / 2 + 1.5 * y_button),
                     (x_button, y_button), self._button_colour, self._button_text_colour, self._kill,
                     font_size=font_size)

        self._update()
        while True:
            for event in pygame.event.get():
                b_s.on_click(event)
                b_w.on_click(event)
                b_e.on_click(event)
                if event.type == pygame.QUIT:
                    self._kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._kill()
