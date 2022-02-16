'''Simple game with falling stuff'''
# python game.py --keyboard --name fsdf --not-full

import argparse
import sys
from os import environ


from emg_games.games.player import Player
from emg_games.gui.scenes import ScreenProperties

from emg_games.amplifier import Amplifier

import emg_games.gui.scenes.game_chooser as game_chooser

from emg_games.games.trash import Trash
from emg_games.games.figures import Figures
from types import SimpleNamespace
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    parser.add_argument('--amplifier', dest='use_amplifier', action='store_true', help='run with amplifier')
    parser.add_argument('--keyboard', dest='use_keyboard', action='store_true', help='run without amplifier')
    parser.add_argument('--not-full', dest='full_screen', action='store_true', help='turn off full screen')

    parser.add_argument('--name', dest='name', default='', type=str, help='set name')

    args = parser.parse_args()

    if args.use_amplifier:
        from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier

    if args.use_keyboard and args.use_amplifier:
        sys.exit('Can\'t use --amplifier and --keyboard at the same time')

    if not args.use_keyboard and not args.use_amplifier:
        args.use_amplifier = False
        args.use_keyboard = True

    app = SimpleNamespace()
    if args.use_amplifier:
        amp = Amplifier()
    else:
        app.amp = None

    app.is_using_amp = bool(app.amp)

    screen_properties = ScreenProperties(args.full_screen)

    player = Player(screen_properties=screen_properties, use_keyboard=args.use_keyboard, app=app)

    name_game = game_chooser.choose_game(screen_properties=screen_properties, kill_game=player.kill)
    print("name_game ", name_game)

    if name_game == "ŚMIECI":
        game = Trash(
            app,
            full_screen=args.full_screen,
            player=player)

    if name_game == "FIGURY":
        game = Figures(
            app,
            full_screen=args.full_screen,
            player=player)
    game.menu()

    if args.use_amplifier:
        amp.terminate()
