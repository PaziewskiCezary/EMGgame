import pygame
import random
import time

import numpy as np
import matplotlib.pyplot as plt

from copy import copy

from emg_games.backbones.abstract_game import AbstractGame
from emg_games.backbones import utils
from emg_games.gui.components import palette
from emg_games.gui.scenes.utils import add_corner_button 

# TODO move to utils
MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class RunningObjects(AbstractGame):

    def __init__(self, full_screen, player, main_game):

        super().__init__(full_screen, player, main_game)

        self._backgrounds = []

        self._targets = []

        self._projectiles = []

        self._game_name = 'Running Object'

        self.emoji_name = None
        self.emoji_color = None

    def _move_target(self, shift):

        if not self._target:
            raise ValueError('self._target not set')
        if abs(shift) > 1:
            raise ValueError('arg must be between -1 and 1')

        self._target.x_position += self._max_shift * shift

    def _set_targets(self):

        only_target = 0

        self._target = self._targets[only_target]

        target_width, target_height = self._targets[only_target].size

        target_y_position = self._y_screen - target_height
        self._target.y_position = target_y_position
        self._target.x_position = self._x_screen // 2 - self._target.size[1] // 2

        return target_y_position

    def _set_new_projectile(self):

        projectile_index = random.randint(0, len(self._projectiles) - 1)
        self._projectile = copy(self._projectiles[projectile_index])

        self._projectile.x_position = random.randint(self._projectile.size[0], self._x_screen -
                                                     self._projectile.size[0])
        self._projectile.y_position = random.randint(-200, 0)

        self.running_projectiles.append(self._projectile)
        # print("number of projectiles w funkcji ", len(self.running_projectiles))
        # self.time_since_new_projectile = time.time()

        self._projectile_number += 1

    def _punctation(self):

        break_loop = False
        new_projectile = False

        acceleration = 1.01 ** self._projectile_number

        y_step = self._y_screen * self._speed_rate * acceleration # * 10  # tak jest ciekawiej na razie

        for (i, projectile_) in enumerate(self.running_projectiles):
            projectile_x_position, projectile_y_position = projectile_.get_position
            projectile_.y_position = projectile_y_position + y_step
            if projectile_.bottom > self._target.y_position:

                new_projectile = False
                if utils.collide_in(projectile_, self._target, 5/4):
                    if self._target.type == projectile_.type:
                        self._score += 10
                    else:
                        self._lives -= 1
                        self._score += -100
                        self._missed += 1

                    new_projectile = True

                elif projectile_.top > self._y_screen:
                    if self._target.type == projectile_.type:
                        self._score -= 10
                    else:
                        self._score += 100
                    new_projectile = True

                if new_projectile:
                    self.running_projectiles.remove(projectile_)

                if self._lives <= 0:
                    break_loop = True

        return break_loop, new_projectile

    def _play(self):

        super()._play()
        play = True
        self._set_targets()
        
        self.running_projectiles = []

        # self.time_since_new_projectile = time.time()

        # self.new_projectile_counter = time.time()

        i = 0
        list_i = []
        current_projectiles = []
        all_projectiles = []
        funkcja = []

        while play and self._lives > 0:

            self._new_projectiles = 1

            while self._new_projectiles:
                # print("new projectiles ", self._new_projectiles)
                self._set_new_projectile()
                new_projectile_time = time.time()
                self._new_projectiles -= 1

            if not self._lives:
                play = False

            while self.running_projectiles:

                # print("time przed ", time.time() - self.new_projectile_counter)
                i += 1
                # if time.time() - self.new_projectile_counter > 0:
                print("running projectiles ", len(self.running_projectiles))
                print("all projectiles ", self._projectile_number)
                print("number 5/9 ", self._projectile_number ** (4 / 7))
                if (len(self.running_projectiles) <= self._projectile_number ** (4/7)) or \
                        (time.time() - new_projectile_time > 3):
                    list_i.append(i)
                    i = 0
                    # print("time po if ", time.time() - self.new_projectile_counter)
                    # print("number of projectile ", len(self.running_projectiles))
                    self._set_new_projectile()
                    new_projectile_time = time.time()
                    current_projectiles.append(len(self.running_projectiles))
                    all_projectiles.append(self._projectile_number)
                    funkcja.append(self._projectile_number ** (4 / 7))
                    # self.new_projectile_counter = time.time() + 1.02**(1/self._projectile_number)  # 1  # + 3 ** self._projectile_number
                    # print(0.98 ** (1 / self._projectile_number))

                break_loop = False

                self._keyboard_control(self._move_target)
                self._target.x_position = max(0,
                                              min(self._target.x_position,
                                                  self._screen_properties.x_screen - self._target.width)
                                              )

                if not self._player._use_keyboard:
                    self._muscle_control(self._move_target)

                break_loop, new_projectile = self._punctation()
                if break_loop:
                    break

                self._screen.fill(palette.BACKGROUND_COLOR)
                self._update_background()

                self._screen.blit(self._target.image, self._target.get_position)

                for projectile_ in self.running_projectiles:
                    self._screen.blit(projectile_.image, projectile_.get_position)

                # labels with lives and score
                
                self._make_health_text(emoji_name=self.emoji_name, emoji_color=self.emoji_color)
                menu_btn = add_corner_button(func=self.menu, text="Menu", x_screen=self._x_screen,
                                             y_screen=self._y_screen, screen=self._screen, loc='right',
                                             func_args={'save_score': True})
                for event in pygame.event.get():
                    menu_btn.on_click(event)
                    if event.type == pygame.QUIT:
                        self._kill()

                    play, break_loop = self._escape_game(event)
                    
                if break_loop:
                    break

                self._update()
                self._clock.tick(60)

            fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
            axs[0, 0].plot(list_i)
            axs[0, 0].set_title("ile minęło")
            axs[1, 0].plot(current_projectiles)
            axs[1, 0].set_title("obecnie")
            axs[0, 1].plot(all_projectiles)
            axs[0, 1].set_title("do tej pory")
            axs[1, 1].plot(funkcja)
            axs[1, 1].set_title("funkcja")

        self._save_score()

        self._what_next()
        plt.show()
    def _update_background(self):
        pass