import argparse
import sys
from os import environ

from emg_games.games.player import Player
from emg_games.gui.scenes import ScreenProperties

from emg_games.gui.scenes import choose_game

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


def main(args):

    screen_properties = ScreenProperties(args.full_screen)

    player = Player(screen_properties=screen_properties)

    game = choose_game(screen_properties=screen_properties, kill_game=player.kill)

    game = game(
        full_screen=args.full_screen,
        player=player)
    game.menu()

    if not player._use_keyboard:
        player.amp.terminate()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    parser.add_argument('--not-full', dest='full_screen', action='store_true', help='turn off full screen')

    args = parser.parse_args()

    main(args)
