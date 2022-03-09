from emg_games.backbones import SimpleBreakout


class Breakout(SimpleBreakout):
    game_name = 'breakout'

    def __init__(self, full_screen, player, main_game):

        super().__init__(full_screen, player, main_game)

        class_name = 'Breakout'

        self.emoji_name = ':cat:'
        self.emoji_color = (18, 156, 16)

