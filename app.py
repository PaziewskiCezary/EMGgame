'''Simple game with falling stuff'''
# python game.py --keyboard --name fsdf --not-full

import argparse
import sys
from os import environ

from emg_games.backbones import AbstractGame


from emg_games.games.player import Player
from emg_games.gui.scenes import ScreenProperties

import emg_games.gui.scenes.game_chooser as game_chooser

from emg_games.games.trash import Trash

from emg_games.games.figures import Figures
from types import SimpleNamespace


environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    #parser.add_argument('--amplifier', dest='use_amplifier', action='store_true', help='run with amplifier')
    #parser.add_argument('--keyboard', dest='use_keyboard', action='store_true', help='run without amplifier')
    parser.add_argument('--not-full', dest='full_screen', action='store_true', help='turn off full screen')

    parser.add_argument('--name', dest='name', default='', type=str, help='set name')

    args = parser.parse_args()

    screen_properties = ScreenProperties(args.full_screen)

    player = Player(screen_properties=screen_properties)

    game = game_chooser.choose_game(screen_properties=screen_properties, kill_game=player.kill)

    game = game(
        full_screen=args.full_screen,
        player=player)

    game.menu()

