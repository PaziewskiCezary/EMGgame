'''Simple game with falling stuff'''
# python game.py --keyboard --name fsdf --not-full

import argparse
import sys
import os
import signal
import platform

import time

import numpy as np

import multiprocessing as mp

from os import environ
from types import SimpleNamespace

from emg_games.games import Player
from emg_games.gui.scenes import ScreenProperties

from emg_games.backbones import AbstractGame

from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier


>>>>>>> effdf072f9064e3f8b37b24f75083ba17f3be847

import emg_games.gui.scenes.game_chooser as game_chooser
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

    name_game = game_chooser.choose_game(screen_properties=screen_properties, kill_game=player.kill)
    print("name_game ", name_game)

    if name_game == "ŚMIECI":
        game = AbstractGame(
            full_screen=args.full_screen,
            player=player)
    game.menu()

