import pygame


class ScreenProperties():
    """Screen"""

    def __init__(self, full_screen):
        self.scale = 1
        self.__full_screen = full_screen
        if self.__full_screen:
            display_info = pygame.display.Info()
            auto_screen_resolution = (display_info.current_w, display_info.current_h)
            self.__screen = pygame.display.set_mode(auto_screen_resolution, pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode((1040, 585))

        self.__x_screen = self.__screen.get_width()
        self.__y_screen = self.__screen.get_height()
        self.__screen_size = (self.__x_screen, self.__y_screen)

    @property
    def screen(self):
        return self.__screen

    @property
    def x_screen(self):
        return self.__x_screen

    @property
    def y_screen(self):
        return self.__y_screen

    @property
    def screen_size(self):
        return self.__screen_size


