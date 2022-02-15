import pygame
import os
import time
import math
import pickle
import numpy as np

from abc import ABC

from emg_games.backbones import utils
from emg_games.gui.components import Button
from emg_games.backbones import Projectile
from emg_games.backbones import Target
from emg_games.gui.components import text
from .player import Player

MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0

from emg_games.gui.scenes.screen_properties import ScreenProperties
from emg_games.gui.components import palette


# class AbstractGame(ABC):
class AbstractGame:
    """AbstractGame"""

    def __init__(self, app, full_screen, player):
        self.app = app


        self.__background_colour = palette.YELLOW_RGB
        self.__text_colour = palette.PINK_RGB
        self.__button_colour = palette.PINK_RGB
        self.__button_text_colour = palette.YELLOW_RGB

        # TODO set full_screen
        self.__full_screen = full_screen
        self.__screen_properties = ScreenProperties(self.__full_screen)
        self.__screen = self.__screen_properties.screen
        self.__x_screen = self.__screen_properties.x_screen
        self.__y_screen = self.__screen_properties.y_screen
        self.__screen.fill(self.__background_colour)
        # TODO move up

        self.__max_lives = 3

        pygame.display.flip()

        self.__clock = pygame.time.Clock()

        self.__font_style = 'DejaVu Sans Mono'
        self.__font_size = 30

        self.__max_shift = 10

        self.__backgrounds = sorted([x for x in utils.get_backgrounds()])
        self.__backgrounds = [pygame.image.load(x) for x in self.__backgrounds]

        self.__targets = [Target(desired_width=self.__x_screen * Target.percentage, img_path=target_path,
                                 target_type=target_type) for (target_type, target_path) in utils.get_targets()]

        self.__projectiles = []
        for i, (projectile_type, projectile_path) in enumerate(utils.get_projectiles()):
            projectile = Projectile(desired_width=self.__x_screen * Projectile.percentage,
                                    img_path=projectile_path, projectile_type=projectile_type)

            self.__projectiles.append(projectile)



        # TODO move up
        self._game_name = 'Falling trash'

        self.__player = player


    def __kill(self):
        pygame.quit()
        exit()

    def __move_projectile(self, shift):
        if not self.__projectile:
            raise ValueError('self.__projectile not set')
        if abs(shift) > 1:
            raise ValueError('arg must be between -1 and 1')

        self.__projectile.x_position += self.__max_shift * shift

    def __muscle_move(self, muscle_tension):

        calibration_difference = self.__calibrate_value_max - self.__calibrate_value_min
        number_of_movement_interval = 3
        movement_interval = calibration_difference / number_of_movement_interval
        second_movement_interval = 2 * movement_interval
        third_movement_interval = 3 * movement_interval

        if muscle_tension <= self.__calibrate_value_min:
            return MOVE_LEFT
        elif muscle_tension >= self.__calibrate_value_max:
            return MOVE_RIGHT
        else:
            actual_muscle_tension = muscle_tension - self.__calibrate_value_min
            if actual_muscle_tension <= movement_interval:
                return (actual_muscle_tension - movement_interval) / movement_interval
            elif movement_interval < actual_muscle_tension <= second_movement_interval:
                return MOVE_DOWN
            elif second_movement_interval < actual_muscle_tension <= third_movement_interval:
                return (actual_muscle_tension - second_movement_interval) / movement_interval

    @staticmethod
    def __update():
        pygame.display.update()

    def __start(self):
        self.__calibrate_value_min, self.__calibrate_value_max = self.__player.calibrate_values

        self.__name = self.__player.name

        self.__play()

    def __show_score(self):

        try:
            scores = pickle.load(open(f'../{self._game_name}_scores.pkl', 'rb'))
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))

        place = np.argmax(index) + 1

        self.__screen.fill(self.__background_colour)
        self.__update()
        x_button, y_button = self.__x_screen // 20, self.__y_screen // 20
        button_font_size = self.__y_screen // 18
        title_font_size = self.__y_screen // 12
        subtitle_font_size = self.__y_screen // 14
        points_font_size = self.__y_screen // 16

        return_btn = Button(self.__screen, 'Menu', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=self.__button_colour, label_color=self.__button_text_colour, func=self.menu,
                            font_size=button_font_size)
        again_btn = Button(self.__screen, 'Zagraj jeszcze raz!', (self.__x_screen // 2, 7 * self.__y_screen // 8),
                           (x_button * 7, y_button * 3),
                           button_color=self.__button_colour, label_color=self.__button_text_colour, func=self.__play,
                           font_size=button_font_size)

        text(self.__screen, self.__text_colour, 'WYNIK', self.__x_screen // 2, self.__y_screen // 4, font_size=title_font_size)
        text(self.__screen, self.__text_colour, 'Punkty', 3 * self.__x_screen // 4, self.__y_screen // 2, font_size=subtitle_font_size)
        text(self.__screen, self.__text_colour, 'Imię', 2 * self.__x_screen // 4, self.__y_screen // 2, font_size=subtitle_font_size)
        text(self.__screen, self.__text_colour, 'Pozycja', self.__x_screen // 4, self.__y_screen // 2, font_size=subtitle_font_size)

        self.__update()
        time.sleep(1)

        text(self.__screen, self.__text_colour, str(self.__score), 3 * self.__x_screen // 4, self.__y_screen // 2 + 100, font_size=points_font_size)
        self.__update()
        time.sleep(1)

        text(self.__screen, self.__text_colour, self.__name, 2 * self.__x_screen // 4, self.__y_screen // 2 + 100, font_size=points_font_size)
        self.__update()
        time.sleep(1)

        text(self.__screen, self.__text_colour, f' {str(place) if place < 10 else str(place)}.', self.__x_screen // 4, self.__y_screen // 2 + 100,
                    font_size=points_font_size)
        self.__update()

        return return_btn, again_btn

    def __make_health_text(self):

        font_size = self.__y_screen // 24
        font_size_heart = self.__y_screen // 20
        score_text = "Punkty: " + str(self.__score)
        lives_text = "Życia: "
        health_text = u"♥"
        width_heart, height_heart = pygame.font.SysFont(self.__font_style, font_size_heart).size(health_text)
        width_score, _ = pygame.font.SysFont(self.__font_style, font_size).size(score_text)
        width_lives, _ = pygame.font.SysFont(self.__font_style, font_size).size(lives_text)
        # 'DejaVu Sans Mono'
        pygame.draw.rect(self.__screen, self.__background_colour,
                         (0, 0, self.__x_screen, self.__y_screen // 14), False)
        text(self.__screen, self.__text_colour, score_text, width_score / 2, 25, font_style=self.__font_style, font_size=font_size)
        text(self.__screen, self.__text_colour, lives_text, self.__x_screen//2, 25, font_style=self.__font_style, font_size=font_size)
        text(self.__screen, self.__text_colour, health_text * self.__lives, self.__x_screen//2 + width_lives//2 + 0.5 * self.__lives * width_heart,
                    25, font_style=self.__font_style, font_size=font_size_heart)

        self.__update()

    # TODO find better name
    def __what_next(self):

        return_btn, again_btn = self.__show_score()
        while True:
            for event in pygame.event.get():
                return_btn.on_click(event)
                again_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()

    def __set_targets(self):

        number_of_targets = len(self.__targets)

        offset = (1 - number_of_targets * Target.percentage) / (number_of_targets + 1)
        offset = round(self.__x_screen * offset)

        first_target = 0

        target_width, target_height = self.__targets[first_target].size

        target_y_position = self.__y_screen - target_height

        for target_number, target_ in enumerate(self.__targets):
            target_x_position = target_width * target_number
            target_x_position += offset * (target_number + 1)
            target_.x_position = target_x_position
            target_.y_position = target_y_position

        return target_y_position

    def __play(self):

        self.__lives = self.__max_lives
        self.__score = 0
        self.__missed = 0

        self.__background_idx = 0
        speed_rate = 0.0003
        projectile_number = 0

        target_y_position = self.__set_targets()
        np.random.shuffle(self.__projectiles)

        play = True
        new_projectile = True
        actual_projectile = None
        self.__update_background()

        while self.__projectiles and play and self.__lives > 0:
            if new_projectile:
                self.__projectile = self.__projectiles.pop()
                projectile_number += 1

                # recalculate x to be in center
                self.__projectile.x_position = self.__x_screen // 2 - self.__projectile.size[1] // 2
                self.__projectile.y_position = 100
                new_projectile = False
                actual_projectile = True

            if not self.__lives:
                play = False

            while actual_projectile:
                break_loop = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__kill()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False
                            break_loop = True

                        if event.key == pygame.K_LEFT:
                            self.__move_projectile(MOVE_LEFT)

                        if event.key == pygame.K_RIGHT:
                            self.__move_projectile(MOVE_RIGHT)

                        if event.key == pygame.K_DOWN:
                            self.__projectile.y_position += 10
                if break_loop:
                    break

                if self.app.is_using_amp:
                    with self.lock:
                        signal = self.__sample_array[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
                    signal -= np.mean(signal)
                    signal = np.abs(signal)
                    move_value = self.__muscle_move(np.mean(signal)) / 10   # comm why 10?
                    self.__move_projectile(move_value)
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                play = False
                                break_loop = True

                            if event.key == pygame.K_LEFT:
                                self.__move_projectile(MOVE_LEFT)

                            if event.key == pygame.K_RIGHT:
                                self.__move_projectile(MOVE_RIGHT)

                if break_loop:
                    break

                projectile_x_position, projectile_y_position = self.__projectile.get_position

                acceleration = 1.02 ** projectile_number

                y_step = self.__y_screen * speed_rate * acceleration
                self.__projectile.x_position, self.__projectile.y_position = projectile_x_position, projectile_y_position + y_step
                if self.__projectile.bottom > target_y_position:
                    collision = False
                    for (i, target_) in enumerate(self.__targets):

                        if utils.collide_in(self.__projectile, target_):
                            collision = True
                            if target_.type == self.__projectile.type:
                                self.__score += 100

                            else:
                                self.__score += -10
                                self.__missed += 1

                    if not collision:
                        self.__lives -= 1

                    new_projectile = True
                    actual_projectile = False

                # showing bins
                self.__screen.fill(self.__background_colour)
                self.__update_background()

                for target_ in self.__targets:
                    self.__screen.blit(target_.image, target_.get_position)
                self.__screen.blit(self.__projectile.image, self.__projectile.get_position)

                # labels with lives and score
                self.__make_health_text()

                self.__clock.tick(60)

        self.__score = self.__score
        self.__save_score()

        self.__what_next()

    # @abstractmethod
    def __update_background(self):
        idx = math.log2(self.__max_lives - self.__lives + self.__missed + 1)
        idx = int(idx)

        idx = min(idx, len(self.__backgrounds) - 1)

        img = self.__backgrounds[idx]
        self.__screen.blit(img, [0, 0])


    def __save_score(self):
        if not os.path.isfile(f'../{self._game_name}_scores.pkl'):
            scores = []
            pickle.dump(scores, open(f'../{self._game_name}_scores.pkl', "wb"))

        scores = pickle.load(open(f'../{self._game_name}_scores.pkl', "rb"))
        scores.append((self.__score, self.__name))
        pickle.dump(scores, open(f'../{self._game_name}_scores.pkl', "wb"))

    def __scores(self):
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

        self.__screen.fill(self.__background_colour)
        self.__update()
        x_button, y_button = self.__x_screen // 20, self.__y_screen // 20
        button_font_size = self.__y_screen // 18
        return_btn = Button(self.__screen, 'Wróć', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=self.__button_colour, label_color=self.__button_text_colour, func=self.menu,
                            font_size=button_font_size)
        text(self.__screen, self.__text_colour, 'WYNIKI', self.__x_screen // 2, self.__y_screen // 10 - 25, font_size=48)
        y_offset = 55
        for i in range(min(len(scores), 10)):
            text(self.__screen, self.__text_colour, f'{" " + str(i + 1) if i < 10 else str(i + 1)}.', self.__x_screen // 4,
                        self.__y_screen // 10 + (i + 1) * y_offset)
            text(self.__screen, self.__text_colour, str(scores[i][1]), 2 * self.__x_screen // 4, self.__y_screen // 10 + (i + 1) * y_offset)
            text(self.__screen, self.__text_colour, str(scores[i][0]), 3 * self.__x_screen // 4, self.__y_screen // 10 + (i + 1) * y_offset)
            time.sleep(0.1)
            self.__update()
        self.__update()
        while True:
            for event in pygame.event.get():
                return_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()

    def menu(self):

        self.__screen.fill(self.__background_colour)

        pygame.display.set_caption('Segreguj smieci')

        x_button = self.__x_screen / 4
        y_button = self.__y_screen / 5
        font_size = int(x_button // 5)

        b_s = Button(self.__screen, 'Start', (self.__x_screen / 2, self.__y_screen / 2 - 1.5 * y_button),
                     (x_button, y_button), self.__button_colour, self.__button_text_colour, self.__start,
                     font_size=font_size)
        b_w = Button(self.__screen, 'Wyniki', (self.__x_screen / 2, self.__y_screen / 2), (x_button, y_button),
                     self.__button_colour, self.__button_text_colour, self.__scores, font_size=font_size)
        b_e = Button(self.__screen, 'Wyjdź', (self.__x_screen / 2, self.__y_screen / 2 + 1.5 * y_button),
                     (x_button, y_button), self.__button_colour, self.__button_text_colour, self.__kill,
                     font_size=font_size)

        self.__update()
        while True:
            for event in pygame.event.get():
                b_s.on_click(event)
                b_w.on_click(event)
                b_e.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__kill()
