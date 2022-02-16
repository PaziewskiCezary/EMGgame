import pygame
import numpy as np
import math

from emg_games.backbones.abstract_game import AbstractGame
from emg_games.backbones import utils
from emg_games.backbones import Projectile
from emg_games.backbones import Target

MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class Trash(AbstractGame):
    game_name = 'Spadające śmieci'

    def __init__(self, app, full_screen, player):

        super().__init__(app, full_screen, player)

        self._backgrounds = sorted([x for x in utils.get_backgrounds()])
        self._backgrounds = [pygame.image.load(x) for x in self._backgrounds]

        self._targets = [Target(desired_width=self._x_screen * Target.percentage, img_path=target_path,
                                target_type=target_type) for (target_type, target_path) in utils.get_targets()]

        self._projectiles = []
        for i, (projectile_type, projectile_path) in enumerate(utils.get_projectiles()):
            projectile = Projectile(desired_width=self._x_screen * Projectile.percentage,
                                    img_path=projectile_path, projectile_type=projectile_type)

            self._projectiles.append(projectile)

    def _set_targets(self):
        number_of_targets = len(self._targets)

        offset = (1 - number_of_targets * Target.percentage) / (number_of_targets + 1)
        offset = round(self._x_screen * offset)

        first_target = 0

        target_width, target_height = self._targets[first_target].size

        target_y_position = self._y_screen - target_height

        for target_number, target_ in enumerate(self._targets):
            target_x_position = target_width * target_number
            target_x_position += offset * (target_number + 1)
            target_.x_position = target_x_position
            target_.y_position = target_y_position

        return target_y_position

    def _play(self):

        self._lives = self._max_lives
        self._score = 0
        self._missed = 0

        self._background_idx = 0
        speed_rate = 0.0003
        projectile_number = 0

        target_y_position = self._set_targets()
        np.random.shuffle(self._projectiles)

        play = True
        new_projectile = True
        actual_projectile = None
        self._update_background()

        while self._projectiles and play and self._lives > 0:
            if new_projectile:
                self._projectile = self._projectiles.pop()
                projectile_number += 1

                # recalculate x to be in center
                self._projectile.x_position = self._x_screen // 2 - self._projectile.size[1] // 2
                self._projectile.y_position = 100
                new_projectile = False
                actual_projectile = True

            if not self._lives:
                play = False

            while actual_projectile:
                break_loop = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._kill()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False
                            break_loop = True

                        if event.key == pygame.K_LEFT:
                            self._move_projectile(MOVE_LEFT)

                        if event.key == pygame.K_RIGHT:
                            self._move_projectile(MOVE_RIGHT)

                        if event.key == pygame.K_DOWN:
                            self._projectile.y_position += 10
                if break_loop:
                    break

                if self.app.is_using_amp:
                    with self.app.amp.lock:

                        signal = self.app.amp.data[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
                        signal -= np.mean(signal)
                        signal = np.abs(signal)
                        move_value = self._muscle_move(np.mean(signal)) / 10  # comm why 10?
                        self._move_projectile(move_value)
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                play = False
                                break_loop = True

                            if event.key == pygame.K_LEFT:
                                self._move_projectile(MOVE_LEFT)

                            if event.key == pygame.K_RIGHT:
                                self._move_projectile(MOVE_RIGHT)

                if break_loop:
                    break

                projectile_x_position, projectile_y_position = self._projectile.get_position

                acceleration = 1.02 ** projectile_number

                y_step = self._y_screen * speed_rate * acceleration
                self._projectile.x_position, self._projectile.y_position = \
                    projectile_x_position, projectile_y_position + y_step
                if self._projectile.bottom > target_y_position:
                    collision = False
                    for (i, target_) in enumerate(self._targets):

                        if utils.collide_in(self._projectile, target_):
                            collision = True
                            if target_.type == self._projectile.type:
                                self._score += 100

                            else:
                                self._score += -10
                                self._missed += 1

                    if not collision:
                        self._lives -= 1

                    new_projectile = True
                    actual_projectile = False

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
        idx = math.log2(self._max_lives - self._lives + self._missed + 1)
        idx = int(idx)

        idx = min(idx, len(self._backgrounds) - 1)

        img = self._backgrounds[idx]
        self._screen.blit(img, [0, 0])
