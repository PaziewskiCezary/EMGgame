'''Simple game with falling stuff'''
# python game.py --keyboard --lives 1 --name fsdf --not-full

import argparse
import sys
import os
import signal
import platform

from multiprocessing import Process, Lock
import time

import numpy as np

from multiprocessing.sharedctypes import Array
import multiprocessing as mp

from os import environ

from emg_games.games import Player
from emg_games.gui.scenes import ScreenProperties


from emg_games.games.player import Player
from emg_games.gui.scenes import ScreenProperties
from emg_games.games import AbstractGame

from emg_games.amplifier import Amplifier


import emg_games.gui.scenes.game_chooser as game_chooser
from emg_games.games.abstract_game import AbstractGame

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'



def play_game(queue, process_lock, samples_array, args):
    screen_properties = ScreenProperties(args.full_screen)

    '''abstract_game = AbstractGame(queue=queue,
                                    lock=process_lock,
                                    sample_array=samples_array,
                                    full_screen=args.full_screen,
                                    lives=args.lives,
                                    name=args.name)#,
                                    #screen_properties=screen_properties)'''

    player = Player(screen_properties=screen_properties, use_keyboard=args.use_keyboard, lock=process_lock,
                    sample_array=samples_array, queue=queue)

    name_game = game_chooser.choose_game(screen_properties=screen_properties, kill_game=player.kill)
    print("name_game ", name_game)
    # game._menu()

    if name_game == "ŚMIECI":
        AbstractGame(queue=queue, lock=process_lock, sample_array=samples_array,
                     full_screen=args.full_screen,
                     lives=args.lives,
                     name=player.name)  # ,
        # screen_properties=screen_properties)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    parser.add_argument('--amplifier', nargs='*', dest='use_amplifier', default=False, help='run with amplifier')
    parser.add_argument('--keyboard', nargs='*', dest='use_keyboard', default=False, help='run without amplifier')
    parser.add_argument('--not-full', nargs='*', dest='full_screen', default=True, help='turn off full screen')

    parser.add_argument('--lives', dest='lives', default=3, type=int, help='set lives number')
    parser.add_argument('--name', dest='name', default='', type=str, help='set name')

    args = parser.parse_args()
    if args.use_keyboard is not False:
        args.use_keyboard = True

    if args.full_screen is not False:
        args.full_screen = False

    if args.use_amplifier is not False:
        from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier

        args.use_amplifier = True

    if args.use_keyboard and args.use_amplifier:
        sys.exit('Can\'t use --amplifier and --keyboard at the same time')

    if not (args.use_keyboard or args.use_amplifier):
        args.use_amplifier = False
        args.use_keyboard = True


    samples_array = Array('d', np.zeros(512 * 2))
    processes_queue = mp.Queue()

    
    if args.use_amplifier:
        # amp = Amplifier(fs=512, samples=2*512)
        amp = Amplifier()

        lock = amp.lock
        samples_array = amp.data
    game_process = Process(target=play_game,
                           args=(processes_queue, lock, samples_array, args))
    game_process.start()

    try:
        while processes_queue.empty():
            pass
    except KeyboardInterrupt:
        processes_queue.put(1)

    if args.use_amplifier:

        amp.terminate()

    if platform.system() == 'Linux':
        os.kill(game_process.pid, signal.SIGKILL)
    elif platform.system() == 'Windows':
        os.kill(game_process.pid, signal.SIGTERM)
