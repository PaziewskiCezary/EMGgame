import pygame
import numpy as np
import random
import time

from emg_games.backbones.abstract_game import AbstractGame
from emg_games.backbones import utils
from emg_games.backbones import Projectile
from emg_games.backbones import Target

MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class RunningObjects(AbstractGame):

    def __init__(self, full_screen, player):

        super().__init__(full_screen, player)

        self._backgrounds = []

        self._targets = []

        self._projectiles = []

        self._game_name = 'Running Object'

    def _move_target(self, shift):
        # if not self._projectile:
        #     raise ValueError('self.__projectile not set')
        # if abs(shift) > 1:
        #     raise ValueError('arg must be between -1 and 1')

        self._target.x_position += self._max_shift * shift

    def _set_projectiles(self):

        pass

    def _set_targets(self):

        only_target = 0

        self._target = self._targets[only_target]

        target_width, target_height = self._targets[only_target].size

        target_y_position = self._y_screen - target_height
        self._target.y_position = target_y_position
        self._target.x_position = self._x_screen // 2 - self._target.size[1] // 2

        return target_y_position

    def _set_new_projectile(self, running_projectiles, projectile_number):

        projectile_index = random.randint(0, len(self._projectiles) - 1)
        self._projectile = self._projectiles[projectile_index]
        running_projectiles.append(self._projectile)
        projectile_number += 1

        self._projectile.x_position = random.randint(0 + self._projectile.size[0] // 2, self._x_screen -
                                                     self._projectile.size[0] // 2)
        self._projectile.y_position = 100

        return running_projectiles, projectile_number

    def _play(self):

        self._lives = self._max_lives
        self._score = 0
        self._missed = 0

        self._background_idx = 0
        speed_rate = 0.0003
        projectile_number = 0

        np.random.shuffle(self._projectiles)
        target_y_position = self._set_targets()

        play = True
        new_projectile = True
        actual_projectile = None
        self._update_background()

        running_projectiles = []

        while play and self._lives > 0:
            if new_projectile:

                running_projectiles, projectile_number = self._set_new_projectile(running_projectiles, projectile_number)
                new_projectile = False
                actual_projectile = True

            if not self._lives:
                play = False

            while len(running_projectiles) != 0:

                break_loop = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._kill()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False
                            break_loop = True

                        if event.key == pygame.K_LEFT:
                            self._move_target(MOVE_LEFT)

                        if event.key == pygame.K_RIGHT:
                            self._move_target(MOVE_RIGHT)

                if break_loop:
                    break

                if not self._player._use_keyboard:
                    with self._player.amp.lock:
                        signal = self.app.amp.data[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
                        signal -= np.mean(signal)
                        signal = np.abs(signal)
                        move_value = self._muscle_move(np.mean(signal)) / 10  # comm why 10?
                        self._move_target(move_value)
                # else:  #przesunięte o tab wszystko do if break_loop
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False
                            break_loop = True

                        # if event.key == pygame.K_LEFT:
                        #     self._move_projectile(MOVE_LEFT)
                        #
                        # if event.key == pygame.K_RIGHT:
                        #     self._move_projectile(MOVE_RIGHT)

                if break_loop:
                    break

                time1 = time.time()
                for (i, projectile_) in enumerate(running_projectiles):
                    time0 = time.time()
                    if time1 - time0 >= 10.98 ** projectile_number:
                        running_projectiles, projectile_number = self._set_new_projectile(running_projectiles,
                                                                                          projectile_number)
                        new_projectile = False
                        actual_projectile = True

                    projectile_x_position, projectile_y_position = projectile_.get_position

                    acceleration = 1.02 ** projectile_number

                    y_step = self._y_screen * speed_rate * acceleration
                    projectile_.x_position, projectile_.y_position = \
                        projectile_x_position, projectile_y_position + y_step
                    if projectile_.bottom > target_y_position:
                        collision = False

                        if utils.collide_in(projectile_, self._target):
                            collision = True
                            if target_.type == self._projectile.type:
                                self._score += 10

                            else:
                                self._lives -= 1
                                self._score += -100
                                self._missed += 1

                        if not collision:
                            if target_.type == self._projectile.type:
                                self._score -= 10
                            else:
                                self._score += 100

                        new_projectile = True
                        actual_projectile = False
                        running_projectiles.remove(projectile_)
                        time1 = time.time()
                    # if projectile_.bottom > self._y_screen

                # showing bins
                self._screen.fill(self._background_colour)
                self._update_background()

                for target_ in self._targets:
                    self._screen.blit(target_.image, target_.get_position)
                self._screen.blit(self._projectile.image, self._projectile.get_position)

                # labels with lives and score
                self._make_health_text()

                self._clock.tick(60)

        self._score = self._score
        self._save_score()

        self._what_next()

    def _update_background(self):
        pass
