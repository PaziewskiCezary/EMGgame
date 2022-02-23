from emg_games.backbones import utils
from emg_games.backbones import Projectile
from emg_games.backbones import Target

from emg_games.backbones.running_objects import RunningObjects


class Turtle(RunningObjects):
    game_name = 'ŻÓŁW'

    def __init__(self, full_screen, player):
        super().__init__(full_screen, player)

        class_name = "Turtle"

        self._targets = [Target(desired_width=self._x_screen * Target.percentage, img_path=target_path,
                                target_type=target_type) for (target_type, target_path) in
                         utils.get_targets(class_name)]

        self._projectiles = []
        for i, (projectile_type, projectile_path) in enumerate(utils.get_projectiles(class_name)):
            projectile = Projectile(desired_width=self._x_screen * Projectile.percentage,
                                    img_path=projectile_path, projectile_type=projectile_type)

            self._projectiles.append(projectile)

        self._game_name = 'Falling figures'

