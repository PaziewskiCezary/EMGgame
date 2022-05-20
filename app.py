import argparse
from os import environ

import pygame

from emg_games.backbones.components.player import Player
from emg_games.backbones.main_game import MainGame
from emg_games.gui.scenes import ScreenProperties

from emg_games.gui.scenes import choose_game
# from emg_games.gui.scenes import options_screen

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


# def main(args):
#
#     screen_properties = ScreenProperties(args.full_screen)
#
#     # options_screen(screen_properties=screen_properties)
#
#     player = Player(screen_properties=screen_properties)
#     gaming = True
#     while gaming:
#         game = choose_game(screen_properties=screen_properties, kill_game=player.kill)
#
#         game = game(
#             full_screen=args.full_screen,
#             player=player)
#         gaming = game.menu()
#
#     if not player._use_keyboard:
#         player.amp.terminate()

def main(args):

    screen_properties = ScreenProperties(args.full_screen)
    # screen_properties = ScreenProperties(False)

    # options_screen(screen_properties=screen_properties)

    player = Player(screen_properties=screen_properties)
    gaming = True
    while gaming:
        game = choose_game(screen_properties=screen_properties, kill_game=player.kill)

        game = game(
            full_screen=args.full_screen,
            player=player)
        gaming = game.menu()

    if not player._use_keyboard:
        player.amp.terminate()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EMG game')

    parser.add_argument('--full', dest='full_screen', action='store_true', help='turn off full screen')
    parser.add_argument('--name', dest='amp_name', action='store', type=str, required=False,
                        help='name of streamer', default=None)


    args = parser.parse_args()

    pygame.init()

    #main(args)
    M = MainGame(args)
    if not M.player._use_keyboard:
        player.amp.terminate()
