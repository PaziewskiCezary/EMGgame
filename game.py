'''Simple game with falling stuff'''

import pygame

from game_classes import Simple_Game


screen_size = 16*70, 9 * 70
game = Simple_Game(screen_size)
game.main()
