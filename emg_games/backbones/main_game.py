from emg_games.backbones.components.player import Player
from emg_games.gui.scenes import ScreenProperties

from emg_games.gui.scenes import choose_game

from emg_games.amplifier import BipolarAmplifier, MonoAmplifier

import emg_games.games

from emg_games.gui.components import palette, text

import pygame

import inspect

from types import SimpleNamespace


class MainGame:

	def __init__(self, args):
		self.full_screen = args.full_screen
		self.screen_properties = ScreenProperties(self.full_screen)
		self.args = args

		text(self.screen_properties.screen, palette.SECONDARY_COLOR, 'Ładownie gry', 2 * self.screen_properties.x_screen // 4,
			self.screen_properties.y_screen // 2, font_size=30)

		pygame.display.update()


		# dummy_player = Player(screen_properties=self.screen_properties)
		dummy_player = SimpleNamespace()
		dummy_player.amp = None
		dummy_player.calibrate_values = float('inf'), 0
		dummy_player.name = 'dummy'
		dummy_player._use_keyboard = True

		self.list_of_games = {obj: obj(full_screen=self.full_screen, player=dummy_player, main_game=self)
							  for name, obj
							  in inspect.getmembers(emg_games.games, inspect.isclass)
							  if issubclass(obj, emg_games.backbones.AbstractGame)}

		self.amp = MonoAmplifier(name=args.amp_name, channels=[24])

		self._new_player()

	def _new_game(self):
		
		game = choose_game(self.screen_properties.screen, screen_properties=self.screen_properties, kill_game=self.player.kill)

		self.game = self.list_of_games[game]

		# self.game = game(
		# 				full_screen=self.full_screen,
		# 				player=self.player, main_game=self)
		#
		# gc.collect()
		self.game.player = self.player
		self.game.menu()

	def _new_player(self):

		self.player = Player(screen_properties=self.screen_properties, amplifier=self.amp)
		
		self._new_game()

	def _new_input_type(self, new_game=False):
		self.player._get_input_type()
		if new_game:
			self._new_game()
		else:
			self.game.menu()
