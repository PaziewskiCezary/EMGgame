import pygame
import math

from emg_games.backbones import utils
from emg_games.backbones import Projectile
from emg_games.backbones import Target

from emg_games.backbones.falling_objects import FallingObjects


class Trash(FallingObjects):

    game_name = 'śmieci'

    def __init__(self, full_screen, player, main_game):
        super().__init__(full_screen, player, main_game)

        class_name = "Trash"

        # TODO load this all in super __init__
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

        self.emoji_name = ':earth_africa:'
        self.emoji_color = (42, 189, 40)

    def _update_background(self):
        idx = math.log2(self._max_lives - self._lives + self._missed + 1)
        idx = int(idx)

        idx = min(idx, len(self._backgrounds) - 1)

        img = self._backgrounds[idx]
        self._screen.blit(img, [0, 0])
