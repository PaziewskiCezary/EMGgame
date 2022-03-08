from emg_games.backbones.components.player import Player
from emg_games.gui.scenes import ScreenProperties

from emg_games.gui.scenes import choose_game

import gc


class MainGame():

	def __init__(self, args):
		self.full_screen = args.full_screen
		self.screen_properties = ScreenProperties(self.full_screen)
		self._new_player()

	def _new_game(self):
		
		game = choose_game(screen_properties=self.screen_properties, kill_game=self.player.kill)

		self.game = game(
						full_screen=self.full_screen,
						player=self.player, main_game=self)

		gc.collect()
		self.game.menu()

	def _new_player(self):

		self.player = Player(screen_properties=self.screen_properties)
		
		self._new_game()

	def _new_input_type(self, new_game=False):
		self.player._get_input_type()
		if new_game:
			self._new_game()
		else:
			self.game.menu()
