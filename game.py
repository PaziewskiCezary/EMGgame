'''Simple game with falling stuff'''
# python game.py --keyboard --lifes 1 --name fsdf --not-full

import argparse
import sys

from multiprocessing import Process, Lock
from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
import time

import numpy as np

from multiprocessing.sharedctypes import Value, Array

def amp(l, a1, fs=512, ds=64, channels=[0,1]):
    amps = TmsiCppAmplifier.get_available_amplifiers('usb')
    if not amps:
        raise ValueError("Nie ma wzmacniacza")
    amp = TmsiCppAmplifier(amps[0])
    amp.sampling_rate = fs
    gains = np.array(amp.current_description.channel_gains)
    offsets = np.array(amp.current_description.channel_offsets)

    amp.start_sampling()    

    while True:    
        t = time.time()
        s = amp.get_samples(ds).samples * gains + offsets

        t2 = time.time()
        s = s[:,channels[0]] - s[:,channels[1]]
        l.acquire()
        a1[:-ds] = a1[ds:]
        a1[-ds:] = Array('d', s)
        l.release()

def play_game(lock, sample_array, screen_size, use_keyboard=False, lifes=3, default_name='', full_screen=True):
    game = Simple_Game(lock, sample_array, screen_size, use_keyboard=use_keyboard, 
                            lifes=lifes, default_name=default_name, 
                            full_screen=full_screen)
    game.menu()


from game_classes import Simple_Game

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    parser.add_argument('--amplifier', nargs='*', dest='use_amplifier', default=False, help='run with aplifier')
    parser.add_argument('--keyboard', nargs='*', dest='use_keyboard', default=False, help='run without aplifier')
    parser.add_argument('--not-full', nargs='*', dest='full_screen', default=True, help='turn off full screen')

    parser.add_argument('--lifes', dest='lifes', default=5, type=int, help='set lifes number')
    parser.add_argument('--name', dest='name', default='', type=str, help='set name')

    args = parser.parse_args()

    if args.use_keyboard is not False:
        args.use_keyboard = True
    if args.use_amplifier is not False:
        args.use_amplifier = True
    if args.full_screen is not True:
        args.full_screen = False

    if args.use_keyboard and args.use_amplifier:
        sys.exit('Can\'t use --amplifier and --keyboard at the same time')
    
    if not (args.use_keyboard or args.use_amplifier):
        args.use_amplifier = True
        args.use_keyboard = False

    screen_size = 16 * 70, 9 * 70

    l = Lock()

    a1 = Array('d', np.zeros(512*2))

    p = Process(target=amp, args=(l, a1))
    p2 = Process(target=play_game, args=(l, a1, screen_size, args.use_keyboard, args.lifes, args.name, args.full_screen))
    p.start()
    p2.start()
    
    #p.join()
    #p2.join()

    try:
        while True:
            pass
    except KeyboardInterrup:
        p.kill()
        p2.kill()
