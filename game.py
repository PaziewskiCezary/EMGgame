'''Simple game with falling stuff'''
# python game.py --keyboard --lives 1 --name fsdf --not-full

import argparse
import sys

from multiprocessing import Process, Lock
import time

import numpy as np

from multiprocessing.sharedctypes import Array
import multiprocessing as mp

from simple_game import SimpleGame


def connect_amplifier(process_lock, samples_array, sampling_frequency=512, number_of_samples=64, channels=[0, 1]):
    amplifiers = TmsiCppAmplifier.get_available_amplifiers('usb')
    if not amplifiers:
        raise ValueError("Nie ma wzmacniacza")
    amplifier = TmsiCppAmplifier(amplifiers[0])
    amplifier.sampling_rate = sampling_frequency
    gains = np.array(amplifier.current_description.channel_gains)
    offsets = np.array(amplifier.current_description.channel_offsets)

    amplifier.start_sampling()
    time.sleep(1)
    while True:

        try:
            samples = amplifier.get_samples(number_of_samples).samples * gains + offsets
            
            samples = samples[:, channels[0]] - samples[:, channels[1]]
            with process_lock:
                samples_array[:-number_of_samples] = samples_array[number_of_samples:]
                samples_array[-number_of_samples:] = Array('d', samples)
        except Exception as e:
            print(e)


def play_game(queue, process_lock, sample_array, screen_size, use_keyboard=False, lives=3, default_name='', full_screen=True):
    game = SimpleGame(queue, process_lock, sample_array, screen_size, use_keyboard=use_keyboard,
                      lives=lives, default_name=default_name,
                      full_screen=full_screen)
    game._menu()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    parser.add_argument('--amplifier', nargs='*', dest='use_amplifier', default=False, help='run with amplifier')
    parser.add_argument('--keyboard', nargs='*', dest='use_keyboard', default=False, help='run without amplifier')
    parser.add_argument('--not-full', nargs='*', dest='full_screen', default=True, help='turn off full screen')

    parser.add_argument('--lives', dest='lives', default=5, type=int, help='set lives number')
    parser.add_argument('--name', dest='name', default='', type=str, help='set name')

    args = parser.parse_args()

    if args.use_keyboard is not False:
        args.use_keyboard = True
    if args.use_amplifier is not False:
        from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier

        args.use_amplifier = True
    if args.full_screen is not True:
        args.full_screen = False

    if args.use_keyboard and args.use_amplifier:
        sys.exit('Can\'t use --amplifier and --keyboard at the same time')

    if not (args.use_keyboard or args.use_amplifier):
        args.use_amplifier = False
        args.use_keyboard = True

    default_screen_size = 16 * 70, 9 * 70

    lock = Lock()

    samples_array = Array('d', np.zeros(512 * 2))
    processes_queue = mp.Queue()

    game_process = Process(target=play_game,
                           args=(processes_queue, lock, samples_array, default_screen_size,
                                 args.use_keyboard, args.lives, args.name, args.full_screen))
    if args.use_amplifier:
        amplifier_process = Process(target=connect_amplifier, args=(lock, samples_array))
        amplifier_process.start()
    game_process.start()
    while processes_queue.empty():
        pass
    if args.use_amplifier:
        print(1)
        amplifier_process.terminate()
    game_process.terminate()
    print(3)
    exit()
