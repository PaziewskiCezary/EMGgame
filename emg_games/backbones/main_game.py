from emg_games.backbones.components.player import Player
from emg_games.gui.scenes import ScreenProperties

from emg_games.gui.scenes import choose_game
class MainGame():

	def __init__(self, args):
		self.full_screen = args.full_screen
		self._new_game()

	def new_game(self):
		screen_properties = ScreenProperties(self.full_screen)

	    # options_screen(screen_properties=screen_properties)

	    if 
	    self.player = Player(screen_properties=screen_properties)

	    game = choose_game(screen_properties=screen_properties, kill_game=player.kill)

	    self.game = game(
	        full_screen=self.full_screen,
	        player=player)
	    self.game.menu()

	    if not player._use_keyboard:
	        player.amp.terminate()