'''Simple game with falling stuff'''
# python game.py --keyboard --lifes 1 --name fsdf --not-full

import argparse
import sys

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
    if args.use_keyboard:
        game = Simple_Game(screen_size, use_keyboard=True, 
                            lifes=args.lifes, default_name=args.name, 
                            full_screen=args.full_screen)
    if args.use_amplifier:
        game = Simple_Game(screen_size, use_keyboard=False, 
                            lifes=args.lifes, default_name=args.name, 
                            full_screen=args.full_screen)
    while game.menu():
        pass
