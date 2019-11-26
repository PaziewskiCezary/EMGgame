'''Simple game with falling stuff'''

import pygame

from game_classes import Simple_Game


def main():
    screen_size = 16*70, 9 * 70
    game = Simple_Game(screen_size)
    while game:
        
        game.main()


    print("end")


if __name__ == '__main__':
    main()
