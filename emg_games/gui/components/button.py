import pygame


class Button(object):
    def __init__(self, screen, label, pos, dims, button_color, label_color, func, font_size):

        self.__screen = screen
        self.__label = label
        self.__x_position, self.__y_position = pos
        self.__dims = dims
        self.__button_color = button_color
        self.__label_color = label_color
        self.__font = pygame.font.SysFont('Teko', font_size)
        self.__func = func

        self.pressed = False

        self.__add_rectangular()
        self.__add_text()

    def __add_rectangular(self):

        weight, height = self.__dims
        self.rectangular = pygame.draw.rect(self.__screen, self.__button_color,
                                            (self.__x_position - weight / 2, self.__y_position - height / 2, weight,
                                             height))

    def __add_text(self):

        text_width, text_height = self.__font.size(self.__label)
        self.__screen.blit(self.__font.render(self.__label, True, self.__label_color),
                           (self.__x_position - text_width / 2, self.__y_position - text_height / 2))

    def on_click(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = event.pos  # gets mouse position

            # checks if mouse position is over the button
            if self.rectangular.collidepoint(mouse_position):
                self.pressed = True
                self.__func()
