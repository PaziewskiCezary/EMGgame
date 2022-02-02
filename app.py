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
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from emg_games.games import Player
from emg_games.gui.scenes import ScreenProperties
from emg_games.amplifier import Amplifier

def play_game(queue, process_lock, samples_array, args):

    screen_properties = ScreenProperties(args.full_screen)

    '''abstract_game = AbstractGame(queue=queue,
                                    lock=process_lock,
                                    sample_array=samples_array,
                                    full_screen=args.full_screen,
                                    lives=args.lives,
                                    name=args.name)#,
                                    #screen_properties=screen_properties)'''

    player = Player(screen_properties=screen_properties, use_keyboard=args.use_keyboard, lock=process_lock, sample_array=samples_array)

    #game._menu()


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

    lock = Lock()

    samples_array = Array('d', np.zeros(512 * 2))
    processes_queue = mp.Queue()

    game_process = Process(target=play_game,
                           args=(processes_queue, lock, samples_array, args))
    game_process.start()
    
    if args.use_amplifier:
        amp = Amplifier()

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
