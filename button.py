import pygame
import sys
# from pygame.locals import *


class Button(object):
    def __init__(self, screen, label, pos, dims, button_color, label_color=(255,255,255)):
        
        self.screen = screen
        self.label = label
        self.pos = pos
        self.dims = dims
        self.button_color = button_color
        self.label_color = label_color
        self.font = pygame.font.SysFont('Arial', 25)
        
        
        self.addRect()
        self.addText()



    def addRect(self):
        pos_x, pos_y = self.pos
        weight, height = self.dims
        self.rect = pygame.draw.rect(self.screen, self.button_color, (pos_x-weight/2, pos_y-height/2, weight, height), 0)


    def addText(self):
        l = self.label
        pos_x, pos_y = self.pos
        weight, height = self.dims
        text_width, text_height = self.font.size(l)
        self.screen.blit(self.font.render(l, True, self.label_color), (pos_x-text_width/2, pos_y-text_height/2))
        
        
    def onClick(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if self.rect.collidepoint(mouse_pos):
                # prints current location of mouse
                print('button was pressed at {0}'.format(mouse_pos))





if __name__ == '__main__':
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60

    clock.tick(fps)
    pygame.display.set_caption('Box Test')
    screen = pygame.display.set_mode((600,400), 0, 32)
    screen.fill((154, 7, 118))

    b = Button(screen, 'Hello', (300,200), (200, 100), (173, 170, 218), (218, 170, 214))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            b.onClick(event)
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit();
        pygame.display.update()