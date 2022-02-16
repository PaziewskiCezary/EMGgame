import pygame
import numpy as np
import math

from emg_games.backbones import utils
from emg_games.backbones import Projectile
from emg_games.backbones import Target

from emg_games.games.falling_objects import FallingObjects

MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class Figures(FallingObjects):

    game_name = 'FIGURY'

    def __init__(self, full_screen, player):

        super().__init__(full_screen, player)

        class_name = "Figures"

        self._backgrounds = sorted([x for x in utils.get_backgrounds(class_name)])
        self._backgrounds = [pygame.image.load(x) for x in self._backgrounds]

        self._targets = [Target(desired_width=self._x_screen * Target.percentage, img_path=target_path,
                                target_type=target_type) for (target_type, target_path) in
                         utils.get_targets(class_name)]

        self._projectiles = []
        for i, (projectile_type, projectile_path) in enumerate(utils.get_projectiles(class_name)):
            projectile = Projectile(desired_width=self._x_screen * Projectile.percentage,
                                    img_path=projectile_path, projectile_type=projectile_type)

            self._projectiles.append(projectile)

        self._game_name = 'Falling figures'
