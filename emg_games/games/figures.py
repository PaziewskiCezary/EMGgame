from emg_games.backbones import utils
from emg_games.backbones import Projectile
from emg_games.backbones import Target

from emg_games.backbones.falling_objects import FallingObjects


class Figures(FallingObjects):

    game_name = 'figury'

    def __init__(self, full_screen, player, main_game):

        super().__init__(full_screen, player, main_game)

        # TODO load this all in super __init__
        class_name = "Figures"

        self._targets = [Target(desired_width=self._x_screen * Target.percentage, img_path=target_path,
                                target_type=target_type) for (target_type, target_path) in
                         utils.get_targets(class_name)]

        self._projectiles = []
        for i, (projectile_type, projectile_path) in enumerate(utils.get_projectiles(class_name)):
            projectile = Projectile(desired_width=self._x_screen * Projectile.percentage,
                                    img_path=projectile_path, projectile_type=projectile_type,
                                    transparent=True)

            self._projectiles.append(projectile)
